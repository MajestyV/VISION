import os
import linecache
import argparse
import numpy as np
import matplotlib.pyplot as plt
# from src.Default_data_folder import GetDefaultDataFolder
# import src.Default_data_folder as default_data_folder

def GetData_Siglent(data_file: str, skiprows: int=6, num_rows: int=500, sampling_interval: int=40000,
                    usecols: tuple=(0, 1), delimiter: str=','):
    '''
    Getting data from Siglent oscilloscope (从示伦特示波器中获取数据)
    skiprows: int, default 6 (跳过前6行)
    max_rows: int, default 100 (读取数据的行数)
    sampling_interval: int, default 1000 (采样间隔，由于数据量较大，可以设置采样间隔，以减少数据量)
    usecols: tuple, default (0,1) (要读取的列)

    '''

    data = np.zeros((num_rows, len(usecols)), dtype=float)  # 创建一个二维数组，用于存储数据

    t_start = float(linecache.getline(data_file, skiprows+1).split(delimiter)[0])  # 获取起始时间
    for i in range(num_rows):
        line = linecache.getline(data_file, i*sampling_interval+skiprows+1)  # 利用linecache按行读取，减少缓存负担（linecache从1开始计数）
        content = line.split(delimiter)  # 以分隔符（逗号，空格，换行'\n'，制表符'\t'等）对字符串做切片
        value = np.array([float(content[n]) for n in usecols])  # 转换为浮点数组
        value[0] = value[0]-t_start  # 时间从0开始（归零）

        data[i, :] = value  # 将数据存入数组

    return data

if __name__ == '__main__':
    # 主程序可用于在命令行终端快速提取数据到txt文件

    default_mode = 'multiple'  # 默认的读取模式

    # 默认的数据路径
    # example_data_directory = 'E:/Projects/EchoStateMachine/Data/ResNode测试/ResNode_20240510/Triangular'  # MMW502
    example_data_directory = 'E:/Projects/EchoStateMachine/Data/ResNode测试/Temperary'

    example_data_filename = 'SDS2354X_HD_Binary_C1_1_Analog_Trace.csv'  # 示例数据文件

    example_data_file = f"{example_data_directory}/{example_data_filename}"  # 示例数据文件的绝对地址

    default_saving_directory = os.path.abspath(os.path.join(os.getcwd(), '..'))+'/Default_data_folder'  # 默认的数据存储路径

    # 加载命令行解析器
    parser = argparse.ArgumentParser()

    # 读取模式
    parser.add_argument('--mode', metavar='-M', type=str, default=default_mode, help='Mode')  # 读取模式

    # 源数据文件参数
    parser.add_argument('--data_file', metavar='-D', type=str, default=example_data_file, help='Source data file')  # 源数据文件绝对地址
    parser.add_argument('--data_directory', metavar='-P', type=str, default=example_data_directory, help='Data directory')  # 源数据文件夹

    # 数据读取参数
    parser.add_argument('--skiprows', metavar='-K', type=int, default=6, help='Skip rows')  # 跳过的行数
    parser.add_argument('--num_rows', metavar='-N', type=int, default=500, help='Number of rows read')  # 最大行数
    parser.add_argument('--sampling_interval', metavar='-I', type=int, default=40000, help='Sampling interval')  # 采样间隔
    parser.add_argument('--usecols', metavar='-C', type=tuple, default=(0, 1), help='Use columns')  # 使用的列
    parser.add_argument('--delimiter', metavar='-B', type=str, default=',', help='Delimiter')  # 分隔符

    # 数据保存参数
    parser.add_argument('--saving_directory', metavar='-S', type=str, default=default_saving_directory,
                        help='Saving directory')  # 数据文件
    parser.add_argument('--file_name', metavar='-F', type=str, default='data.csv', help='File name')  # 数据文件

    args = parser.parse_args()

    # 区分模式读取
    if args.mode == 'single':  # 单文件模式
        data = GetData_Siglent(data_file=args.data_file,
                               skiprows=args.skiprows, num_rows=args.num_rows, sampling_interval=args.sampling_interval,
                               usecols=args.usecols, delimiter=args.delimiter)
        np.savetxt(f"{args.saving_directory}/{args.file_name}", data, delimiter=',')  # 保存数据

    elif args.mode == 'multiple':  # 多文件模式
        # 在这个模式下，不需要指定文件名，只需要指定文件夹，程序会自动读取文件夹下的所有文件中的数据
        file_list = os.listdir(args.data_directory)
        for file in file_list:
            data = GetData_Siglent(data_file=f"{args.data_directory}/{file}",
                                   skiprows=args.skiprows, num_rows=args.num_rows, sampling_interval=args.sampling_interval,
                                   usecols=args.usecols, delimiter=args.delimiter)
            np.savetxt(f"{args.saving_directory}/{file}", data, delimiter=',')  # 保存数据
    else:
        print('Invalid mode! Please select a valid mode parameter: single or multiple ! ! !')
        exit()

    print('Data extraction completed!')
    exit()