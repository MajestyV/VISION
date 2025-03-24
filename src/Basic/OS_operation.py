import os      # 导入 os 模块
import shutil  # 导入 shutil 模块

def Select_files_by_extension(directory: str, extension: str, returning_absolute_path: bool=False) -> list:
    ''' 此函数用于按照文件扩展名来选择文件 '''
    file_list = os.listdir(directory)                     # 获取文件夹中所有文件的名称

    selected_files = []                                   # 创建一个空列表用于存储符合条件的文件名
    for file in file_list:                                # 遍历文件夹中的所有文件
        file_path_abs = f'{directory}/{file}'             # 获取文件的绝对路径
        if not os.path.isfile(file_path_abs):             # 如果当前文件格式不是一个文件，则跳过
            continue
        elif file.startswith('.'):                        # 忽略隐藏文件
            continue
        else:
            if file.endswith(extension):                  # 如果当前文件的扩展名符合条件
                if returning_absolute_path:
                    selected_files.append(file_path_abs)  # 添加文件绝对路径到选中文件列表
                else:
                    selected_files.append(file)           # 添加文件名到选中文件列表

    return selected_files

if __name__ == '__main__':
    testing_path_1 = 'E:/PhD_research/Jingfang Pei/Solution-processed IC/Data/KEITHLEY4200/20250323 sol ic 5x20_preview/1_to_20'  # 测试路径

    print(Select_files_by_extension(testing_path_1, 'xls', returning_absolute_path=True))  # 测试选择文件