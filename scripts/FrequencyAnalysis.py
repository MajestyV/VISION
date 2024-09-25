# 有时pycharm的文件结构和cmd的文件结构不一样，在cmd中运行会显示：ModuleNotFoundError: No module named 'src'
# 这可以通过在脚本开头添加项目根目录到sys.path中解决，详情请参考：https://blog.csdn.net/qq_42730750/article/details/119799157
import os
import sys
project_path = os.path.abspath(os.path.join(os.getcwd(), '..'))  # 项目根目录
sys.path.append(project_path)  # 添加路径到系统路径中

import argparse                              # 导入命令行解析库
import numpy as np                           # 导入numpy库
import pandas as pd                          # 导入pandas库
from src.Electrica.Analysis import FreqAnal  # 导入频谱分析模块
import matplotlib.pyplot as plt              # 导入画图库
import seaborn as sns                        # 导入seaborn库

default_working_place = 'MMW405'             # 默认工作地点

# 默认的数据文件目录字典
data_dir_dict = {'Macbook': '/Users/liusongwei/Desktop/SolutionIC_Temporary/Data/RO',
                 'MMW405': 'E:/Projects/Jingfang Pei/Solution-processed IC/Temporary_working_dir/RO/20240711'}
# 默认的数据保存目录字典
saving_dir_dict = {'MMW405': 'E:/Projects/Jingfang Pei/Solution-processed IC/Temporary_working_dir/RO/20240711'}

