import linecache
import numpy as np
import matplotlib.pyplot as plt

def GetData_Siglent(data_file: str, skiprows: int=6, max_rows: int=500, sampling_interval: int=40000, usecols: tuple=(0, 1)):
    '''
    Getting data from Siglent oscilloscope (从示伦特示波器中获取数据)
    skiprows: int, default 6 (跳过前6行)
    max_rows: int, default 100 (读取数据的行数)
    sampling_interval: int, default 1000 (采样间隔，由于数据量较大，可以设置采样间隔，以减少数据量)
    usecols: tuple, default (0,1) (要读取的列)

    '''

    data = np.zeros((max_rows, 2), dtype=float)  # 创建一个二维数组，用于存储数据

    t_start = float(linecache.getline(data_file, skiprows+1).split(',')[0])  # 获取起始时间
    for i in range(max_rows):
        line = linecache.getline(data_file, i*sampling_interval+skiprows+1)  # 利用linecache按行读取，减少缓存负担（linecache从1开始计数）
        content = line.split(',')  # 以逗号（空格，换行'\n'，制表符'\t'等）为分隔符对字符串做切片
        value = np.array([float(content[n]) for n in usecols])  # 转换为浮点数组
        value[0] = value[0]-t_start  # 时间从0开始（归零）

        data[i, :] = value  # 将数据存入数组

    return data

if __name__ == '__main__':
    pass