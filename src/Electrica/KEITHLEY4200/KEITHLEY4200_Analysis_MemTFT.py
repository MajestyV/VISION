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

        num_points = len(Vg)  # 获取数据点数

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

    def TransferCurve(self) -> tuple:
        forward_sweep = (self.Vg_forward, self.Id_forward, self.Is_forward, self.Ig_forward)  # 正向扫描
        backward_sweep = (self.Vg_backward, self.Id_backward, self.Is_backward, self.Ig_backward)  # 反向扫描
        return forward_sweep, backward_sweep  # 返回转移曲线数据

    def LeakageCurrent(self) -> float:
        leakage_forward = np.mean(np.abs(self.Ig_forward))  # 正向漏电流
        leakage_backward = np.mean(np.abs(self.Ig_backward))  # 反向漏电流
        return np.mean([leakage_forward, leakage_backward])  # 返回平均漏电流

    def OnOffRatio_Extremum(self) -> tuple:
        # 正向极限开关比
        on_off_ratio_Id_forward = np.max(self.Id_forward)/np.min(self.Id_backward)  # 用Id计算开关比
        on_off_ratio_Is_forward = np.max(self.Is_forward)/np.min(self.Is_backward)  # 用Is计算开关比
        # 反向极限开关比
        on_off_ratio_Is_backward = np.max(self.Is_backward)/np.min(self.Is_backward)  # 用Is计算开关比
        on_off_ratio_Id_backward = np.max(self.Id_backward) / np.min(self.Id_backward)  # 用Id计算开关比
        return (max([on_off_ratio_Id_forward, on_off_ratio_Is_forward]),
                max([on_off_ratio_Is_backward, on_off_ratio_Id_backward]))

    def OnOffRatio(self, on_region: tuple=None, off_region: tuple=None) -> tuple:
        '''
        计算正常意义下的开关比
        '''

        Vgs_forward, Ids_forward = self.Vg_forward, self.Ids_forward  # 获取正向扫描的Vgs和Ids数据
        Vgs_backward, Ids_backward = self.Vg_backward, self.Ids_backward  # 获取反向扫描的Vgs和Ids数据

        on_start, on_end = on_region  # 开启区间
        off_start, off_end = off_region  # 关断区间

        # 正向扫描
        Ids_on_forward = Ids_forward[np.logical_and(Vgs_forward >= on_start, Vgs_forward <= on_end)]  # 获取开启区间的Ids数据
        Ids_off_forward = Ids_forward[np.logical_and(Vgs_forward >= off_start, Vgs_forward <= off_end)]  # 获取关断区间的Ids数据
        on_off_ratio_forward = np.mean(Ids_on_forward)/np.mean(Ids_off_forward)  # 计算开关比
        # 反向扫描
        Ids_on_backward = Ids_backward[np.logical_and(Vgs_backward >= on_start, Vgs_backward <= on_end)]  # 获取开启区间的Ids数据
        Ids_off_backward = Ids_backward[np.logical_and(Vgs_backward >= off_start, Vgs_backward <= off_end)]  # 获取关断区间的Ids数据
        on_off_ratio_backward = np.mean(Ids_on_backward)/np.mean(Ids_off_backward)  # 计算开关比

        return (on_off_ratio_forward, on_off_ratio_backward)

    def ThresholdVoltage(self, Vgs, Ids, window_size: int=10, boundary_cond: str='same',
                         evaluation_range: tuple=None) -> tuple:
        '''
        计算阈值电压（通常将传输特性曲线中输出电压随输入电压改变而急剧变化转折区的中点对应的输入电压称为阈值电压）
        '''

        if evaluation_range is not None:
            Vgs_start, Vgs_end = evaluation_range  # 获取阈值电压评估范围
        else:
            Vgs_start, Vgs_end = (Vgs[0], Vgs[-1])  # 默认评估范围为整个数据范围

        # 平滑数据，防止噪声对后面的求导计算产生影响
        conv_window = np.ones(int(window_size)) / float(window_size)
        Ids = np.convolve(Ids, conv_window, boundary_cond)

        dI_dV = np.gradient(Ids, Vgs)  # 计算Ids对Vgs的导数
        d2I_dV2 = np.gradient(dI_dV, Vgs)  # 计算dI_dV对Vgs的导数

        d2I_dV2_selected = d2I_dV2[np.logical_and(Vgs >= Vgs_start, Vgs <= Vgs_end)]  # 获取评估范围内的数据索引
        d2I_dV2_max = np.max(d2I_dV2_selected)  # 获取最大值
        Vth = Vgs[np.where(d2I_dV2 == d2I_dV2_max)][0]  # 获取阈值电压

        return Vth, dI_dV, d2I_dV2

    def MemoryWindow(self, window_size: int=10, boundary_cond: str='same', evaluation_range: tuple=None) -> float:
        '''
        计算存储窗口
        '''
        Vgs_forward, Ids_forward = self.Vg_forward, self.Ids_forward  # 获取正向扫描的Vgs和Ids数据
        Vgs_backward, Ids_backward = self.Vg_backward, self.Ids_backward  # 获取反向扫描的Vgs和Ids数据

        # 获取正向扫描阈值电压
        Vth_forward, dI_dV_forward, d2I_dV2_forward = self.ThresholdVoltage(Vgs_forward, Ids_forward, window_size,
                                                                            boundary_cond, evaluation_range)
        # 获取反向扫描阈值电压
        Vth_backward, dI_dV_backward, d2I_dV2_backward = self.ThresholdVoltage(Vgs_backward, Ids_backward, window_size,
                                                                               boundary_cond, evaluation_range)

        return np.abs(Vth_forward - Vth_backward)  # 返回存储窗口

    def SubthresholdSwing(self,V_FullWidth: float=1, window_size: int=10, boundary_cond: str='same',
                          evaluation_range: tuple[tuple,tuple]=None) -> tuple[list,list]:
        '''
        计算亚阈值摆幅，详见：https://en.wikipedia.org/wiki/Subthreshold_swing
        公式参考：chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://hal.science/hal-03368147/document
        '''

        # 数据字典
        # 有时KEITHLEY4200在读取微小电流时会出现负值，因此对数运算前先进行绝对值运算，防止出现程序运行出错
        data_dict = {'forward': (self.Vg_forward, np.log10(np.abs(self.Ids_forward)), evaluation_range[0]),
                     'backward': (self.Vg_backward, np.log10(np.abs(self.Ids_backward)), evaluation_range[1])}


        SS_list = []  # 创建一个空列表，用于存储亚阈值摆幅
        V_swing_list = []  # 创建一个空列表，用于存储摆幅电压

        for sweep in ('forward', 'backward'):

            Vgs, Ids_log, eval_range = data_dict[sweep]

            if evaluation_range is not None:
                Vgs_start, Vgs_end = eval_range  # 获取阈值电压评估范围
            else:
                Vgs_start, Vgs_end = (Vgs[0], Vgs[-1])  # 默认评估范围为整个数据范围

            # 平滑数据，防止噪声对后面的求导计算产生影响
            conv_window = np.ones(int(window_size)) / float(window_size)
            Ids_log = np.convolve(Ids_log, conv_window, boundary_cond)

            # 计算亚阈值摆幅（SS - Subthreshold Swing）
            # 利用numpy的梯度函数计算各点导数，详见：https://numpy.org/doc/stable/reference/generated/numpy.gradient.html
            if self.channel_type == 'P':

                # 由于对数运算改变了电流的变化率，所以不能用电流来定位摆幅电压，需要用取对数后的电流值来定位
                dI_log_dV = np.gradient(Ids_log, Vgs)  # 计算Ids对Vgs的导数的绝对值
                dI_log_dV_selected = dI_log_dV[np.logical_and(Vgs >= Vgs_start, Vgs <= Vgs_end)]  # 获取评估范围内的数据索引
                dI_log_dV_min = np.min(dI_log_dV_selected)  # 获取最小值

                V_swing = Vgs[np.where(dI_log_dV == dI_log_dV_min)][0]  # 获取摆幅电压

                # 获取评估范围内的数据索引
                index_selected = np.where(np.logical_and(Vgs >= V_swing-V_FullWidth, Vgs <= V_swing))  # 防止取到沟道反型点
                Vgs_selected = Vgs[index_selected]  # 获取评估范围内的Vgs数据
                Ids_log_selected = Ids_log[index_selected]  # 获取评估范围内的Ids数据

                SS = -np.gradient(Vgs_selected, Ids_log_selected)  # 对于P型器件，Ids随Vgs增大而减小，所以需要加负号

            elif self.channel_type == 'N':
                dI_log_dV = np.gradient(Ids_log, Vgs)  # 计算Ids对Vgs的导数的绝对值
                dI_log_dV_selected = dI_log_dV[np.logical_and(Vgs >= Vgs_start, Vgs <= Vgs_end)]  # 获取评估范围内的数据索引
                dI_log_dV_min = np.max(dI_log_dV_selected)  # 与P型器件不同，N型器件Ids随Vgs增大而增大，所以取最大值

                V_swing = Vgs[np.where(dI_log_dV == dI_log_dV_min)][0]  # 获取摆幅电压

                # 获取评估范围内的数据索引
                index_selected = np.where(np.logical_and(Vgs >= V_swing, Vgs <= V_swing + V_FullWidth))  # 防止取到沟道反型点
                Vgs_selected = Vgs[index_selected]  # 获取评估范围内的Vgs数据
                Ids_log_selected = Ids_log[index_selected]  # 获取评估范围内的Ids数据

                SS = np.gradient(Vgs_selected, Ids_log_selected)  # 对于N型器件，Ids随Vgs增大而增大，所以不需要加负号

            else:
                raise ValueError('Invalid channel type, please choose from "P" or "N"')

            SS_list.append(np.mean(SS))  # 计算平均值
            V_swing_list.append(V_swing)  # 存储摆幅电压

        return SS_list, V_swing_list

