# User Guidance

## I. Prerequisite

The use of [anaconda](https://www.anaconda.com/) for environment management is highly recommended.

## II. Scripts

本代码内含了一系列方便用于光电子器件及硬件系统的数据分析模块，可以用过脚本进行快速调用分析。所有的脚本都可以在终端（terminal or cmd for windows）中通过命令行调用。其中一部分脚本的使用方法如下所示。

### A. Frequency analysis (频谱分析)

```cmd
> python FrequencyAnalysis.py -h
usage: FrequencyAnalysis.py [-h] [--working_place -W] [--file_name -F] [--data_format -T] [--drop_out -D]
                            [--drop_out_ratio -R] [--window_func -W] [--fig_size -S] [--time_unit -TU]
                            [--freq_unit -FU] [--set_freq_range -SFR] [--freq_range -FR] [--power_spectrum_method -M]
                            [--figure_format -FF] [--figure_quality -DPI]

options:
  -h, --help            show this help message and exit
  --working_place -W    Working place
  --file_name -F        File name
  --data_format -T      File type
  --drop_out -D         Drop out zero frequency
  --drop_out_ratio -R   Drop out ratio
  --window_func -W      Window function
  --fig_size -S         Figure size
  --time_unit -TU       Time unit
  --freq_unit -FU       Frequency unit
  --set_freq_range -SFR
                        Set frequency range
  --freq_range -FR      Frequency range
  --power_spectrum_method -M
                        Power spectrum method
  --figure_format -FF   Figure format
  --figure_quality -DPI
                        Figure quality
```

Below is an example command:

```
> python FrequencyAnalysis.py --file_name Empty --drop_out True --drop_out_ratio 0.05 --time_unit m --freq_unit M --set_freq_range True
```



## Problems & solutions

### i. ImportError: cannot import name ‘animation‘ from partially initialized module ‘matplotlib’

在Pycharm等IDE中运行正常的代码，在本地的cmd运行python code出现了一个错误：

```cmd
ImportError: cannot import name ‘animation’ from partially initialized module ‘matplotlib’ (most likely due to a circular import)
```

这很可能是由于python调用了windows本机的python引起的。我本地的环境anaconda是放在E盘的。但报错显示的C盘里的matplotlib没有找到animation的模块。说明，import之后，系统到C盘去导入这个库，所以即使你重装升级都没用。此时，如果我们进入到conda环境中去查看默认的python版本的话，会发现：

```
> where python
E:\Anaconda\Anaconda3\envs\python3.10\python.exe
C:\Users\Majes\AppData\Local\Microsoft\WindowsApps\python.exe
```

本机的python环境以及conda中的环境其实都被调用了。那么很简单，[把本机python卸载](https://answers.microsoft.com/zh-hans/windows/forum/all/%E6%97%A0%E6%B3%95%E5%8D%B8%E8%BD%BD%E6%9D%A5/8a4f4465-85af-415a-9526-8c148178b45a)完事。辣鸡Microsoft，Anaconda YYDS！！！

详情可参考：https://blog.csdn.net/weixin_42326545/article/details/127368928