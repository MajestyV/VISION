import matplotlib.pyplot as plt
# 手动导入，避免循环，提高运行效率
import GetData as gd
import src.FigureSetting as fs



# 命令行解析器模块 --------------------------------------------------------------------------------------------------------
# def

# def SetParser()

if __name__ == '__main__':
    # data_directory = 'E:/Projects/EchoStateMachine/Data/ResNode测试/ResNode_20240510/Triangular'  # MMW502
    # data_directory = 'E:/Projects/EchoStateMachine/Data/ResNode测试/Activation/Raw data'  # MMW405
    # data_directory = 'E:/Projects/EchoStateMachine/Data/ResNode测试/Temperary'
    # data_directory = 'D:/PhD_research/EchoStateMachine/Data/ResNode/Triangular'  # Lingjiang
    # input_file = 'SDS2354X_HD_Binary_C1_1_Analog_Trace.csv'
    # output_file = 'SDS2354X_HD_Binary_C3_1_Analog_Trace.csv'

    working_loc_key = 'MMW405_RO'

    data_dir_dict = {'MMW405_RO': 'E:/Projects/Jingfang Pei/Solution-processed IC/Data/OSC/RingOscillator/20240711/csv'}

    file_name_list = ['SDS2354X_HD_Binary_C3_1_Analog_Trace.csv',
                      'SDS2354X_HD_Binary_C3_2_Analog_Trace.csv',
                      # 'SDS2354X_HD_Binary_C3_3_Analog_Trace.csv',
                      'SDS2354X_HD_Binary_C3_4_Analog_Trace.csv',
                      'SDS2354X_HD_Binary_C3_5_Analog_Trace.csv']
                      #'SDS2354X_HD_Binary_C3_2_Analog_Trace.csv',
                      #'SDS2354X_HD_Binary_C3_11_Analog_Trace.csv',]

    extration_param = [(400000, 1), (200000, 1), (400000, 1), (400000, 1)]

    # 全局画图设定
    fs.GlobalSetting()

    plt.figure(figsize=(10, 6))

    for i in range(len(file_name_list)):
        data_file = f"{data_dir_dict[working_loc_key]}/{file_name_list[i]}"
        # print(data_file)

        num_rows, sampling_interval = extration_param[i]

        data = gd.GetData_Siglent(data_file, num_rows=num_rows, sampling_interval=sampling_interval)

        ax = plt.subplot(len(file_name_list), 1, i+1)  # 分配子图位置

        ax.plot(data[:, 0], data[:, 1])

        ax.set_xlim(data[0, 0], data[-1, 0])  # 设置x轴（时间轴）范围

        ax.spines['top'].set_visible(False)  # 隐藏上边框
        ax.spines['right'].set_visible(False)  # 隐藏右边框

    plt.tight_layout()  # 调整子图之间的间距

    plt.show(block=True)  # 显示图像




    #data_file = data_directory + '/' + file_name


    # print(data)

    #plt.plot(data[:, 0], data[:, 1])

    #plt.show(block=True)