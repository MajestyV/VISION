# 有时pycharm的文件结构和cmd的文件结构不一样，在cmd中运行会显示：ModuleNotFoundError: No module named 'src'
# 这可以通过在脚本开头添加项目根目录到sys.path中解决，详情请参考：https://blog.csdn.net/qq_42730750/article/details/119799157
import os
import sys
project_path = os.path.abspath(os.path.join(os.getcwd(), '..'))  # 项目根目录
sys.path.append(project_path)  # 添加路径到系统路径中

import argparse
from src import Electrica
import matplotlib.pyplot as plt

working_loc = 'CentraHorizon'             # 默认工作地点

# 默认的数据文件目录字典
data_dir_dict = {'Macbook': '/Users/liusongwei/Desktop/SolutionIC_Temporary/Data/RO',
                 'MMW405': 'E:/Projects/Jingfang Pei/CNT-ASIC (CASIC)/Exp data/20241004 tft hfo2 40x25',
                 'JCPGH1': 'D:/Projects/Jingfang Pei/Solution-processed IC/Data/4200/20240923 tft 20x20 array glass substrate',
                 'JinDiMingJin': 'E:/Projects/Jingfang Pei/CASIC (CNT ASIC)/Exp data/20241004 tft hfo2 40x25_selected',
                 'Lingjiang': 'E:/PhD_research/Jingfang Pei/CNT-ASIC (CASIC)/Exp data/20241004 tft hfo2 40x25',
                 'CentraHorizon': 'D:/Projects/Jingfang Pei/CNT-ASIC (CASIC)/Exp data/20x20 Data for stastistical TPU/data'}

# 默认的数据保存目录字典
saving_dir_dict = {'MMW405': 'E:/Projects/Jingfang Pei/CNT-ASIC (CASIC)/Exp data/Working_dir',
                   'JCPGH1': 'C:/Users/13682/OneDrive/桌面/Temporary_data/SolutionIC_glass',
                   'JinDiMingJin': 'E:/Projects/Jingfang Pei/CASIC (CNT ASIC)/Exp data/Working_dir',
                   'Lingjiang': 'E:/PhD_research/Jingfang Pei/CNT-ASIC (CASIC)/Exp data/Working_dir',
                   'CentraHorizon': 'D:/Projects/Jingfang Pei/CNT-ASIC (CASIC)/Exp data/20x20 Data for stastistical TPU/demo'}

