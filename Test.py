import matplotlib.pyplot as plt
import numpy as np
import numpy.fft as fft
import pandas as pd

def get_fft_values(y_values, N, f_s):
    '''
    封装好的频谱分析函数
    '''
    f_values = np.linspace(0.0, f_s / 2.0, N // 2)
    fft_values_ = fft.fft(y_values)
    fft_values = 2.0 / N * np.abs(fft_values_[0:N // 2])
    return f_values, fft_values

if __name__ == '__main__':
    # 提取数据
    working_place = 'MMW405'

    data_dir_dict = {'Macbook': '/Users/liusongwei/Desktop/SolutionIC_Temporary/Data/RO',
                     'MMW405': 'E:/Projects/Jingfang Pei/Solution-processed IC/Temporary_working_dir/RO'}

    data_filename = 'data_100000.csv'
    data_file = f"{data_dir_dict[working_place]}/{data_filename}"

    data_DF = pd.read_csv(data_file)
    time = data_DF.values[:, 0]
    y = data_DF.values[:, 1]

    n_sample = len(time)  # 采样点数
    f_sample = n_sample/max(time)  # 采样频率

    print(n_sample,f_sample)

    a, b = get_fft_values(y,N=n_sample,f_s=f_sample)

    print(a,b)

    plt.plot(a,b)
    plt.ylim(-0.01,0.01)

    plt.show(block=True)

