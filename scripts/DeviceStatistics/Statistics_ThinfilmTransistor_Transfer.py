# 有时pycharm的文件结构和cmd的文件结构不一样，在cmd中运行会显示：ModuleNotFoundError: No module named 'src'
# 这可以通过在脚本开头添加项目根目录到sys.path中解决，详情请参考：https://blog.csdn.net/qq_42730750/article/details/119799157
import os
import sys
project_path = os.path.abspath(os.path.join(os.path.join(os.getcwd(), '..'), '..'))  # 项目根目录
sys.path.append(project_path)  # 添加路径到系统路径中

import argparse
from src import Electrica
import matplotlib.pyplot as plt

working_loc = 'Lingjiang'             # 默认工作地点

# 默认的数据文件目录字典
data_dir_dict = {'Macbook': '/Users/liusongwei/Desktop/SolutionIC_Temporary/Data/RO',
                 'MMW405': 'E:/Projects/Jingfang Pei/Solution-processed IC/Temporary_working_dir/RO/20240711',
                 'JCPGH1': 'D:/Projects/Jingfang Pei/Solution-processed IC/Data/4200/20240923 tft 20x20 array glass substrate',
                 'Lingjiang': 'E:/PhD_research/Jingfang Pei/Solution-processed IC/Data/KEITHLEY4200/20250323 sol ic 5x20_preview/1_to_10_then_11_to_20_separated'}  # Not yet ready

# 默认的数据保存目录字典
saving_dir_dict = {'MMW405': 'E:/Projects/Jingfang Pei/Solution-processed IC/Temporary_working_dir/RO/20240711',
                   'JCPGH1': 'C:/Users/13682/OneDrive/桌面/Temporary_data/SolutionIC_glass',
                   'Lingjiang': 'E:/PhD_research/Jingfang Pei/Solution-processed IC/Data/KEITHLEY4200/Working_dir'}

def InitializeParser() -> argparse.Namespace:
    '''
    初始化命令行解析器, 并返回解析器对象
    '''
    # 加载命令行解析器
    parser = argparse.ArgumentParser()

    # 数据文件路径以及分析结果保存路径
    parser.add_argument('--data_directory', metavar='-P', type=str, default=data_dir_dict[working_loc], help='Data directory')  # 数据文件夹
    parser.add_argument('--saving_directory', metavar='-S', type=str, default=saving_dir_dict[working_loc], help='Saving directory')  # 分析结果保存文件夹

    # 基础设置
    parser.add_argument('--voltage_unit', metavar='-V', type=str, default='mV', help='Voltage unit')  # 电压单位
    parser.add_argument('--current_unit', metavar='-I', type=str, default='A', help='Current unit')  # 电流单位

    # 统计分析参数
    parser.add_argument('--mode', metavar='-M', type=str, default='auto', help='Analysis mode')  # 分析模式
    parser.add_argument('--ON_range', metavar='-ON', type=tuple, default=(-0.5, -0.4), help='ON range')  # ON范围
    parser.add_argument('--OFF_range', metavar='-OFF', type=tuple, default=(1.3, 1.5), help='OFF range')  # OFF范围
    parser.add_argument('--SS_range', metavar='-SS', type=tuple, default=(0.3, 0.5), help='SS range')  # SS范围
    parser.add_argument('--Vth_location', metavar='-Vth', type=tuple, default=(0.25, 1.25), help='Vth location')  # 阈值电压位置

    # 分析指标设置
    parser.add_argument('--heatmap', metavar='-H', type=tuple, nargs='+',
                        default=('ON_OFF_ratio', 'ON_OFF_ratio_extreme', 'SS'), help='Heatmap')  # 热图
    parser.add_argument('--distribution', metavar='-D', type=tuple, nargs='+', default=('Igs', 'Vth'),
                        help='Distribution')  # 分布图

    # 绘图参数
    # argumentParser() 存储bool类型有坑，不能直接传True/False，需要设置action
    # python 终端读取时传入的都是string类型，转为bool型时，由于是非空字符串，所以（无论传入什么字符均）转为True
    # 详情请参考：
    # https://blog.csdn.net/qinduohao333/article/details/131305803
    # https://blog.csdn.net/orangeOrangeRed/article/details/117624905?login=from_csdn
    parser.add_argument('-AN', '--annot', action='store_true', help='Annotation on the heatmap')  # 是否标注
    parser.add_argument('--Leakage_plotting_range', metavar='-:PR', type=tuple, default=(1e-12, 1e-7), help='Igs plotting range')  # 漏电流绘图范围
    parser.add_argument('--Vth_plotting_range', metavar='-VPR', type=tuple, default=(-0.5, 1.5), help='Vth plotting range')  # Vth绘图范围
    parser.add_argument('--format', metavar='-F', type=str or tuple, default=('png', 'eps', 'pdf'), help='Figure format')  # 图像保存格式


    # 以下增加几个指标
    parser.add_argument('--Igs', metavar='-Igs', type=tuple, default=(-0.5, 0.5), help='Igs range')  # Igs范围


    args = parser.parse_args()

    return args

if __name__ == '__main__':
    print('Start analysis workflow ...')

    args = InitializeParser()  # 初始化命令行解析器

    print('Parser initialized ...')

    # 创建统计器件特性对象
    statistic = Electrica.KEITHLEY4200.Statistics_Transistor(data_directory=args.data_directory, voltage_unit=args.voltage_unit,
                                                             current_unit=args.current_unit)

    # 统计器件特性
    statistic.Analysis(mode=args.mode, ON_range=args.ON_range, OFF_range=args.OFF_range, SS_range=args.SS_range,
                       Vth_location=args.Vth_location)

    print('Device characteristics analysis completed. Starting to plot results ...')

    # 热度图
    for character in args.heatmap:
        # statistic.Heatmap(character=character, annot=args.annot)  # 画热度图
        statistic.Heatmap(character=character, annot=False)  # 画热度图(debug版本)

        if isinstance(args.format, str):  # 只指定了一个格式
            plt.savefig(f"{args.saving_directory}/{character}.{args.format}")  # 保存图像

        elif isinstance(args.format, tuple):  # 指定了多个格式
            for fmt in args.format:
                plt.savefig(f"{args.saving_directory}/{character}.{fmt}")

        plt.close()  # 关闭图像

    # 分布图
    for character in args.distribution:

        if character == 'Igs':
            statistic.Distribution(character=character, plotting_range=args.Leakage_plotting_range)  # 画漏电流分布图
        elif character == 'Vth':
            statistic.Distribution(character=character, plotting_range=args.Vth_plotting_range)  # 画阈值电压分布图

        if isinstance(args.format, str):
            plt.savefig(f"{args.saving_directory}/{character}.{args.format}")

        elif isinstance(args.format, tuple):
            for fmt in args.format:
                plt.savefig(f"{args.saving_directory}/{character}.{fmt}")

        plt.close()  # 关闭图像

    print('Analysis workflow completed!')