def InitializeParser() -> argparse.Namespace:
    ''' 初始化命令行解析器, 并返回解析器对象 '''

    parser = argparse.ArgumentParser()  # 加载命令行解析器

    # 数据文件路径以及分析结果保存路径
    parser.add_argument('--data_directory', metavar='-P', type=str, default=data_dir_dict[working_loc], help='Data directory')  # 数据文件夹
    parser.add_argument('--saving_directory', metavar='-S', type=str, default=saving_dir_dict[working_loc], help='Saving directory')  # 分析结果保存文件夹

    # 基础设置
    parser.add_argument('-V_unit', '--voltage_unit', metavar='-V', type=str, default='V', help='Voltage unit')  # 电压单位
    parser.add_argument('-I_unit', '--current_unit', metavar='-I', type=str, default='A', help='Current unit')  # 电流单位

    # 统计分析参数
    parser.add_argument('--mode', metavar='-M', type=str, default='auto', help='Analysis mode')  # 分析模式
    parser.add_argument('--channel_type', metavar='-C', type=str, default='P', help='Channel type')  # 通道类型
    parser.add_argument('--analysis_subject', metavar='-A', type=str, default='I_drain', help='Analysis subject')  # 分析对象

    parser.add_argument('--ON_range', metavar='-ON', type=tuple, default=(-8, -7), help='ON range')  # ON范围
    parser.add_argument('--OFF_range', metavar='-OFF', type=tuple, default=(7, 8), help='OFF range')  # OFF范围
    # parser.add_argument('--SS_range', metavar='-SS', type=tuple, default=(0.25, 0.3), help='SS range')  # SS范围

    parser.add_argument('--V_FullWidth', metavar='-V_FullWidth', type=float, default=1.0, help='V FullWidth')  # 摆幅电压衡量区间全宽度
    parser.add_argument('--window_size', metavar='-W', type=int, default=5, help='Window size')  # 窗口大小
    parser.add_argument('--boundary_cond', metavar='-B', type=str, default='same', help='Boundary condition')  # 边界条件
    parser.add_argument('--Vth_eval_range', metavar='-Vth', type=tuple, default=(-6,8), help='Vth evaluation range')  # 阈值电压评估范围
    parser.add_argument('--mem_eval_range', metavar='-Mem', type=tuple, default=(-6,8), help='Memory evaluation range')  # 存储评估范围
    parser.add_argument('--SS_eval_range', metavar='-SS', type=tuple, default=((-6,0), (4,7.5)), help='SS evaluation range')  # SS评估范围

    # parser.add_argument('--Vth_location', metavar='-Vth', type=tuple, default=(0.2, 0.6), help='Vth location')  # 阈值电压位置

    # 分析指标设置
    heatmap_defualt = ['ON_OFF_ratio_forward', 'ON_OFF_ratio_backward', 'ON_OFF_ratio_extremum_forward',
                       'ON_OFF_ratio_extremum_backward',
                       'memory_window',
                       'SS_forward', 'SS_backward']
    distribution_default = ['leakage', 'Vth']

    parser.add_argument('--heatmap', metavar='-H', type=tuple, nargs='+', default=heatmap_defualt, help='Heatmap')  # 热图
    parser.add_argument('--distribution', metavar='-D', type=tuple, nargs='+', default=distribution_default,
                        help='Distribution')  # 分布图
    # 绘图参数
    # argumentParser() 存储bool类型有坑，不能直接传True/False，需要设置action
    # python 终端读取时传入的都是string类型，转为bool型时，由于是非空字符串，所以（无论传入什么字符均）转为True
    # 详情请参考：
    # https://blog.csdn.net/qinduohao333/article/details/131305803
    # https://blog.csdn.net/orangeOrangeRed/article/details/117624905?login=from_csdn
    parser.add_argument('-AN', '--annot', action='store_true', help='Annotation on the heatmap')  # 是否标注
    parser.add_argument('-CM', '--colormap', metavar='colormap', type=str, default='viridis', help='Colormap of the heatmap')  # 色图
    parser.add_argument('-CM_source', '--colormap_source', metavar='colormap source', type=str, default='default', help='Source of the colormap')  # 色图来源

    # 图像保存参数
    # parser.add_argument('--format', metavar='-F', type=str or tuple, default='png', help='Figure format')  # 图像保存格式
    parser.add_argument('-F', '--format', metavar='format', type=tuple, default=('png','eps', 'pdf'), help='Formats of the figures to be saved')  # 图像保存格式

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = InitializeParser()  # 初始化命令行解析器

    # 创建统计器件特性对象
    statistic = Electrica.KEITHLEY4200.MemTransistorStatistics(data_directory=args.data_directory, voltage_unit=args.voltage_unit,
                                                               current_unit=args.current_unit)

    # 统计器件特性
    statistic.Analysis(mode=args.mode, channel_type=args.channel_type, analysis_subject=args.analysis_subject,
                       ON_range=args.ON_range, OFF_range=args.OFF_range, V_FullWidth=args.V_FullWidth,
                       window_size=args.window_size, boundary_cond=args.boundary_cond, Vth_eval_range=args.Vth_eval_range,
                       mem_eval_range=args.mem_eval_range, SS_eval_range=args.SS_eval_range)

    # 热度图
    for character in args.heatmap:
        # 画热度图
        statistic.Heatmap(character=character, annot=args.annot, colormap=args.colormap, colormap_source=args.colormap_source)

        if isinstance(args.format, str):  # 只指定了一个格式
            plt.savefig(f"{args.saving_directory}/{character}.{args.format}")  # 保存图像

        elif isinstance(args.format, tuple):  # 指定了多个格式，则保存到对应格式命名的目录下
            for fmt in args.format:
                if not os.path.exists(f"{args.saving_directory}/{fmt}"):  # 检查保存目录是否存在
                    os.makedirs(f"{args.saving_directory}/{fmt}")  # 如果不存在则创建目录
                plt.savefig(f"{args.saving_directory}/{fmt}/{character}.{fmt}")  # 保存图像

        plt.close()  # 关闭图像

    # 分布图
    for character in args.distribution:
        statistic.Distribution(character=character)  # 画分布图

        if isinstance(args.format, str):                                         # 只指定了一个格式
            plt.savefig(f"{args.saving_directory}/{character}.{args.format}")    # 保存图像

        elif isinstance(args.format, tuple):                                     # 指定了多个格式，则保存到对应格式命名的目录下
            for fmt in args.format:
                if not os.path.exists(f"{args.saving_directory}/{fmt}"):         # 检查保存目录是否存在
                    os.makedirs(f"{args.saving_directory}/{fmt}")                # 如果不存在则创建目录
                plt.savefig(f"{args.saving_directory}/{fmt}/{character}.{fmt}")  # 保存图像

        plt.close()  # 关闭图像

    print('Analysis completed!')