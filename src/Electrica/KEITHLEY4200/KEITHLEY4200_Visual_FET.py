import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 函数包内直接调用提高运行效率
from src.Basic import Select_files_by_extension
from src.Electrica.KEITHLEY4200 import GetData_KEITHLEY4200A_SCS

# 通过定义一个字典，方便地将缩写转换为全称
abbrev_dict = {'t': 'Time', 'Gm': 'GM',
               'V_g': 'GateV', 'V_d': 'DrainV', 'V_s': 'SourceV',
               'I_g': 'GateI', 'I_d': 'DrainI', 'I_s': 'SourceI',
               'I_gate': 'GateI', 'I_drain': 'DrainI', 'I_source': 'SourceI'}

class Visual_Transistor:
    ''' 此函数类专用于快速可视化大量晶体管的测试数据，以辅助后续分析 '''
    def __init__(self, **kwargs):
        ''' 初始化函数类 '''

        # 定义可变参数的默认值
        self.mode = kwargs['mode'] if 'mode' in kwargs else 'auto'  # 可视化模式
        self.data_directory = kwargs['data_directory'] if 'data_directory' in kwargs else None  # 数据文件夹
        self.data_file_list = kwargs['data_file_list'] if 'data_file_list' in kwargs else None  # 数据文件列表
        self.data_file_extension = kwargs['data_file_extension'] if 'data_file_extension' in kwargs else 'xls'  # 数据文件扩展名

        if self.mode == 'auto':  # 自动模式: 在这个模式下，不需要指定文件名，只需要指定文件夹，程序会自动读取文件夹下的所有数据文件中的数据
            self.data_file_list = Select_files_by_extension(self.data_directory, self.data_file_extension, returning_absolute_path=True)
        elif self.mode == 'manual':  # 手动模式: 在这个模式下，需要指定文件名列表
            pass
        else:
            raise ValueError('Invalid mode, please choose from "auto" or "manual" !')  # 报错

        self.num_files = len(self.data_file_list)  # 计算数据文件的数量
        self.num_cycles = len(GetData_KEITHLEY4200A_SCS(data_file=self.data_file_list[0]))  # 计算每个文件中的测试循环次数，即数据列表的长度

        # 读取数据文件，生成数据列表，每个测试循环的数据都储存在一个DataFrame中
        self.data_list = [GetData_KEITHLEY4200A_SCS(data_file=self.data_file_list[i]) for i in range(self.num_files)]

    def TransferCurve(self, plotting_subject: str='I_drain', figsize: tuple[float,float]=(8., 6.),
                      color_current: str='blue', color_leakage: str='red', log_scale: bool=False,
                      showing_leakage: bool=False) -> None:
        ''' 可视化转移特性 '''

        current_abbrev = abbrev_dict[plotting_subject]  # 获取电流对象缩写

        plt.figure(figsize=figsize)  # 创建画布
        # 遍历所有数据文件
        for i in range(self.num_files):
            for j in range(self.num_cycles):

                data = self.data_list[i][j]
                Vgs, I, Ig = data[abbrev_dict['V_g']].values, data[current_abbrev].values, data[abbrev_dict['I_g']].values

                if log_scale:  # 如果需要对数坐标, 则需要对电流取绝对值
                    I, Ig = np.abs(I), np.abs(Ig)

                plt.plot(Vgs, I, color=color_current)

                if showing_leakage:
                    plt.plot(Vgs, Ig, color=color_leakage)

        # 图画设置
        plt.xlabel('Gate bias')
        plt.ylabel(plotting_subject)

        if log_scale:
            plt.yscale('log')

        return

    def SavingFig(self, saving_directory: str, figure_name: str='untitled', fmt: str or list or tuple=('png','pdf','eps'),
                  dpi: int=300) -> None:
        ''' 保存图像 '''
        if isinstance(fmt, str):
            plt.savefig(f'{saving_directory}/{figure_name}.{fmt}', format=fmt, dpi=dpi)
        else:
            for format in fmt:
                plt.savefig(f'{saving_directory}/{figure_name}.{format}', format=format, dpi=dpi)
        return

if __name__ == '__main__':
    data_directory = 'E:/PhD_research/Jingfang Pei/Solution-processed IC/Data/KEITHLEY4200/20250323 sol ic 5x20_preview/1_to_10_then_11_to_20_separated'
    saving_directory = 'E:/PhD_research/Jingfang Pei/Solution-processed IC/Data/KEITHLEY4200/Working_dir'

    visual = Visual_Transistor(mode='auto', data_directory=data_directory)

    visual.TransferCurve(log_scale=True)

    visual.SavingFig(saving_directory=saving_directory, figure_name='TransferCurve')

    plt.show(block=True)

