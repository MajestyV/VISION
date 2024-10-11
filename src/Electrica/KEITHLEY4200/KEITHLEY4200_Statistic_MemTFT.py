import os
import numpy as np
import pandas as pd
from scipy.ndimage import label

# 导入数据读取模块
from src.Electrica.KEITHLEY4200.KEITHLEY4200_GetData import GetData_KEITHLEY4200_OldModel
# 从KEITHLEY4200数据中提取忆阻晶体管特性的函数
from src.Electrica.KEITHLEY4200.KEITHLEY4200_Analysis_MemTFT import MemTransistorCharacteristics

# 导入绘图模块
import seaborn as sns
import matplotlib.pyplot as plt

class MemTransistorStatistics:
    '''
    此类专用于统计器件特性
    '''

    def __init__(self, data_directory: str, voltage_unit: str='V', current_unit: str='A'):
        '''
        初始化函数类
        '''

        self.data_directory = data_directory  # 数据文件夹

        self.voltage_unit = voltage_unit  # 电压单位
        self.current_unit = current_unit  # 电流单位

        # 缩放字典
        self.scaling_dict = {'nA': 1e9, 'uA': 1e6, 'mA': 1e3, 'A': 1.0, 'kA': 1e-3, 'MA': 1e-6, 'GA': 1e-9,
                             'nV': 1e9, 'uV': 1e6, 'mV': 1e3, 'V': 1.0, 'kV': 1e-3, 'MV': 1e-6, 'GV': 1e-9}
        self.voltage_scaling = self.scaling_dict[voltage_unit]  # 电压缩放因子
        self.current_scaling = self.scaling_dict[current_unit]  # 电流缩放因子

        self.data_dict = dict()  # 数据字典 （设置为实例变量，方便在函数类中调用）

    def Analysis(self, mode: str, channel_type: str, analysis_subject: str, ON_range: tuple, OFF_range: tuple,
                 V_FullWidth: float, window_size: int,  boundary_cond: str, Vth_eval_range: tuple, mem_eval_range: tuple,
                 SS_eval_range: tuple[tuple,tuple]) -> tuple:
        '''
        分析函数
        '''

        if mode == 'auto':  # 自动模式: 在这个模式下，不需要指定文件名，只需要指定文件夹，程序会自动读取文件夹下的所有文件中的数据
            file_list = os.listdir(self.data_directory)
            num_files = len(file_list)  # 计算数据文件的数量
            example_data = GetData_KEITHLEY4200_OldModel(data_file=f"{self.data_directory}/{file_list[0]}")
            num_cycles = len(example_data)  # 计算测试循环次数，即数据列表的长度

            # 创建一系列全零数组，用于存储数据
            leakage_avg_map = np.zeros((num_files, num_cycles), dtype=float)  # 平均漏电流
            on_off_ratio_map = np.zeros((num_files, num_cycles, 2), dtype=float)  # 开关比
            on_off_ratio_extremum_map = np.zeros((num_files, num_cycles,2), dtype=float)  # 开关比（极端值）
            Vth_map = np.zeros((num_files, num_cycles, 2), dtype=float)  # 阈值电压
            MemWindow_map = np.zeros((num_files, num_cycles), dtype=float)  # 存储窗口
            SS_map = np.zeros((num_files, num_cycles, 2), dtype=float)  # SS - Subthreshold Swing (亚阈值摆幅)
            V_swing_map = np.zeros((num_files, num_cycles, 2), dtype=float)  # 摆幅电压

            for i in range(num_files):
                data = GetData_KEITHLEY4200_OldModel(data_file=f"{self.data_directory}/{file_list[i]}")
                print(f"File {file_list[i]} is processing ...")

                for j in range(num_cycles):

                    # 实例化忆阻晶体管特性对象
                    mem_TFT = MemTransistorCharacteristics(data[j], channel_type=channel_type,
                                                           analysis_subject=analysis_subject)

                    # 获取转移曲线数据
                    forward_sweep, backward_sweep = mem_TFT.TransferCurve()
                    Vgs_forward, Id_forward, Is_forward, Ig_forward = forward_sweep  # 解压正向扫描数据
                    Vgs_backward, Id_backward, Is_backward, Ig_backward = backward_sweep  # 解压反向扫描数据

                    leakage = mem_TFT.LeakageCurrent()  # 漏电流
                    on_off_ratio_extremum = mem_TFT.OnOffRatio_Extremum()  # 开关比
                    on_off_ratio = mem_TFT.OnOffRatio(on_region=ON_range, off_region=OFF_range)  # 开关比

                    # 阈值电压
                    Vth_forward = mem_TFT.ThresholdVoltage(Vgs_forward, Id_forward, window_size, boundary_cond, Vth_eval_range)[0]
                    Vth_backward = mem_TFT.ThresholdVoltage(Vgs_backward, Id_backward, window_size, boundary_cond, Vth_eval_range)[0]

                    # 存储窗口
                    memory_window = mem_TFT.MemoryWindow(window_size, boundary_cond, mem_eval_range)

                    # 亚阈值摆幅
                    SS, V_swing = mem_TFT.SubthresholdSwing(V_FullWidth, window_size, boundary_cond, SS_eval_range)

                    # 存储数据
                    leakage_avg_map[i, j] = leakage  # 平均漏电流
                    on_off_ratio_map[i, j] = on_off_ratio  # 开关比
                    on_off_ratio_extremum_map[i, j] = on_off_ratio_extremum  # 开关比（极端值）
                    Vth_map[i, j] = (Vth_forward,Vth_backward)  # 阈值电压
                    MemWindow_map[i,j] = memory_window  # 储存窗口
                    SS_map[i, j] = SS  # 亚阈值摆幅
                    V_swing_map[i, j] = V_swing  # 摆幅电压

                    print(f"Cycle {j+1}/{num_cycles} is done ! ! !")

        else:
            raise ValueError('Invalid mode! Please select a valid mode parameter: "single" or "multiple" ! ! !')

        # 统计的器件数目信息
        self.data_dict['num_cycles'] = num_cycles
        self.data_dict['num_files'] = num_files
        # 将数据保存到实例变量字典中方便外部调用
        self.data_dict['leakage_avg_map'] = leakage_avg_map
        self.data_dict['on_off_ratio_map'] = on_off_ratio_map
        self.data_dict['on_off_ratio_extremum_map'] = on_off_ratio_extremum_map
        self.data_dict['Vth_map'] = Vth_map
        self.data_dict['MemWindow_map'] = MemWindow_map
        self.data_dict['SS_map'] = SS_map
        self.data_dict['V_swing_map'] = V_swing_map

        return leakage_avg_map, on_off_ratio_map, on_off_ratio_extremum_map, Vth_map, MemWindow_map, SS_map

    ####################################################################################################################
    # 以下是画图函数

    def Heatmap(self, character: str, figsize: tuple[float,float]=(12,8)) -> None:
        '''
        热力图 （关于seaborn的设置，参考：https://blog.csdn.net/weixin_45492560/article/details/106227864）
        '''
        plt.figure(figsize=figsize)  # 创建一个新的画布

        # 开关比 (ON-OFF ratio)
        if character == 'ON_OFF_ratio_forward':
            data = self.data_dict['on_off_ratio_map'][:,:,0]  # 提取实例变量字典中的数据
            # 关于倍频得讨论：https: // blog.csdn.net / cabbage2008 / article / details / 52043646
            fig = sns.heatmap(20*np.log10(data), annot=True, fmt='.1f', cmap='magma', vmin=0, vmax=100,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(<I_{on}>/<I_{off}>)$ (dB)'})
        elif character == 'ON_OFF_ratio_backward':
            data = self.data_dict['on_off_ratio_map'][:,:,1]
            fig = sns.heatmap(20 * np.log10(data), annot=True, fmt='.1f', cmap='magma', vmin=0, vmax=100,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(<I_{on}>/<I_{off}>)$ (dB)'})

        # 极限开关比
        elif character == 'ON_OFF_ratio_extremum_forward':
            data = self.data_dict['on_off_ratio_extremum_map'][:,:,0]
            fig = sns.heatmap(20 * np.log10(data), annot=True, fmt='.1f', cmap='magma', vmin=0, vmax=120,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(I_{max}/I_{min})$ (dB)'})
        elif character == 'ON_OFF_ratio_extremum_backward':
            data = self.data_dict['on_off_ratio_extremum_map'][:,:,1]
            fig = sns.heatmap(20 * np.log10(data), annot=True, fmt='.1f', cmap='magma', vmin=0, vmax=120,
                              cbar_kws={'label': r'$20 \cdot \log_{10}(I_{max}/I_{min})$ (dB)'})

        elif character == 'memory_window':
            data = self.data_dict['MemWindow_map']*self.voltage_scaling
            fig = sns.heatmap(data, annot=True, fmt='.1f', cmap='coolwarm',
                              cbar_kws={'label': f"Memory Window ({self.voltage_unit})"})

        # 亚阈值摆幅（Subthreshold Swing）
        elif character == 'SS_forward':  # 正向扫描
            data = self.data_dict['SS_map'][:,:,0]*self.voltage_scaling
            fig = sns.heatmap(data, annot=True, fmt='.0f', cmap='coolwarm', # vmin=0, vmax=2000,
                              cbar_kws={'label': f"Subthreshold Swing ({self.voltage_unit}/decade)"})
        elif character == 'SS_backward':  # 反向扫描
            data = self.data_dict['SS_map'][:,:,1]*self.voltage_scaling
            fig = sns.heatmap(data, annot=True, fmt='.0f', cmap='coolwarm', # vmin=0, vmax=2000,
                              cbar_kws={'label': f"Subthreshold Swing ({self.voltage_unit}/decade)"})

        else:
            raise ValueError('Invalid character! Please select a valid character parameter ! ! !')

        # 各种画图设置
        xtick = np.arange(1, self.data_dict['num_cycles']+1, 1)  # 生成x轴刻度（从1开始）
        ytick = np.arange(1, self.data_dict['num_files']+1, 1)   # 生成y轴刻度（从1开始）
        fig.set(xlabel='Column number', ylabel='Row number', xticklabels=xtick, yticklabels=ytick)

        plt.tight_layout()  # 调整布局

        return

    def Distribution(self, character: str) -> None:
        '''
        统计分布图
        '''
        plt.figure()  # 创建一个新的画布

        # 漏电流
        if character == 'leakage':
            data = self.data_dict['leakage_avg_map'].flatten()*self.current_scaling  # 将二维数组展平为一维数组，然后缩放数据
            fig = sns.displot(data, kde=True, bins=50, color='red', rug=True, log_scale=10)
            fig.set(xlabel='Leakage current $I_{gs}$ ('+self.current_unit+')', xlim=(1e-12, 1e-7))

        # 阈值电压 (Threshold voltage)
        elif character == 'Vth':
            Vth_forward = self.data_dict['Vth_map'][:,:,0].flatten()*self.voltage_scaling  # 将二维数组展平为一维数组，然后缩放数据
            Vth_backward = self.data_dict['Vth_map'][:,:,1].flatten()*self.voltage_scaling

            Vth_dict = {'sweep': [], 'Vth': []}
            for Vth in Vth_forward:
                Vth_dict['sweep'].append('forward')
                Vth_dict['Vth'].append(Vth)
            for Vth in Vth_backward:
                Vth_dict['sweep'].append('backward')
                Vth_dict['Vth'].append(Vth)
            Vth_DF = pd.DataFrame(Vth_dict)

            fig = sns.displot(Vth_DF, x='Vth', hue='sweep', kde=True, bins=50, rug=True, legend=False)

            fig.set(xlabel = 'Threshold voltage $V_{th}$ ('+self.voltage_unit+')', xlim = (-8, 8))

        else:
            raise ValueError('Invalid character! Please select a valid character parameter ! ! !')

        plt.tight_layout()  # 调整布局

        return

if __name__ == '__main__':
    pass