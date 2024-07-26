import argparse
from src.Electrica.Analysis import FreqAnal

default_working_place = 'MMW405'  # 默认工作地点

# 默认的数据文件目录字典
data_dir_dict = {'Macbook': '/Users/liusongwei/Desktop/SolutionIC_Temporary/Data/RO',
                 'MMW405': 'E:/Projects/Jingfang Pei/Solution-processed IC/Temporary_working_dir/RO/20240711'}
# 默认的数据保存目录字典
saving_dir_dict = {}

def InitializeParser():
    '''
    用于初始化命令行解析器的函数, 并返回解析器对象（此函数可以后续直接命令行调用此脚本）
    '''

    parser = argparse.ArgumentParser()  # 加载命令行解析器

    parser.add_argument('--file_name', metavar='-F', type=str, default='data.csv', help='File name')  # 数据文件

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    # 提取数据
    working_place = 'MMW405'

    data_dir_dict = {'Macbook': '/Users/liusongwei/Desktop/SolutionIC_Temporary/Data/RO',
                     'MMW405': 'E:/Projects/Jingfang Pei/Solution-processed IC/Temporary_working_dir/RO/20240711'}

    data_filename = 'Vdd_9V.csv'
    data_file = f"{data_dir_dict[working_place]}/{data_filename}"

    data_DF = pd.read_csv(data_file)
    time = data_DF.values[:, 0]
    y = data_DF.values[:, 1]

    n_sample = len(time)  # 采样点数
    f_sample = n_sample / max(time)  # 采样频率

    # print(n_sample, f_sample)

    # 创建一个frequency analysis对象
    # 频谱分析测试
    drop_out_ratio = 0.05

    FA = FreqAnal(signal_train=x, n_sample=npoints, f_sample=fs, drop_out=False, drop_out_ratio=0.05,
                  window_func='identity')
    # FA = FreqAnal(signal_train=y, n_sample=n_sample, f_sample=f_sample, window_func='identity')

    f_raw, amp_raw = FA.Cal_FFT_raw()  # 计算原始频谱
    f_raw, amp_raw = FA.Dropout([f_raw, amp_raw], drop_out_ratio=drop_out_ratio, mode='full')  # 零频去除

    f, amp = FA.Cal_FFT_standard()  # 计算标准化的频谱
    f, amp = FA.Dropout([f, amp], drop_out_ratio=drop_out_ratio, mode='half')  # 零频去除

    f_phase, phase = FA.Cal_PhaseSpec_raw()  # 计算原始相位谱
    f_phase, phase = FA.Dropout([f_phase, phase], drop_out_ratio=drop_out_ratio, mode='full')  # 零频去除

    f_energy, energy = FA.Cal_EnergySpec()  # 计算能量谱
    f_energy, energy = FA.Dropout([f_energy, energy], drop_out_ratio=drop_out_ratio, mode='half')  # 零频去除

    f_power_direct, power_direct = FA.Cal_PowerSpec_direct()  # 计算直接周期法功率谱
    f_power_direct, power_direct = FA.Dropout([f_power_direct, power_direct], drop_out_ratio=drop_out_ratio,
                                              mode='half')  # 零频去除

    f_power_correlate, power_correlate = FA.Cal_PowerSpec_correlate()  # 计算自相关法功率谱
    f_power_correlate, power_correlate = FA.Dropout([f_power_correlate, power_correlate], drop_out_ratio=drop_out_ratio,
                                                    mode='half')  # 零频去除

    f_ceps, ceps = FA.Cal_FFT_cepstrum()  # 计算倒谱
    f_ceps, ceps = FA.Dropout([f_ceps, ceps], drop_out_ratio=drop_out_ratio, mode='full')  # 零频去除

    # 画图模块
    scaling_factor = 1e-6  # 缩放系数

    plt.figure(figsize=(10, 6))  # 设置图像大小

    # 画出原始波形
    ax_signal = plt.subplot(311)
    ax_signal.plot(time * 1e3, y)
    ax_signal.set_xlim(time.min() * 1e3, time.max() * 1e3)  # 设置x轴范围
    ax_signal.set_title('Signal output')  # 设置标题
    ax_signal.set_xlabel('Time (ms)')  # 设置x轴标签
    ax_signal.set_ylabel('Voltage (V)')  # 设置y轴标签

    # 画出原始频谱
    ax_fft_raw = plt.subplot(334)
    ax_fft_raw.plot(f_raw * scaling_factor, amp_raw)
    ax_fft_raw.set_title('Raw FFT spectrum')  # 设置标题
    ax_fft_raw.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    # 画出标准化的频谱
    ax_fft = plt.subplot(335)
    ax_fft.plot(f * scaling_factor, amp)  # 画出标准化的频谱
    ax_fft.set_title('Standard FFT spectrum')  # 设置标题
    ax_fft.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    ax_phase = plt.subplot(336)
    ax_phase.plot(f_phase * scaling_factor, phase)  # 画出原始相位谱
    ax_phase.set_title('Phase spectrum')  # 设置标题

    ax_energy = plt.subplot(337)
    ax_energy.plot(f_energy * scaling_factor, energy)  # 画出能量谱
    ax_energy.set_title('Energy spectrum')
    ax_energy.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    # ax_power_direct = plt.subplot(338)
    # ax_power_direct.plot(f_power_direct*scaling_factor,power_direct)  # 画出直接周期法功率谱
    # ax_power_direct.set_title('Power spectrum')
    # ax_power_direct.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    ax_power_correlate = plt.subplot(338)
    ax_power_correlate.plot(f_power_correlate * scaling_factor, power_correlate)  # 画出自相关法功率谱
    ax_power_correlate.set_title('Power spectrum')
    ax_power_correlate.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    ax_ceps = plt.subplot(339)
    ax_ceps.plot(f_ceps, ceps)  # 画出倒谱
    ax_ceps.set_title('Cepstrum')
    ax_ceps.set_xlabel('Quefrency (s)')  # 设置x轴标签

    for axes in [ax_signal, ax_fft_raw, ax_fft, ax_phase, ax_energy, ax_power_correlate, ax_ceps]:  # 遍历所有的子图
        axes.spines['top'].set_visible(False)  # 隐藏上边框
        axes.spines['right'].set_visible(False)  # 隐藏右边框

    plt.tight_layout()  # 调整页面分布
    plt.show(block=True)  # 显示图像

    print('End of the program')
    exit()