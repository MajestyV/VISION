# 此代码专用于分析KEITHLEY4200测得的晶体管的数据

import numpy as np
import matplotlib.pyplot as plt
from src.Visual_for_ElectronicEngineering.KEITHLEY4200_GetData import GetData_KEITHLEY4200_OldModel  # 数据读取函数

# 通过定义一个字典，方便地将缩写转换为全称
abbrev_dict = {'t': 'Time', 'Gm': 'GM',
               'V_g': 'GateV', 'V_d': 'DrainV', 'V_s': 'SourceV', 'I_g': 'GateI', 'I_d': 'DrainI', 'I_s': 'SourceI'}

class TransistorCharacteristics:
    '''
    此函数类专用于分析晶体管特性
    '''
    def __init__(self, data: dict, channel_type: str='P',
                 sweep_mode: str='DualSweep', characteristic: str='Transfer', **kwargs):
        '''
        初始化函数
        DataFrame类型的变量可以看作字典，详情请参考：
        https://www.quora.com/Are-there-advantages-of-Python-dictionaries-over-Pandas-dataframes#:~:text=A%20dictionary%20is%20a%20collection,%2C%20an%20array%2Dlike%20structure.
        '''

        # 从数据字典中获取数据
        V_g = data[abbrev_dict['V_g']]
        V_d = data[abbrev_dict['V_d']]
        # V_s = data[abbrev_dict['V_s']]

        I_g = data[abbrev_dict['I_g']]
        I_d = data[abbrev_dict['I_d']]
        # I_s = data[abbrev_dict['I_s']]
        I_s = np.abs(data[abbrev_dict['I_s']])  # 取绝对值

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

    def SubthresholdSwing(self):
        '''
        计算亚阈值摆幅，详见：https://en.wikipedia.org/wiki/Subthreshold_swing
        公式参考：chrome-extension://oemmndcbldboiebfnladdacbdfmadadm/https://hal.science/hal-03368147/document
        '''

        Ids_log = np.log10(self.I_s)
        Vgs = self.V_g

        # 利用numpy的梯度函数计算各点导数，详见：https://numpy.org/doc/stable/reference/generated/numpy.gradient.html
        SS = np.gradient(Vgs, Ids_log)

        return Vgs, SS





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
    Vgs, SS = transistor.SubthresholdSwing()
    print(SS)

    # 可视化模块
    # plt.plot(V_g, I_d, label='Transfer')
    # plt.plot(V_g, I_g, label='Leakage')
    plt.plot(Vgs, SS, label='SS')

    plt.xlim(0.5,1.0)
    plt.ylim(0,-2)

    plt.legend(loc='best')

    plt.show(block=True)