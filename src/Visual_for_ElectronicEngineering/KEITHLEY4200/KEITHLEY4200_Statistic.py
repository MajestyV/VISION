import os
import argparse
import numpy as np
from KEITHLEY4200_GetData import GetData_KEITHLEY4200_OldModel  # 数据读取模块
from KEITHLEY4200_Analysis import TransistorCharacteristics     # 数据分析模块


import seaborn as sns
import matplotlib.pyplot as plt

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
        SS_map = np.zeros((num_files, num_cycles), dtype=float)  # SS - Subthreshold Swing (亚阈值摆幅)
        on_off_ratio_map = np.zeros((num_files, num_cycles), dtype=float)  # 开关比
        on_off_ratio_extreme_map = np.zeros((num_files, num_cycles), dtype=float)  # 开关比（极端值）
        leakage_avg_map = np.zeros((num_files, num_cycles), dtype=float)  # 平均漏电流
        Vth_map = np.zeros((num_files, num_cycles), dtype=float)  # 阈值电压

        for i in range(num_files):
            data = GetData_KEITHLEY4200_OldModel(data_file=f"{args.data_directory}/{file_list[i]}")

            for j in range(num_cycles):
                transistor = TransistorCharacteristics(data=data[j])  # 创建一个晶体管特性对象
                Vgs, Id, Is, Ig = transistor.TransferCurve()  # 获取传输曲线
                # on_off_ratio = transistor.OnOffRatio((-0.5, -0.48), (1.24, 1.26))  # 计算开关比
                # on_off_ratio_extreme = transistor.OnOffRatio_Extreme()  # 计算开关比（极端值）
                SS = transistor.SubthresholdSwing((0.7, 0.9))  # 计算亚阈值摆幅
                leakage_avg = transistor.LeakageCurrent()  # 计算平均漏电流
                Vth, dI_dV, d2I_dV2 = transistor.ThresholdVoltage((0.25, 1.25))  # 计算阈值电压

                # 存储数据
                SS_map[i,j] = SS  # 亚阈值摆幅
                # on_off_ratio_map = on_off_ratio  # 开关比
                # on_off_ratio_extreme_map = on_off_ratio_extreme  # 开关比（极端值）
                leakage_avg_map[i,j] = leakage_avg  # 平均漏电流
                Vth_map[i,j] = Vth  # 阈值电压

    else:
        raise ValueError('Invalid mode! Please select a valid mode parameter: "single" or "multiple" ! ! !')


    # 可视化模块

    # print(leakage_avg_map)

    scaling_factor = 1e12  # 缩放因子

    plt.figure()

    # 关于seaborn的设置，参考：https://blog.csdn.net/weixin_45492560/article/details/106227864
    # sns.heatmap(leakage_avg_map)
    # sns.heatmap(SS_map*1e3, annot=True, fmt='.0f', cmap='coolwarm', cbar_kws={'label': 'Subthreshold Swing (mV/decade)'})
    # plt.savefig('./data/46/seaborn_heatmap_list.png')
    # plt.close('all')

    # 统计分布图

    # 漏电流
    # leakage_avg = leakage_avg_map.flatten()  # 将二维数组展平为一维数组
    # fig = sns.displot(leakage_avg, kde=True, bins=100, color='blue', rug=True, log_scale=10)
    # fig.set(xlim = (1e-12, 5e-8))

    # 阈值电压
    Vth = Vth_map.flatten()  # 将二维数组展平为一维数组
    print
    fig = sns.displot(Vth, kde=True, bins=20, color='blue', rug=True)

    fig.set(xlim = (0.2, 0.7))

    # sns.displot(leakage_avg*scaling_factor, kde=True, bins=20, color='blue', rug=True)
    # sns.displot(data=leakage_avg, x="bill_length_mm", kind='kde')
    # sns.displot(data=leakage_avg, x="bill_length_mm", kind='ecdf')

    plt.show(block=True)

    exit()