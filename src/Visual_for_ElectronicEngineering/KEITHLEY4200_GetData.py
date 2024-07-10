# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

def GetData_KEITHLEY4200_OldModel(data_file: str, sheets_ignored: list=('Calc', 'Settings')):
    '''
    从KEITHLEY4200旧型号中获取数据
    '''
    # 读取数据
    excel_file = pd.ExcelFile(data_file)
    sheet_names = excel_file.sheet_names  # 获取所有的sheet名称
    for n in sheets_ignored:  # 删除不需要的sheet
        sheet_names.remove(n)

    data_list = []  # 创建一个空列表，用于存储数据
    for data in sheet_names:
        data_DF = pd.read_excel(excel_file, sheet_name=data)  # 读取数据（DF - DataFrame）
        data_list.append(data_DF)

    return data_list

if __name__ == '__main__':
    # 数据路径
    data_directory = 'D:/Projects/Jingfang Pei/Solution-processed IC/Data/4200/20240708 tft 10x10 array'
    data_file = 'line_1.xls'

    # 获取数据
    # for i in


    # Read the data
    #df = pd.read_csv('data/KEITHLEY4200/Keithley4200_1.csv')
    #print(df.head())
    # Plot the data
    #df.plot(x='Time', y='V1', kind='line')

    # 画图模块
    # plt.show(block=True)



