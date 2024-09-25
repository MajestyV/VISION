import os
import argparse
import numpy as np
from KEITHLEY4200_GetData import GetData_KEITHLEY4200_OldModel  # 数据读取模块
from KEITHLEY4200_Analysis import TransistorCharacteristics     # 数据分析模块


import seaborn as sns
import matplotlib.pyplot as plt

# 通过定义一个字典，方便地将缩写转换为全称
# abbrev_dict = {'t': 'Time', 'Gm': 'GM',
               # 'V_g': 'GateV', 'V_d': 'DrainV', 'V_s': 'SourceV', 'I_g': 'GateI', 'I_d': 'DrainI', 'I_s': 'SourceI'}

class DeviceStatistics:
    '''
    此类专用于统计器件特性
    '''

    def __init__(self, data_directory: str, scaling_factor: float=1e3):
        '''
        初始化函数类
        '''

        self.data_directory = data_directory  # 数据文件夹

        self.scaling_factor = scaling_factor  # 缩放因子，用于单位变换(默认为1e3)
        self.scaling_dict = {'m': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15, 'a': 1e-18}  # 缩放字典

        self.data_dict = dict()  # 数据字典 （设置为实例变量，方便在函数类中调用）

    def Analysis(self, mode: str, ON_range: tuple, OFF_range: tuple, SS_range: tuple, Vth_location: tuple) -> tuple:
        '''
        分析函数
        '''

        if mode == 'auto':  # 自动模式: 在这个模式下，不需要指定文件名，只需要指定文件夹，程序会自动读取文件夹下的所有文件中的数据
            file_list = os.listdir(self.data_directory)
            num_files = len(file_list)  # 计算数据文件的数量
            example_data = GetData_KEITHLEY4200_OldModel(data_file=f"{self.data_directory}/{file_list[0]}")
            num_cycles = len(example_data)  # 计算测试循环次数，即数据列表的长度

            # 创建一系列全零数组，用于存储数据
            SS_map = np.zeros((num_files, num_cycles), dtype=float)  # SS - Subthreshold Swing (亚阈值摆幅)
            on_off_ratio_map = np.zeros((num_files, num_cycles), dtype=float)  # 开关比
            on_off_ratio_extreme_map = np.zeros((num_files, num_cycles), dtype=float)  # 开关比（极端值）
            leakage_avg_map = np.zeros((num_files, num_cycles), dtype=float)  # 平均漏电流
            Vth_map = np.zeros((num_files, num_cycles), dtype=float)  # 阈值电压

            for i in range(num_files):
                data = GetData_KEITHLEY4200_OldModel(data_file=f"{self.data_directory}/{file_list[i]}")

                for j in range(num_cycles):
                    transistor = TransistorCharacteristics(data=data[j])  # 创建一个晶体管特性对象
                    Vgs, Id, Is, Ig = transistor.TransferCurve()  # 获取传输曲线
                    on_off_ratio = transistor.OnOffRatio(ON_range, OFF_range)  # 计算开关比
                    on_off_ratio_extreme = transistor.OnOffRatio_Extreme()  # 计算开关比（极端值）
                    SS = transistor.SubthresholdSwing(SS_range)  # 计算亚阈值摆幅
                    leakage_avg = transistor.LeakageCurrent()  # 计算平均漏电流
                    Vth, dI_dV, d2I_dV2 = transistor.ThresholdVoltage(Vth_location)  # 计算阈值电压

                    # 存储数据
                    SS_map[i, j] = SS  # 亚阈值摆幅
                    on_off_ratio_map[i, j] = on_off_ratio  # 开关比
                    on_off_ratio_extreme_map[i, j] = on_off_ratio_extreme  # 开关比（极端值）
                    leakage_avg_map[i, j] = leakage_avg  # 平均漏电流
                    Vth_map[i, j] = Vth  # 阈值电压

        else:
            raise ValueError('Invalid mode! Please select a valid mode parameter: "single" or "multiple" ! ! !')

        # 统计的器件数目信息
        self.data_dict['num_cycles'] = num_cycles
        self.data_dict['num_files'] = num_files
        # 将数据保存到实例变量字典中方便外部调用
        self.data_dict['SS_map'] = SS_map
        self.data_dict['on_off_ratio_map'] = on_off_ratio_map
        self.data_dict['on_off_ratio_extreme_map'] = on_off_ratio_extreme_map
        self.data_dict['leakage_avg_map'] = leakage_avg_map
        self.data_dict['Vth_map'] = Vth_map

        return SS_map, on_off_ratio_map, on_off_ratio_extreme_map, leakage_avg_map, Vth_map

    def Heatmap(self, character: str, data: np.ndarray, title: str, xlabel: str, ylabel: str, xtick: np.ndarray, ytick: np.ndarray, cmap: str, cbar_label: str):
        '''
        热力图 （关于seaborn的设置，参考：https://blog.csdn.net/weixin_45492560/article/details/106227864）

        '''
        # fig = sns.heatmap(data, annot=True, fmt='.1f', cmap=cmap,
                          # cbar_kws={'label': cbar_label})
        # fig.set(xlabel=xlabel, ylabel=ylabel, xticklabels=xtick, yticklabels=ytick)

        # 开关比 (ON-OFF ratio)
        if character == 'ON_OFF_ratio':
            data = self.data_dict['on_off_ratio_map']  # 提取实例变量字典中的数据
            # 关于倍频得讨论：https: // blog.csdn.net / cabbage2008 / article / details / 52043646
            fig = sns.heatmap(20*np.log10(data), annot=True, fmt='.1f', cmap='magma', vmin=0, vmax=100,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(<I_{on}>/<I_{off}>)$ (dB)'})

        # 极限开关比
        elif character == 'ON_OFF_ratio_extreme':
            data = self.data_dict['on_off_ratio_extreme_map']
            fig = sns.heatmap(20 * np.log10(data), annot=True, fmt='.1f', cmap='magma', vmin=0, vmax=100,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(<I_{on}>/<I_{off}>)$ (dB)'})

        # 亚阈值摆幅（Subthreshold Swing）
        elif character == 'SS'
            data = self.data_dict['SS_map']*self.scaling_factor

            fig = sns.heatmap(data, annot=True, fmt='.0f', cmap='coolwarm',
                              cbar_kws={'label': 'Subthreshold Swing (mV/decade)'})

        else:
            raise ValueError('Invalid character! Please select a valid character parameter ! ! !')

        # sns.heatmap(np.log10(on_off_ratio_extreme_map), annot=True, fmt='.1f', cmap='coolwarm', cbar_kws={'label': 'On-Off Ratio'})
        # sns.heatmap(leakage_avg_map)
        # sns.heatmap(SS_map*1e3, annot=True, fmt='.0f', cmap='coolwarm', cbar_kws={'label': 'Subthreshold Swing (mV/decade)'})
        # plt.savefig('./data/46/seaborn_heatmap_list.png')
        # plt.close('all')

        xtick = np.arange(1, num_cycles+1, 1)  # 生成x轴刻度（从1开始）
        ytick = np.arange(1, num_files+1, 1)   # 生成y轴刻度（从1开始）
        # fig.set(xlabel='Column number', ylabel='Row number', xticklabels=xtick, yticklabels=ytick)  # 各种画图设置

        # cbar = fig.collections[0].colorbar  # 设置colorbar

        # fig.set_xlabel('Cycle')
        # fig.set_ylabel('File')
        # fig.set_xticklabels('On-Off Ratio')





if __name__ == '__main__':

    # 可视化模块

    # print(leakage_avg_map)

    scaling_factor = 1e3  # 缩放因子

    plt.figure()

    # 热力图



    # 统计分布图

    # 漏电流
    leakage_avg = leakage_avg_map.flatten()  # 将二维数组展平为一维数组
    fig = sns.displot(leakage_avg, kde=True, bins=100, color='red', rug=True, log_scale=10)
    fig.set(xlabel = 'Leakage current $I_{gs}$ (A)', xlim = (1e-12, 5e-8))

    # 阈值电压
    # Vth = Vth_map.flatten()  # 将二维数组展平为一维数组
    # fig = sns.displot(Vth, kde=True, bins=20, color='blue', rug=True)
    # fig.set(xlabel = 'Threshold voltage $V_{th}$ (V)', xlim = (0.1, 0.8))

    # sns.displot(leakage_avg*scaling_factor, kde=True, bins=20, color='blue', rug=True)
    # sns.displot(data=leakage_avg, x="bill_length_mm", kind='kde')
    # sns.displot(data=leakage_avg, x="bill_length_mm", kind='ecdf')

    plt.tight_layout()  # 调整布局

    # 保存图像
    plt.savefig(args.saving_directory + '/Untitled.png')

    plt.show(block=True)

    exit()