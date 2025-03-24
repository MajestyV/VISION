import os
import numpy as np
from src.Electrica.KEITHLEY4200.KEITHLEY4200_GetData import GetData_KEITHLEY4200A_SCS  # 数据读取模块
from src.Electrica.KEITHLEY4200.KEITHLEY4200_Analysis_FET import Characteristics_Transistors     # 数据分析模块

import seaborn as sns
import matplotlib.pyplot as plt

class Statistics_Transistor:
    ''' 此类专用于统计器件特性 '''
    def __init__(self, data_directory: str, voltage_unit: str='V', current_unit: str='A'):
        ''' 初始化函数类 '''

        self.data_directory = data_directory  # 数据文件夹

        self.voltage_unit = voltage_unit  # 电压单位
        self.current_unit = current_unit  # 电流单位

        # 缩放字典
        self.scaling_dict = {'nA': 1e9, 'uA': 1e6, 'mA': 1e3, 'A': 1.0, 'kA': 1e-3, 'MA': 1e-6, 'GA': 1e-9,
                             'nV': 1e9, 'uV': 1e6, 'mV': 1e3, 'V': 1.0, 'kV': 1e-3, 'MV': 1e-6, 'GV': 1e-9}
        self.voltage_scaling = self.scaling_dict[voltage_unit]  # 电压缩放因子
        self.current_scaling = self.scaling_dict[current_unit]  # 电流缩放因子

        self.data_dict = dict()  # 数据字典 （设置为实例变量，方便在函数类中调用）

    def Analysis(self, mode: str, ON_range: tuple, OFF_range: tuple, SS_range: tuple, Vth_location: tuple) -> tuple:
        '''
        分析函数
        '''

        if mode == 'auto':  # 自动模式: 在这个模式下，不需要指定文件名，只需要指定文件夹，程序会自动读取文件夹下的所有文件中的数据
            file_list = os.listdir(self.data_directory)
            num_files = len(file_list)  # 计算数据文件的数量
            example_data = GetData_KEITHLEY4200A_SCS(data_file=f"{self.data_directory}/{file_list[0]}")
            num_cycles = len(example_data)  # 计算测试循环次数，即数据列表的长度

            # 创建一系列全零数组，用于存储数据
            SS_map = np.zeros((num_files, num_cycles), dtype=float)  # SS - Subthreshold Swing (亚阈值摆幅)
            on_off_ratio_map = np.zeros((num_files, num_cycles), dtype=float)  # 开关比
            on_off_ratio_extreme_map = np.zeros((num_files, num_cycles), dtype=float)  # 开关比（极端值）
            leakage_avg_map = np.zeros((num_files, num_cycles), dtype=float)  # 平均漏电流
            Vth_map = np.zeros((num_files, num_cycles), dtype=float)  # 阈值电压

            for i in range(num_files):
                data = GetData_KEITHLEY4200A_SCS(data_file=f"{self.data_directory}/{file_list[i]}")

                for j in range(num_cycles):
                    transistor = Characteristics_Transistors(data=data[j])  # 创建一个晶体管特性对象
                    Vgs, Id, Is, Ig = transistor.TransferCurve()  # 获取传输曲线
                    on_off_ratio = transistor.OnOffRatio(ON_range, OFF_range)  # 计算开关比
                    on_off_ratio_extreme = transistor.OnOffRatio_Extreme()  # 计算开关比（极端值）
                    SS = transistor.SubthresholdSwing(evaluation_range=SS_range)  # 计算亚阈值摆幅
                    leakage_avg = transistor.LeakageCurrent()  # 计算平均漏电流
                    Vth, dI_dV, d2I_dV2 = transistor.ThresholdVoltage(Vth_location=Vth_location)  # 计算阈值电压

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

    ####################################################################################################################
    # 以下是画图函数

    def Heatmap(self, character: str, annot: bool=True) -> None:
        '''
        热力图 （关于seaborn的设置，参考：https://blog.csdn.net/weixin_45492560/article/details/106227864）
        '''
        plt.figure()  # 创建一个新的画布

        # 开关比 (ON-OFF ratio)
        if character == 'ON_OFF_ratio':
            data = self.data_dict['on_off_ratio_map']  # 提取实例变量字典中的数据
            # 关于倍频得讨论：https: // blog.csdn.net / cabbage2008 / article / details / 52043646
            fig = sns.heatmap(20*np.log10(data), annot=annot, fmt='.1f', cmap='magma', vmin=0, vmax=100,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(<I_{on}>/<I_{off}>)$ (dB)'})

        # 极限开关比
        elif character == 'ON_OFF_ratio_extreme':
            data = self.data_dict['on_off_ratio_extreme_map']
            fig = sns.heatmap(20 * np.log10(data), annot=annot, fmt='.1f', cmap='magma', vmin=0, vmax=100,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(<I_{on}>/<I_{off}>)$ (dB)'})

        # 亚阈值摆幅（Subthreshold Swing）
        elif character == 'SS':
            data = self.data_dict['SS_map']*self.voltage_scaling
            fig = sns.heatmap(data, annot=annot, fmt='.0f', cmap='coolwarm', vmin=0, vmax=1000,
                              cbar_kws={'label': f"Subthreshold Swing ({self.voltage_unit}/decade)"})
            # 记得要修改画图范围

        else:
            raise ValueError('Invalid character! Please select a valid character parameter ! ! !')

        # 各种画图设置
        xtick = np.arange(1, self.data_dict['num_cycles']+1, 1)  # 生成x轴刻度（从1开始）
        ytick = np.arange(1, self.data_dict['num_files']+1, 1)   # 生成y轴刻度（从1开始）
        fig.set(xlabel='Column number', ylabel='Row number', xticklabels=xtick, yticklabels=ytick)

        plt.tight_layout()  # 调整布局

        return

    def Distribution(self, character: str, plotting_range: tuple[float,float]) -> None:
        '''
        统计分布图
        '''
        plt.figure()  # 创建一个新的画布

        # 漏电流
        if character == 'Igs':
            data = self.data_dict['leakage_avg_map'].flatten()*self.current_scaling  # 将二维数组展平为一维数组，然后缩放数据
            fig = sns.displot(data, kde=True, bins=100, color='red', rug=True, log_scale=10)
            fig.set(xlabel='Leakage current $I_{gs}$ ('+self.current_unit+')', xlim=plotting_range)

        # 阈值电压 (Threshold voltage)
        elif character == 'Vth':
            data = self.data_dict['Vth_map'].flatten()*self.voltage_scaling  # 将二维数组展平为一维数组，然后缩放数据
            fig = sns.displot(data, kde=True, bins=20, color='blue', rug=True)
            fig.set(xlabel = 'Threshold voltage $V_{th}$ ('+self.voltage_unit+')', xlim=plotting_range)

        else:
            raise ValueError('Invalid character! Please select a valid character parameter ! ! !')

        plt.tight_layout()  # 调整布局

        return

if __name__ == '__main__':
    pass