def InitializeParser():
    '''
    用于初始化命令行解析器的函数, 并返回解析器对象（此函数可以后续直接命令行调用此脚本）
    '''

    parser = argparse.ArgumentParser()  # 加载命令行解析器

    # 文件读取参数
    parser.add_argument('--working_place', metavar='-W', type=str, default=default_working_place, help='Working place')  # 工作地点
    parser.add_argument('--file_name', metavar='-F', type=str, default='data', help='File name')  # 数据文件名
    parser.add_argument('--data_format', metavar='-T', type=str, default='csv', help='File type')  # 数据文件类型

    # 解析参数
    parser.add_argument('--drop_out', metavar='-D', type=bool, default=False, help='Drop out zero frequency')  # 是否去除零频
    parser.add_argument('--drop_out_ratio', metavar='-R', type=float, default=0.05, help='Drop out ratio')  # 零频去除比例
    parser.add_argument('--window_func', metavar='-W', type=str, default='identity', help='Window function')  # 窗函数

    # 画图参数
    parser.add_argument('--fig_size', metavar='-S', type=tuple, default=(12, 7.2), help='Figure size')  # 图像大小

    parser.add_argument('--time_unit', metavar='-TU', type=str, default='', help='Time unit')  # 时间缩放系数
    parser.add_argument('--freq_unit', metavar='-FU', type=str, default='', help='Frequency unit')  # 频率缩放系数

    parser.add_argument('--set_freq_range', metavar='-SFR', type=bool, default=False, help='Set frequency range')  # 是否设置频率范围
    parser.add_argument('--freq_range', metavar='-FR', type=tuple, default=(0, 17), help='Frequency range')  # 频率范围

    parser.add_argument('--power_spectrum_method', metavar='-M', type=str, default='correlate', help='Power spectrum method')  # 功率谱计算方法

    parser.add_argument('--figure_format', metavar='-FF', type=str, default='png', help='Figure format')  # 图像保存格式
    parser.add_argument('--figure_quality', metavar='-DPI', type=int, default=300, help='Figure quality')  # 图像保存质量

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = InitializeParser()  # 初始化命令行解析器
    data_file = f"{data_dir_dict[args.working_place]}/{args.file_name}.{args.data_format}"  # 数据文件的绝对地址

    # 提取数据
    data_DF = pd.read_csv(data_file)
    time = data_DF.values[:, 0]  # 时间
    signal = data_DF.values[:, 1]  # 信号

    n_sample = len(time)  # 采样点数
    f_sample = n_sample / max(time)  # 采样频率

    # 创建一个频谱分析测试对象
    FA = FreqAnal(signal_train=signal, n_sample=n_sample, f_sample=f_sample, drop_out=args.drop_out,
                  drop_out_ratio=args.drop_out_ratio,window_func=args.window_func)

    amp_raw = FA.Cal_FFT_raw()  # 计算原始频谱
    amp = FA.Cal_FFT_standard()  # 计算标准化的频谱
    phase = FA.Cal_PhaseSpec_raw()  # 计算原始相位谱
    energy = FA.Cal_EnergySpec()  # 计算能量谱
    power_direct = FA.Cal_PowerSpec_direct()  # 计算直接周期法功率谱
    power_correlate = FA.Cal_PowerSpec_correlate()  # 计算自相关法功率谱
    ceps = FA.Cal_FFT_cepstrum()  # 计算倒谱

    # 零频去除模块
    info_list = [amp_raw, amp, phase, energy, power_direct, power_correlate]  # 信息列表（倒谱先不用去零频，代码还没完善好）
    mode_list = ['full', 'half', 'full', 'half', 'half', 'half']  # 模式列表
    if args.drop_out:
        for i in range(len(info_list)):
            info_list[i] = FA.Dropout(info_list[i], drop_out_ratio=args.drop_out_ratio, mode=mode_list[i])
    else:
        pass

    # 画图模块，关于横纵坐标，请参考：https://blog.csdn.net/qq_35576225/article/details/109403321
    scaling_dict = {'n': 1e9, 'u': 1e6, 'm': 1e3, '': 1.0, 'k': 1e-3, 'M': 1e-6, 'G': 1e-9}  # 缩放系数字典，小要放大，大要缩小

    t_scale = scaling_dict[args.time_unit]  # 时间缩放系数
    f_scale = scaling_dict[args.freq_unit]  # 频率缩放系数

    color_platte = sns.color_palette('deep')  # 颜色板

    plt.figure(figsize=args.fig_size)  # 设置图像大小

    # 画出原始波形
    ax_signal = plt.subplot(311)  # 创建子图
    ax_signal.plot(time*t_scale, signal, color=color_platte[0])
    ax_signal.set_xlim(time.min()*t_scale, time.max()*t_scale)  # 设置x轴范围
    ax_signal.set_title('Signal output')  # 设置标题
    ax_signal.set_xlabel(f"Time ({args.time_unit}s)")  # 设置x轴标签
    ax_signal.set_ylabel('Voltage (V)')  # 设置y轴标签

    # 画出原始频谱
    ax_fft_raw = plt.subplot(334)  # 创建子图
    ax_fft_raw.plot(amp_raw[0]*f_scale, amp_raw[1], color=color_platte[1])  # 画出原始频谱
    ax_fft_raw.set_xlim(amp_raw[0].min()*f_scale, amp_raw[0].max()*f_scale)  # 设置x轴范围
    ax_fft_raw.set_title('Raw FFT spectrum')  # 设置标题
    ax_fft_raw.set_xlabel(f"Frequency ({args.freq_unit}Hz)")  # 设置x轴标签
    ax_fft_raw.set_ylabel('Amplitude (a.u.)')  # 设置y轴标签

    # 画出标准化的频谱
    ax_fft = plt.subplot(335)  # 创建子图
    ax_fft.plot(amp[0]*f_scale, amp[1], color=color_platte[2])  # 画出标准化的频谱
    if args.set_freq_range:
        ax_fft.set_xlim(args.freq_range[0], args.freq_range[1])
    else:
        ax_fft.set_xlim(amp[0].min()*f_scale, amp[0].max()*f_scale)
    ax_fft.set_title('Standard FFT spectrum')  # 设置标题
    ax_fft.set_xlabel(f"Frequency ({args.freq_unit}Hz)")  # 设置x轴标签
    ax_fft.set_ylabel('Norm. Amp. (a.u.)')  # 设置y轴标签

    # 画出原始相位谱
    ax_phase = plt.subplot(336)  # 创建子图
    ax_phase.plot(phase[0]*f_scale, phase[1]*180/np.pi, color=color_platte[3])  # 画出原始相位谱，将弧度转换为角度
    ax_phase.set_xlim(phase[0].min()*f_scale, phase[0].max()*f_scale)  # 设置x轴范围
    ax_phase.set_title('Phase spectrum')  # 设置标题
    ax_phase.set_xlabel(f"Frequency ({args.freq_unit}Hz)")  # 设置x轴标签
    ax_phase.set_ylabel('Phase (deg)')  # 设置y轴标签
    ax_phase.set_ylim(-200, 200)  # 设置y轴范围
    ax_phase.set_yticks(np.arange(-180, 181, 90))  # 设置y轴刻度

    # 画出能量谱
    ax_energy = plt.subplot(337)  # 创建子图
    ax_energy.plot(energy[0]*f_scale, energy[1], color=color_platte[4])  # 画出能量谱
    if args.set_freq_range:
        ax_energy.set_xlim(args.freq_range[0], args.freq_range[1])
    else:
        ax_energy.set_xlim(energy[0].min()*f_scale, energy[0].max()*f_scale)
    ax_energy.set_title('Energy spectrum')
    ax_energy.set_xlabel(f"Frequency ({args.freq_unit}Hz)")  # 设置x轴标签
    ax_energy.set_ylabel('Energy (a.u.)')  # 设置y轴标签

    # 画出功率谱
    if args.power_spectrum_method == 'direct':
        ax_power = plt.subplot(338)  # 创建子图
        ax_power.plot(power_direct[0]*f_scale, power_direct[1], color=color_platte[5])  # 画出直接周期法功率谱
        if args.set_freq_range:
            ax_power.set_xlim(args.freq_range[0], args.freq_range[1])
        else:
            ax_power.set_xlim(power_direct[0].min()*f_scale, power_direct[0].max()*f_scale)
        ax_power.set_title('Power spectrum by direct approach')
        ax_power.set_xlabel(f"Frequency ({args.freq_unit}Hz)")  # 设置x轴标签
        ax_power.set_ylabel('Power (dB)')  # 设置y轴标签
    elif args.power_spectrum_method == 'correlate':
        ax_power = plt.subplot(338)  # 创建子图
        ax_power.plot(power_correlate[0]*f_scale, power_correlate[1], color=color_platte[5])  # 画出自相关法功率谱
        if args.set_freq_range:
            ax_power.set_xlim(args.freq_range[0], args.freq_range[1])
        else:
            ax_power.set_xlim(power_correlate[0].min()*f_scale, power_correlate[0].max()*f_scale)
        ax_power.set_title('Power spectrum by correlate approach')
        ax_power.set_xlabel(f"Frequency ({args.freq_unit}Hz)")  # 设置x轴标签
        ax_power.set_ylabel('Power (dB)')  # 设置y轴标签
    else:
        raise ValueError('Invalid power spectrum method! Please select a valid method: "direct" or "correlate" ! ! !')

    # 画出倒谱（目前还没好，有点小问题）
    ax_ceps = plt.subplot(339)  # 创建子图
    ax_ceps.plot(ceps[0]*f_scale, ceps[1], color=color_platte[6])  # 画出倒谱，注意这里的频率是倒谱的频率，所以是1/f_scale
    # ax_ceps.set_xlim(ceps[0].min()*f_scale, ceps[0].max()*f_scale)  # 设置x轴范围
    ax_ceps.set_title('Cepstrum')
    ax_ceps.set_xlabel(f"Quefrency ({args.time_unit}s)")  # 设置x轴标签，注意这里的时间是倒谱的时间，所以用时间单位
    ax_ceps.set_ylabel('Amplitude (a.u.)')  # 设置y轴标签

    # 遍历所有的子图，设置全局图像格式
    for axes in [ax_signal, ax_fft_raw, ax_fft, ax_phase, ax_energy, ax_power, ax_ceps]:
        axes.spines['top'].set_visible(False)  # 隐藏上边框
        axes.spines['right'].set_visible(False)  # 隐藏右边框

    plt.tight_layout()  # 调整页面分布

    # 保存图像
    plt.savefig(f"{saving_dir_dict[args.working_place]}/{args.file_name}_windowfunc-{args.window_func}.{args.figure_format}",
                dpi=args.figure_quality)

    plt.show(block=True)  # 显示图像

    print('Code finished ! ! !')  # 输出程序执行完毕提示信息
    exit()