import os
import linecache
import argparse
import numpy as np
from .KEITHLEY4200_GetData import GetData_KEITHLEY4200_OldModel  # 数据读取函数

# 通过定义一个字典，方便地将缩写转换为全称
abbrev_dict = {'t': 'Time', 'Gm': 'GM',
               'V_g': 'GateV', 'V_d': 'DrainV', 'V_s': 'SourceV', 'I_g': 'GateI', 'I_d': 'DrainI', 'I_s': 'SourceI'}

def InitializeParser(default_mode: str='multiple'):
    '''
    初始化命令行解析器, 并返回解析器对象
    '''

    # 设置各种默认路径
    # 示例数据路径
    example_data_directory = 'D:/Projects/Jingfang Pei/Solution-processed IC/Data/4200/20240708 tft 10x10 array'  # JCPGH1

    example_data_filename = 'line_1.xls'  # 示例数据文件

    example_data_file = f"{example_data_directory}/{example_data_filename}"  # 示例数据文件的绝对地址

    example_saving_directory = 'D:/Projects/Jingfang Pei/Solution-processed IC/Data/4200/Working_dir'  # JCPGH1

    ####################################################################################################################
    # 加载命令行解析器
    parser = argparse.ArgumentParser()

    # 读取模式
    parser.add_argument('--mode', metavar='-M', type=str, default=default_mode, help='Mode')  # 读取模式

    # 源数据文件参数
    parser.add_argument('--data_file', metavar='-D', type=str, default=example_data_file,
                        help='Source data file')  # 源数据文件绝对地址
    parser.add_argument('--data_directory', metavar='-P', type=str, default=example_data_directory,
                        help='Data directory')  # 源数据文件夹

    # 数据保存参数
    parser.add_argument('--saving_directory', metavar='-S', type=str, default=example_saving_directory,
                        help='Saving directory')  # 数据文件
    parser.add_argument('--file_name', metavar='-F', type=str, default='data.csv', help='File name')  # 数据文件

    args = parser.parse_args()

    return args

    ####################################################################################################################

    # 区分模式读取
    #if args.mode == 'single':  # 单文件模式
        #data = GetData_Siglent(data_file=args.data_file,
                               #skiprows=args.skiprows, num_rows=args.num_rows, sampling_interval=args.sampling_interval,
                               #usecols=args.usecols, delimiter=args.delimiter)
        #np.savetxt(f"{args.saving_directory}/{args.file_name}", data, delimiter=',')  # 保存数据

    #elif args.mode == 'multiple':  # 多文件模式
        # 在这个模式下，不需要指定文件名，只需要指定文件夹，程序会自动读取文件夹下的所有文件中的数据
        #file_list = os.listdir(args.data_directory)
        #for file in file_list:
            #data = GetData_Siglent(data_file=f"{args.data_directory}/{file}",
                                   #skiprows=args.skiprows, num_rows=args.num_rows,
                                   #sampling_interval=args.sampling_interval,
                                   #usecols=args.usecols, delimiter=args.delimiter)
            #np.savetxt(f"{args.saving_directory}/{file}", data, delimiter=',')  # 保存数据
    #else:
        #print('Invalid mode! Please select a valid mode parameter: single or multiple ! ! !')
        #exit()



if __name__ == '__main__':
    args = InitializeParser(default_mode='multiple')  # 初始化命令行解析器

    if args.mode == 'multiple':  # 多文件模式
        # 在这个模式下，不需要指定文件名，只需要指定文件夹，程序会自动读取文件夹下的所有文件中的数据
        file_list = os.listdir(args.data_directory)
        num_files = len(file_list)  # 计算数据文件的数量
        example_data = GetData_KEITHLEY4200_OldModel(data_file=f"{args.data_directory}/{file_list[0]}")
        num_cycles = len(example_data)  # 计算测试循环次数，即数据列表的长度

        # 创建一系列全零数组，用于存储数据
        SS = np.zeros((num_files, num_cycles), dtype=float)  # SS - Subthreshold Swing (亚阈值摆幅)

        for i in range(num_files):
            data = GetData_KEITHLEY4200_OldModel(data_file=f"{args.data_directory}/{file_list[i]}")

            for j in range(num_cycles):

                XXX

                SS[i, j] = XXX





        data = GetData_Siglent(data_file=f"{args.data_directory}/{file}",
    # skiprows=args.skiprows, num_rows=args.num_rows,
    # sampling_interval=args.sampling_interval,
    # usecols=args.usecols, delimiter=args.delimiter)




    print('Data extraction completed!')
    exit()