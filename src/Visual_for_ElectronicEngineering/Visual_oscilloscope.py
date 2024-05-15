import matplotlib.pyplot as plt
# 手动导入，避免循环，提高运行效率
import GetData as gd
import src.FigureSetting as fs



# 命令行解析器模块 --------------------------------------------------------------------------------------------------------
# def

# def SetParser()

if __name__ == '__main__':
    data_directory = 'E:/Projects/EchoStateMachine/Data/ResNode测试/ResNode_20240510/Triangular'  # MMW502
    # input_file = 'SDS2354X_HD_Binary_C1_1_Analog_Trace.csv'
    # output_file = 'SDS2354X_HD_Binary_C3_1_Analog_Trace.csv'

    file_name_list = ['SDS2354X_HD_Binary_C1_1_Analog_Trace.csv',
                      'SDS2354X_HD_Binary_C3_1_Analog_Trace.csv']
                      #'SDS2354X_HD_Binary_C3_2_Analog_Trace.csv',
                      #'SDS2354X_HD_Binary_C3_11_Analog_Trace.csv',]

    # 全局画图设定
    fs.GlobalSetting()

    for i in range(len(file_name_list)):
        data_file = data_directory+ '/' + file_name_list[i]
        data = gd.GetData_Siglent(data_file, max_rows=500, sampling_interval=40000)
        plt.plot(data[:, 0], data[:, 1])

    plt.xlim(data[0, 0], data[-1, 0])  # 设置x轴（时间轴）范围

    plt.show(block=True)




    #data_file = data_directory + '/' + file_name


    # print(data)

    #plt.plot(data[:, 0], data[:, 1])

    #plt.show(block=True)