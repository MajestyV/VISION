# 此代码专用于分析KEITHLEY4200测得的晶体管的数据

import numpy as np
import matplotlib.pyplot as plt
from src.Electrica.KEITHLEY4200.KEITHLEY4200_GetData import GetData_KEITHLEY4200A_SCS  # 数据读取函数

# 通过定义一个字典，方便地将缩写转换为全称
abbrev_dict = {'t': 'Time', 'Gm': 'GM',
               'V_g': 'GateV', 'V_d': 'DrainV', 'V_s': 'SourceV', 'I_g': 'GateI', 'I_d': 'DrainI', 'I_s': 'SourceI'}

class Characteristics_Transistors:
    '''
    此函数类专用于分析晶体管特性
    '''
    def __init__(self, data: dict, channel_type: str='P', sweep_mode: str='DualSweep', analysis_subject: str='I_drain',
                 characteristic: str='Transfer', **kwargs):
        '''
        初始化函数
        DataFrame类型的变量可以看作字典，详情请参考：
        https://www.quora.com/Are-there-advantages-of-Python-dictionaries-over-Pandas-dataframes#:~:text=A%20dictionary%20is%20a%20collection,%2C%20an%20array%2Dlike%20structure.
        '''

        # 从数据字典中获取数据，同时转换为numpy数组
        V_g = data[abbrev_dict['V_g']].values
        V_d = data[abbrev_dict['V_d']].values

        I_g = data[abbrev_dict['I_g']].values
        I_d = data[abbrev_dict['I_d']].values
        # 在4200中，Drain端为施加电压Vds的端口，所以Drain端电流流出，为正值；Source端电流流入，故为负值，需要取绝对值
        I_s = np.abs(data[abbrev_dict['I_s']].values)

        num_points = len(V_g)  # 获取数据点数

        if sweep_mode == 'DualSweep':
            # 分别获取正向和反向的数据（在python中，//是整除号）
            # 此处的flip()函数是将数组逆序排列，对于反向的数据需要倒序，防止在后续的分析模块中算出相反数
            V_g_forward, V_g_backward = (V_g[:num_points//2], np.flip(V_g[num_points//2:]))
            V_d_forward, V_d_backward = (V_d[:num_points//2], np.flip(V_d[num_points//2:]))
            I_g_forward, I_g_backward = (I_g[:num_points//2], np.flip(I_g[num_points//2:]))
            I_d_forward, I_d_backward = (I_d[:num_points//2], np.flip(I_d[num_points//2:]))
            I_s_forward, I_s_backward = (I_s[:num_points//2], np.flip(I_s[num_points//2:]))

            sweep = kwargs['sweep'] if 'sweep' in kwargs else 'forward'  # 获取扫描方向，默认为正向

            if sweep == 'forward':
                self.V_g, self. V_d, self.I_g, self.I_d, self.I_s = (V_g_forward, V_d_forward, I_g_forward, I_d_forward, I_s_forward)
            elif sweep == 'backward':
                self.V_g, self. V_d, self.I_g, self.I_d, self.I_s = (V_g_backward, V_d_backward, I_g_backward, I_d_backward, I_s_backward)
            else:
                raise ValueError('Invalid sweep direction, please choose from "forward" or "backward"')

        elif sweep_mode == 'SingleSweep':
            self.V_g, self. V_d, self.I_g, self.I_d, self.I_s = (V_g, V_d, I_g, I_d, I_s)

        else:
            raise ValueError('Invalid sweep mode, please choose from "DualSweep" or "SingleSweep"')

        # 器件分析参数
        self.channel_type = channel_type  # 器件类型
        # 由于半导体分析仪即会测I_source也会测I_drain，所以需要指定具体的分析对象
        if analysis_subject == 'I_source':
            self.I_ds = self.I_s
        elif analysis_subject == 'I_drain':
            self.I_ds = self.I_d
        else:
            raise ValueError('Invalid analysis subject, please choose from "I_source" or "I_drain"')

    def TransferCurve(self): return self.V_g, self.I_d, self.I_s, self.I_g  # 返回转移曲线数据

    def LeakageCurrent(self): return np.mean(np.abs(self.I_g))  # 计算平均漏电流

    def OnOffRatio_Extreme(self):
        '''
        极限开关比
        '''
        I_d, I_s = np.abs(self.I_d), np.abs(self.I_s)  #由于机器在电流极小时会出现负值，所以取绝对值

        on_off_ratio_Id = np.max(I_d)/np.min(I_d)  # 用Id计算开关比
        on_off_ratio_Is = np.max(I_s)/np.min(I_s)  # 用Is计算开关比
        return np.max([on_off_ratio_Id,on_off_ratio_Is])  # 计算开关比

    def OnOffRatio(self, on_region: tuple=None, off_region: tuple=None):
        '''
        计算正常的开关比
        '''

        Vgs, Ids = self.V_g, self.I_ds   # 获取Vgs和Ids数据

        on_start, on_end = on_region     # 开启区间
        off_start, off_end = off_region  # 关断区间

        Ids_on = Ids[np.logical_and(Vgs >= on_start, Vgs <= on_end)]     # 获取开启区间的Ids数据
        Ids_off = Ids[np.logical_and(Vgs >= off_start, Vgs <= off_end)]  # 获取关断区间的Ids数据
        on_off_ratio = np.mean(np.abs(Ids_on))/np.mean(np.abs(Ids_off))  # 计算开关比（由于机器在电流极小时会出现负值，所以取绝对值）

        return on_off_ratio

    def ThresholdVoltage(self, Vth_location: tuple=None, window_size: int=10, boundary_cond: str='same',
                         mode: str='auto') -> tuple:
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
            if Vth_location is not None:
                Vgs_start, Vgs_end = Vth_location  # 获取评估范围
            else:
                Vgs_start, Vgs_end = (Vgs[0], Vgs[-1])  # 默认评估范围为整个数据范围

            d2I_dV2_selected = d2I_dV2[np.logical_and(Vgs >= Vgs_start, Vgs <= Vgs_end)]  # 获取评估范围内的数据索引
            d2I_dV2_max = np.max(d2I_dV2_selected)  # 获取最大值
            Vth = Vgs[np.where(d2I_dV2 == d2I_dV2_max)][0]  # 获取阈值电压

            return Vth, dI_dV, d2I_dV2

        else:
            raise ValueError('Invalid mode, please choose from "auto" or "manual"')

    def SubthresholdSwing(self, evaluation_range: tuple=None, Vth_neighbor: float=0.2, **kwargs):
        '''
        计算亚阈值摆幅，详见：https://en.wikipedia.org/wiki/Subthreshold_swing
        公式参考：chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://hal.science/hal-03368147/document
        '''
        Ids_log = np.log10(np.abs(self.I_ds))  # 对Ids取对数（由于机器在电流极小时会出现负值，所以取绝对值）
        Vgs = self.V_g  # Gate-source电压

        # 选定评估范围内计算SS
        if evaluation_range is not None:                        # 手动模式 - 指定SS的评估范围
            Vgs_start, Vgs_end = evaluation_range
        elif 'mode' in kwargs and kwargs['mode'] == 'default':  # 默认模式 - 默认评估整个数据范围
            Vgs_start, Vgs_end = (Vgs[0], Vgs[-1])
        elif 'mode' in kwargs and kwargs['mode'] == 'auto':     # 自动模式 - 自动获取阈值电压并根据阈值电压指定评估范围
            Vth = self.ThresholdVoltage()[0]                               # 获取阈值电压
            Vgs_start, Vgs_end = (Vth - Vth_neighbor, Vth + Vth_neighbor)  # 评估阈值电压附近的数据
        else:
            raise ValueError('Invalid mode, please choose from "auto" or "default"')

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
    data = GetData_KEITHLEY4200A_SCS(f'{data_directory}/{data_file}')

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