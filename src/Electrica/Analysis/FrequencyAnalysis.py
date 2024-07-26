import numpy as np
from scipy.fftpack import fft
import pandas as pd  # 数据提取包
import matplotlib.pyplot as plt  # 画图包

class FreqAnal:
    def __init__(self, signal_train: np.ndarray, n_sample: int, f_sample: float, window_func: str = 'identity', **kwargs):
        '''
        This class of function is designed for analysis the frequency spectrum of time series.
        signal_train: np.ndarray, the time series data
        n_sample: int, 采样点数
        f_sample: float, 采样频率
        drop_out: bool, 是否进行零频去除
        drop_out_ratio: float, 零频去除比例
        '''

        # 窗函数字典
        window_dict = {'hanning': np.hanning, 'hamming': np.hamming, 'blackman': np.blackman, 'bartlett': np.bartlett}
        if window_func == 'identity':                                    # 不加窗
            signal_train = signal_train
        else:                                                            # 加窗
            window = window_dict[window_func](n_sample)                  # 选择合适的窗函数
            signal_train = signal_train * window                         # 对信号进行窗口加权

        y_fft = fft(signal_train)                                        # 频域信号
        y_fft_half = y_fft[0:n_sample//2]                                # 取一半区间的频域信号
        f_values_half = np.linspace(0.0, f_sample / 2.0, n_sample // 2)  # 单边频域
        f_values_full = np.linspace(0.0, f_sample, n_sample)             # 双边频域

        # 批量转换为实例变量方便后面调用
        self.y = signal_train                                            # 时域信号
        self.n_sample = n_sample                                         # 采样点数
        self.f_sample = f_sample                                         # 采样频率
        self.y_fft = y_fft
        self.y_fft_half = y_fft_half
        self.f_values_full = f_values_full
        self.f_values_half = f_values_half

    def Cal_FFT_raw(self): return self.f_values_full, self.y_fft  # 计算原始频谱

    def Cal_FFT_standard(self):
        '''
        计算标准化的频谱
        '''
        fft_values = 2.0 / self.n_sample * np.abs(self.y_fft_half)  # 计算标准化的频谱
        return self.f_values_half, fft_values

    def Cal_PhaseSpec_raw(self):
        '''
        计算原始相位谱
        '''
        phase_values = np.angle(self.y_fft)  # 计算相位谱
        return self.f_values_full, phase_values

    def Cal_EnergySpec(self):
        '''
        计算能量谱
        '''
        energy_values = np.square(np.abs(self.y_fft_half))
        return self.f_values_half, energy_values

    def Cal_PowerSpec_direct(self):
        '''
        通过直接周期法计算功率谱
        '''
        power_values = np.square(np.abs(self.y_fft_half)) / self.n_sample
        return self.f_values_half, power_values

    def Cal_PowerSpec_correlate(self):
        '''
        通过自相关方法计算功率谱
        维纳-辛钦定理指出：一个信号的功率谱密度就是该信号自相关函数的傅里叶变换
        详情请参考：https://zh.wikipedia.org/zh-cn/%E7%BB%B4%E7%BA%B3-%E8%BE%9B%E9%92%A6%E5%AE%9A%E7%90%86
        '''
        cor_y = np.correlate(self.y, self.y, mode='full')  # 计算自相关函数
        cor_f = fft(cor_y,self.n_sample)  # 计算自相关函数的傅里叶变换
        cor_power = np.abs(cor_f)  # 取绝对值
        # 归一化，并转化为分贝（计算功率增益，前面只需要乘10）[https://bbs.eeworld.com.cn/thread-1102719-1-1.html]
        power_values = 10*np.log10(cor_power/np.max(cor_power))  # 计算功率谱
        return  self.f_values_half, power_values[0:self.n_sample//2]  # 返回频率和功率谱，只需返回一半的功率谱

    def Cal_FFT_cepstrum(self):
        '''
        计算倒谱
        '''
        # print(len(self.y), self.n_sample)
        spectrum = fft(self.y,self.n_sample)  # 傅里叶变换
        cepstrum = np.fft.ifft(np.log(np.abs(spectrum))).real  # 信号→傅里叶→对数→傅里叶逆变换
        return self.f_values_full, cepstrum

    def Dropout(self, data: list, drop_out_ratio: float, mode: str):
        '''
        零频去除函数
        '''
        x_value, y_value = data  # 解压出数据

        idx_min = int(self.n_sample * drop_out_ratio)  # 去除的最低频率的索引
        idx_max = int(self.n_sample * (1 - drop_out_ratio))  # 去除的最高频率的索引

        if mode == 'half':  # 半幅数据的截断
            x_value_dropped = x_value[idx_min:idx_max]
            y_value_dropped = y_value[idx_min:idx_max]
        elif mode == 'full':  # 全幅数据的截断
            x_value_dropped = x_value[idx_min:idx_max]
            y_value_dropped = y_value[idx_min:idx_max]
        else:
            raise ValueError('The mode is not supported, please select from "half" or "full" ! ! !')

        return x_value_dropped, y_value_dropped

if __name__=='__main__':
    # 采样点选择1400个，由于设置的信号频率份量最高为600赫兹，根据采样定理知采样频率要大于信号频率2倍，因此这里设置采样频率为1400赫兹（即一秒内有1400个采样点，同样意思的）
    # x = np.linspace(0, 1, 1400)

    # 设置须要采样的信号，频率份量有200，400和600
    # y = 7 * np.sin(2 * np.pi * 200 * x) + 5 * np.sin(2 * np.pi * 400 * x) + 3 * np.sin(2 * np.pi * 600 * x)

    # """
    # 生成原始信号序列

    # 在原始信号中加上噪声
    # np.random.randn(t.size)
    # """
    fs = 1000
    npoints = 1000

    t = np.arange(0, 1, 1 / fs)
    f0 = 100
    f1 = 200
    x = np.cos(2 * np.pi * f0 * t) + 3 * np.cos(2 * np.pi * f1 * t) + np.random.randn(t.size)

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

    FA = FreqAnal(signal_train=x, n_sample=npoints, f_sample=fs, drop_out=False, drop_out_ratio=0.05, window_func='identity')
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
    f_power_direct, power_direct = FA.Dropout([f_power_direct, power_direct], drop_out_ratio=drop_out_ratio, mode='half')  # 零频去除

    f_power_correlate, power_correlate = FA.Cal_PowerSpec_correlate()  # 计算自相关法功率谱
    f_power_correlate, power_correlate = FA.Dropout([f_power_correlate, power_correlate], drop_out_ratio=drop_out_ratio, mode='half')  # 零频去除

    f_ceps, ceps = FA.Cal_FFT_cepstrum()  # 计算倒谱
    f_ceps, ceps = FA.Dropout([f_ceps, ceps], drop_out_ratio=drop_out_ratio, mode='full')  # 零频去除

    # 画图模块
    scaling_factor = 1e-6  # 缩放系数

    plt.figure(figsize=(10, 6))  # 设置图像大小

    # 画出原始波形
    ax_signal = plt.subplot(311)
    ax_signal.plot(time*1e3, y)
    ax_signal.set_xlim(time.min()*1e3, time.max()*1e3)  # 设置x轴范围
    ax_signal.set_title('Signal output')  # 设置标题
    ax_signal.set_xlabel('Time (ms)')     # 设置x轴标签
    ax_signal.set_ylabel('Voltage (V)')   # 设置y轴标签

    # 画出原始频谱
    ax_fft_raw = plt.subplot(334)
    ax_fft_raw.plot(f_raw*scaling_factor,amp_raw)
    ax_fft_raw.set_title('Raw FFT spectrum')  # 设置标题
    ax_fft_raw.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    # 画出标准化的频谱
    ax_fft = plt.subplot(335)
    ax_fft.plot(f*scaling_factor,amp)  # 画出标准化的频谱
    ax_fft.set_title('Standard FFT spectrum')  # 设置标题
    ax_fft.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    ax_phase = plt.subplot(336)
    ax_phase.plot(f_phase*scaling_factor,phase)  # 画出原始相位谱
    ax_phase.set_title('Phase spectrum')  # 设置标题

    ax_energy = plt.subplot(337)
    ax_energy.plot(f_energy*scaling_factor,energy)  # 画出能量谱
    ax_energy.set_title('Energy spectrum')
    ax_energy.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    # ax_power_direct = plt.subplot(338)
    # ax_power_direct.plot(f_power_direct*scaling_factor,power_direct)  # 画出直接周期法功率谱
    # ax_power_direct.set_title('Power spectrum')
    # ax_power_direct.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    ax_power_correlate = plt.subplot(338)
    ax_power_correlate.plot(f_power_correlate*scaling_factor,power_correlate)  # 画出自相关法功率谱
    ax_power_correlate.set_title('Power spectrum')
    ax_power_correlate.set_xlabel('Frequency (MHz)')  # 设置x轴标签

    ax_ceps = plt.subplot(339)
    ax_ceps.plot(f_ceps,ceps)  # 画出倒谱
    ax_ceps.set_title('Cepstrum')
    ax_ceps.set_xlabel('Quefrency (s)')  # 设置x轴标签

    for axes in [ax_signal,ax_fft_raw, ax_fft, ax_phase, ax_energy, ax_power_correlate, ax_ceps]:  # 遍历所有的子图
        axes.spines['top'].set_visible(False)  # 隐藏上边框
        axes.spines['right'].set_visible(False)  # 隐藏右边框

    plt.tight_layout()  # 调整页面分布
    plt.show(block=True)  # 显示图像

    print('End of the program')
    exit()