if __name__ == '__main__':
    # 数据路径
    # data_directory = 'E:/Projects/Jingfang Pei/CNT-ASIC (CASIC)/Exp data/20241004 tft hfo2 40x25'  # MMW405
    data_directory = 'E:/Projects/Jingfang Pei/CASIC (CNT ASIC)/Exp data/20241004 tft hfo2 40x25'  # JinDiMingJin
    data_file = 'line_11#1_to_20.xls'

    # 获取数据
    data = GetData_KEITHLEY4200_OldModel(f'{data_directory}/{data_file}')

    example_data = data[6]  # 选择第一个数据作为测试对象

    # 实例化晶体管特性对象
    mem_TFT = MemTransistorCharacteristics(example_data, channel_type='P', analysis_subject='I_drain')

    # 获取转移曲线数据
    forward_sweep, backward_sweep = mem_TFT.TransferCurve()
    Vgs_forward, Id_forward, Is_forward, Ig_forward = forward_sweep
    Vgs_backward, Id_backward, Is_backward, Ig_backward = backward_sweep

    # 分析模块
    # 分析参数
    window_size = 5

    leakage = mem_TFT.LeakageCurrent()  # 漏电流
    on_off_ratio_Extremum = mem_TFT.OnOffRatio_Extremum()  # 开关比
    on_off_ratio = mem_TFT.OnOffRatio(on_region=(-8,-7), off_region=(7,8))  # 开关比

    # 阈值电压
    Vth, dI_dV, d2I_dV2 = mem_TFT.ThresholdVoltage(Vgs_forward, Id_forward, window_size=window_size, evaluation_range=(-7,8))

    # 检视曲线
    plt.plot(Vgs_forward, Id_forward, label='forward_sweep')
    plt.plot(Vgs_backward, Is_backward, label='backward_sweep')
    plt.legend(loc='best')
    plt.show(block=True)

    # 存储窗口
    memory_window = mem_TFT.MemoryWindow(window_size=window_size)
    # print(memory_window)

    # 亚阈值摆幅
    SS, V_swing, = mem_TFT.SubthresholdSwing(V_HalfWidth=0.2, window_size=5, evaluation_range=((-6,0),(4,7.5)))

    # 打印分析结果
    print(f'Leakage current: {leakage}')
    print(f'On-off ratio (Extremum): forward -> {"%e" % on_off_ratio_Extremum[0]}, backward -> {"%e" % on_off_ratio_Extremum[1]}')
    print(f'On-off ratio: forward -> {"%e" % on_off_ratio[0]}, backward -> {"%e" % on_off_ratio[1]}')
    print(f'Threshold voltage: {Vth}')
    print(f'Memory window: {memory_window}')
    print(f'Subthreshold swing: forward -> {SS[0]}, backward -> {SS[1]}')
    print(f'Swing voltage: forward -> {V_swing[0]}, backward -> {V_swing[1]}')

    # 可视化模块 - log scale
    plt.plot(Vgs_forward, Id_forward, label='forward_sweep')
    plt.plot(Vgs_backward, Is_backward, label='backward_sweep')
    # plt.plot(Vgs_forward, test_data[0], label='forward_sweep_deriv')
    # plt.plot(Vgs_backward, test_data[1], label='backward_sweep_deriv')

    # plt.legend(loc='best')
    plt.yscale('log')
    plt.show(block=True)