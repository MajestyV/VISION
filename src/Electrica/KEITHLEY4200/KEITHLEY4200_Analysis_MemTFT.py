# 此代码专用于分析KEITHLEY4200测得的晶体管的数据

import numpy as np
import matplotlib.pyplot as plt
from src.Electrica.KEITHLEY4200.KEITHLEY4200_GetData import GetData_KEITHLEY4200_OldModel  # 数据读取函数

# 通过定义一个字典，方便地将缩写转换为全称
abbrev_dict = {'t': 'Time', 'Gm': 'GM',
               'V_g': 'GateV', 'V_d': 'DrainV', 'V_s': 'SourceV', 'I_g': 'GateI', 'I_d': 'DrainI', 'I_s': 'SourceI'}

class MemTransistorCharacteristics:
    '''
    此函数类专用于分析晶体管特性
    '''
    def __init__(self, data: dict, channel_type: str='P', analysis_subject: str='I_source'):
        '''
        初始化函数
        DataFrame类型的变量可以看作字典，详情请参考：
        https://www.quora.com/Are-there-advantages-of-Python-dictionaries-over-Pandas-dataframes#:~:text=A%20dictionary%20is%20a%20collection,%2C%20an%20array%2Dlike%20structure.
        '''

        # 从数据字典中获取数据，同时转换为numpy数组
        Vg = data[abbrev_dict['V_g']].values
        Vd = data[abbrev_dict['V_d']].values
        Ig = data[abbrev_dict['I_g']].values
        Id = data[abbrev_dict['I_d']].values
        # 在4200中，Drain端为施加电压Vds的端口，所以Drain端电流流出，为正值；Source端电流流入，故为负值，需要取绝对值
        Is = np.abs(data[abbrev_dict['I_s']].values)

        num_points = len(V_g)  # 获取数据点数

        # 分别获取正向和反向的数据（在python中，//是整除号）
        # 此处的flip()函数是将数组逆序排列，对于反向的数据需要倒序，防止在后续的分析模块中算出相反数
        self.Vg_forward, self.Vg_backward = (Vg[:num_points//2], np.flip(Vg[num_points//2:]))
        self.Vd_forward, self.Vd_backward = (Vd[:num_points//2], np.flip(Vd[num_points//2:]))
        self.Ig_forward, self.Ig_backward = (Ig[:num_points//2], np.flip(Ig[num_points//2:]))
        self.Id_forward, self.Id_backward = (Id[:num_points//2], np.flip(Id[num_points//2:]))
        self.Is_forward, self.Is_backward = (Is[:num_points//2], np.flip(Is[num_points//2:]))

        # 器件分析参数
        self.channel_type = channel_type  # 器件类型
        # 由于半导体分析仪即会测I_source也会测I_drain，所以需要指定具体的分析对象
        if analysis_subject == 'I_source':
            self.Ids_forward, self.Ids_backward = (self.Is_forward, self.Is_backward)
        elif analysis_subject == 'I_drain':
            self.Ids_forward, self.Ids_backward = (self.Id_forward, self.Id_backward)
        else:
            raise ValueError('Invalid analysis subject, please choose from "I_source" or "I_drain"')

    def TransferCurve(self):
        forward_sweep = (self.Vg_forward, self.Id_forward, self.Is_forward, self.Ig_forward)  # 正向扫描
        backward_sweep = (self.Vg_backward, self.Id_backward, self.Is_backward, self.Ig_backward)  # 反向扫描
        return forward_sweep, backward_sweep  # 返回转移曲线数据

    def LeakageCurrent(self):
        leakage_forward = np.mean(np.abs(self.Ig_forward))  # 正向漏电流
        leakage_backward = np.mean(np.abs(self.Ig_backward))  # 反向漏电流
        return np.mean([leakage_forward, leakage_backward])  # 返回平均漏电流

    def OnOffRatio_Extreme(self):
        # 正向极限开关比
        on_off_ratio_Id_forward = np.max(self.Id_forward)/np.min(self.Id_backward)  # 用Id计算开关比
        on_off_ratio_Is_forward = np.max(self.Is_forward)/np.min(self.Is_backward)  # 用Is计算开关比
        # 反向极限开关比
        on_off_ratio_Is_backward = np.max(self.Is_backward)/np.min(self.Is_backward)  # 用Is计算开关比
        on_off_ratio_Id_backward = np.max(self.Id_backward) / np.min(self.Id_backward)  # 用Id计算开关比
        return (max([on_off_ratio_Id_forward, on_off_ratio_Is_forward]),
                max([on_off_ratio_Is_backward, on_off_ratio_Id_backward]))


    def OnOffRatio(self, on_region: tuple=None, off_region: tuple=None):
        '''
        计算正常的开关比
        '''

        Vgs, Ids = self.V_g, self.I_ds  # 获取Vgs和Ids数据

        on_start, on_end = on_region  # 开启区间
        off_start, off_end = off_region  # 关断区间

        Ids_on = Ids[np.logical_and(Vgs >= on_start, Vgs <= on_end)]  # 获取开启区间的Ids数据
        Ids_off = Ids[np.logical_and(Vgs >= off_start, Vgs <= off_end)]  # 获取关断区间的Ids数据
        on_off_ratio = np.mean(Ids_on)/np.mean(Ids_off)  # 计算开关比



        return on_off_ratio

    def ThresholdVoltage(self, mode: str='auto', window_size: int=10, boundary_cond: str='same',
                         evaluation_range: tuple=None):
        '''
        计算阈值电压（通常将传输特性曲线中输出电压随输入电压改变而急剧变化转折区的中点对应的输入电压称为阈值电压）
        '''

        Vgs, Ids_raw = self.V_g, self.I_ds  # 获取Vgs和Ids数据

        if mode == 'auto':  # 自动模式
            window = np.ones(int(window_size)) / float(window_size)
            Ids = np.convolve(Ids_raw, window, boundary_cond)  # 平滑数据

            dI_dV = np.gradient(Ids, Vgs)  # 计算Ids对Vgs的导数
            d2I_dV2 = np.gradient(dI_dV, Vgs)  # 计算dI_dV对Vgs的导数

            Vgs_start, Vgs_end = (Vgs[0], Vgs[-1])  # 评估整个数据范围

            d2I_dV2_selected = d2I_dV2[np.logical_and(Vgs >= Vgs_start, Vgs <= Vgs_end)]  # 获取评估范围内的数据索引
            d2I_dV2_max = np.max(d2I_dV2_selected)  # 获取最大值
            Vth = Vgs[np.where(d2I_dV2 == d2I_dV2_max)][0]  # 获取阈值电压

            return Vth, dI_dV, d2I_dV2

        elif mode == 'manual':  # 手动模式
            Ids = Ids_raw

            dI_dV = np.gradient(Ids, Vgs)  # 计算Ids对Vgs的导数
            d2I_dV2 = np.gradient(dI_dV, Vgs)  # 计算dI_dV对Vgs的导数

            # 选定评估范围内计算阈值电压
            if evaluation_range is not None:
                Vgs_start, Vgs_end = evaluation_range  # 获取评估范围
            else:
                Vgs_start, Vgs_end = (Vgs[0], Vgs[-1])  # 默认评估范围为整个数据范围

            d2I_dV2_selected = d2I_dV2[np.logical_and(Vgs >= Vgs_start, Vgs <= Vgs_end)]  # 获取评估范围内的数据索引
            d2I_dV2_max = np.max(d2I_dV2_selected)  # 获取最大值
            Vth = Vgs[np.where(d2I_dV2 == d2I_dV2_max)][0]  # 获取阈值电压

            return Vth, dI_dV, d2I_dV2

        else:
            raise ValueError('Invalid mode, please choose from "auto" or "manual"')

    def SubthresholdSwing(self, mode: str='auto', Vth_neighbor: float=0.2, evaluation_range: tuple=None):
        '''
        计算亚阈值摆幅，详见：https://en.wikipedia.org/wiki/Subthreshold_swing
        公式参考：chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://hal.science/hal-03368147/document
        '''
        Ids_log = np.log10(self.I_ds)  # 对Ids取对数
        Vgs = self.V_g  # Gate-source电压

        # 选定评估范围内计算SS
        if mode == 'auto':
            Vth = self.ThresholdVoltage()[0]  # 获取阈值电压
            Vgs_start, Vgs_end = (Vth-Vth_neighbor, Vth+Vth_neighbor)  # 评估阈值电压附近的数据
        elif (mode == 'manual') and (evaluation_range is not None):
            Vgs_start, Vgs_end = evaluation_range  # 获取评估范围
        elif (mode == 'manual') and (evaluation_range is None):
            Vgs_start, Vgs_end = (Vgs[0], Vgs[-1])  # 默认评估范围为整个数据范围
        else:
            raise ValueError('Invalid mode, please choose from "auto" or "manual"')

        index_selected = np.where(np.logical_and(Vgs >= Vgs_start, Vgs <= Vgs_end))  # 获取评估范围内的数据索引
        Vgs_selected = Vgs[index_selected]  # 获取评估范围内的Vgs数据
        Ids_log_selected = Ids_log[index_selected]  # 获取评估范围内的Ids数据

        # 计算亚阈值摆幅（SS - Subthreshold Swing）
        # 利用numpy的梯度函数计算各点导数，详见：https://numpy.org/doc/stable/reference/generated/numpy.gradient.html
        if self.channel_type == 'P':
            SS = -np.gradient(Vgs_selected, Ids_log_selected)  # 对于P型器件，Ids随Vgs增大而减小，所以需要加负号
        elif self.channel_type == 'N':
            SS = np.gradient(Vgs_selected, Ids_log_selected)  # 对于N型器件，Ids随Vgs增大而增大，所以不需要加负号
        else:
            raise ValueError('Invalid channel type, please choose from "P" or "N"')

        SS_mean = np.mean(SS)  # 计算平均值

        return SS_mean


if __name__ == '__main__':
    # 数据路径
    data_directory = 'D:/Projects/Jingfang Pei/Solution-processed IC/Data/4200/20240708 tft 10x10 array'
    data_file = 'line_1.xls'

    # 获取数据
    data = GetData_KEITHLEY4200_OldModel(f'{data_directory}/{data_file}')

    example_data = data[0]

    V_g = example_data[abbrev_dict['V_g']]
    V_d = example_data[abbrev_dict['V_d']]
    # V_s = example_data[abbrev_dict['V_s']]

    I_g = example_data[abbrev_dict['I_g']]
    I_d = example_data[abbrev_dict['I_d']]
    I_s = example_data[abbrev_dict['I_s']]

    # 创建晶体管特性对象
    transistor = TransistorCharacteristics(example_data, sweep='backward')
    Vgs, Id, Is, Ig = transistor.TransferCurve()
    on_off_ratio_extreme = transistor.OnOffRatio_Extreme()
    print(on_off_ratio_extreme)
    on_off_ratio = transistor.OnOffRatio((-0.5,-0.48), (1.24,1.26))
    print(on_off_ratio)
    SS, SS_mean = transistor.SubthresholdSwing((0.7,0.9))
    print(SS_mean)
    leakage_avg = transistor.LeakageCurrent()
    print(leakage_avg)

    Vth, dI_dV, d2I_dV2 = transistor.ThresholdVoltage((0.25,1.25))
    print(Vth)

    # 可视化模块
    # plt.plot(V_g, I_d, label='Transfer')
    plt.plot(Vgs, Is, label='Transfer')
    plt.plot(Vgs, np.abs(Ig), label='Leakage')
    # plt.plot(Vgs, SS, label='SS')

    # plt.plot(Vgs, dI_dV, label='dI_dV')
    # plt.plot(Vgs, d2I_dV2, label='d2I_dV2')

    # plt.xlim(0.5,1.0)
    # plt.ylim(0,-2)

    plt.yscale('log')  # 设置y轴为对数坐标

    plt.legend(loc='best')

    plt.show(block=True)