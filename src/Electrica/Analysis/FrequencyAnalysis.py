import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl

import pandas as pd  # 数据提取包

# mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
# mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

class FreqAnal:
    '''
    This class of function is designed for analysis the frequency spectrum of time series.
    '''
    def __init__(self, signal_train: np.ndarray, num_freq: int):
        self.y = signal_train
        self.fft_y = fft(y)  # 快速傅里叶变换
        self.n_freq = num_freq  # 衡量的频率个数

    def Freq(self): return self.fft_y  # 频谱图

    def Freq_absolute(self): return np.abs(self.fft_y)  # 取复数的绝对值，即复数的模(双边频谱)

    def Freq_normalized(self): return np.abs(self.fft_y)/self.n_freq  # 归一化处理（双边频谱）

    def Freq_half(self):  # 因为对称性，只取一半区间（单边频谱）
        fft_y_normalized = np.abs(self.fft_y)/self.n_freq
        return fft_y_normalized[range(int(self.n_freq/2))]

    def Phase(self): return np.angle(fft_y)  # 取复数的角度，即为相位


if __name__=='__main__':
    # 采样点选择1400个，由于设置的信号频率份量最高为600赫兹，根据采样定理知采样频率要大于信号频率2倍，因此这里设置采样频率为1400赫兹（即一秒内有1400个采样点，同样意思的）
    # x = np.linspace(0, 1, 1400)

    # 设置须要采样的信号，频率份量有200，400和600
    # y = 7 * np.sin(2 * np.pi * 200 * x) + 5 * np.sin(2 * np.pi * 400 * x) + 3 * np.sin(2 * np.pi * 600 * x)

    # 提取数据
    data_directory = '/Users/liusongwei/Desktop/SolutionIC_Temporary/Data/RO'  # Macbook
    data_filename = 'data_1000.csv'
    data_file = f"{data_directory}/{data_filename}"

    data_DF = pd.read_csv(data_file)
    time = data_DF.values[:, 0]
    y = data_DF.values[:, 1]

    # print(data_DF.values)


    # exit()

    N = len(y)
    x = np.arange(N)  # 频率个数
    half_x = x[range(int(N / 2))]  # 取一半区间

    FA = FreqAnal(signal_train=y,num_freq=N)  # 创建一个frequency analysis对象
    fft_y = FA.Freq()
    abs_y = FA.Freq_absolute()
    angle_y = FA.Phase()
    normalization_y = FA.Freq_normalized()
    normalization_half_y = FA.Freq_half()

    plt.subplot(231)
    plt.plot(x, y)
    plt.title('原始波形')

    plt.subplot(232)
    plt.plot(x, fft_y, 'black')
    plt.title('双边振幅谱(未求振幅绝对值)', fontsize=9, color='black')

    plt.subplot(233)
    plt.plot(x, abs_y, 'r')
    plt.title('双边振幅谱(未归一化)', fontsize=9, color='red')

    plt.subplot(234)
    plt.plot(x, angle_y, 'violet')
    plt.title('双边相位谱(未归一化)', fontsize=9, color='violet')

    plt.subplot(235)
    plt.plot(x, normalization_y, 'g')
    plt.title('双边振幅谱(归一化)', fontsize=9, color='green')

    plt.subplot(236)
    plt.plot(half_x, normalization_half_y, 'blue')
    plt.title('单边振幅谱(归一化)', fontsize=9, color='blue')

    plt.tight_layout()  # 调整页面分布

    plt.show(block=True)