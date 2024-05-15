import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# 画图模块
# 一些用于文章级结果图的matplotlib参数，可以作为matplotlib的全局变量载入
def GlobalSetting(**kwargs):
    '''
    Global setting for matplotlib (全局设置matplotlib参数)
    '''

    # 设置刻度线方向
    plt.rcParams['xtick.direction'] = 'in'  # 将x轴的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度线方向设置向内

    # 确认是否显示刻度线
    bottom_tick = kwargs['bottom_tick'] if 'bottom_tick' in kwargs else True  # 底坐标轴刻度
    top_tick = kwargs['top_tick'] if 'top_tick' in kwargs else False          # 顶坐标轴刻度
    left_tick = kwargs['left_tick'] if 'left_tick' in kwargs else True    # 左坐标轴刻度
    right_tick = kwargs['right_tick'] if 'right_tick' in kwargs else False        # 右坐标轴刻度
    plt.tick_params(bottom=bottom_tick, top=top_tick, left=left_tick, right=right_tick)

    # 设置主次刻度线
    plt.tick_params(which='major', length=5)  # 设置主刻度长度
    plt.tick_params(which='minor', length=2)  # 设置次刻度长度

    if 'figsize' in kwargs:
        plt.figure(figsize=kwargs['figsize'])
    else:
        pass

    # 创建图例对象
    ax = plt.subplot(111)  # 注意有些参数（比如刻度）一般都在ax中设置,不在plot中设置

    # 刻度参数
    x_major_tick = kwargs['x_major_tick'] if 'x_major_tick' in kwargs else 10  # 设置x轴主刻度标签
    y_major_tick = kwargs['y_major_tick'] if 'y_major_tick' in kwargs else 10  # 设置y轴主刻度标签
    x_minor_tick = kwargs['x_minor_tick'] if 'x_minor_tick' in kwargs else x_major_tick / 5.0  # 设置x轴次刻度标签
    y_minor_tick = kwargs['y_minor_tick'] if 'y_minor_tick' in kwargs else y_major_tick / 5.0  # 设置y轴次刻度标签

    # 控制是否关闭坐标轴刻度
    hide_tick = kwargs['hide_tick'] if 'hide_tick' in kwargs else ''  # 控制关闭哪根坐标轴的刻度
    if hide_tick == 'x':
        ax.set_xticks([])  # 设置x轴刻度为空
    elif hide_tick == 'y':
        ax.set_yticks([])  # 设置y轴刻度为空
    elif hide_tick == 'both':
        ax.set_xticks([])  # 设置x轴刻度为空
        ax.set_yticks([])  # 设置y轴刻度为空
    else:
        # 设置主刻度
        x_major_locator = MultipleLocator(x_major_tick)  # 将x主刻度标签设置为x_major_tick的倍数
        y_major_locator = MultipleLocator(y_major_tick)  # 将y主刻度标签设置为y_major_tick的倍数
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        # 设置次刻度
        x_minor_locator = MultipleLocator(x_minor_tick)  # 将x主刻度标签设置为x_major_tick/5.0的倍数
        y_minor_locator = MultipleLocator(y_minor_tick)  # 将y主刻度标签设置为y_major_tick/5.0的倍数
        ax.xaxis.set_minor_locator(x_minor_locator)
        ax.yaxis.set_minor_locator(y_minor_locator)
    # 设置刻度文本选项
    # 控制是否隐藏刻度文本的模块
    hide_ticklabel = kwargs['hide_ticklabel'] if 'hide_ticklabel' in kwargs else ''  # 控制隐藏哪根坐标轴的刻度
    if hide_ticklabel == 'x':
        ax.xaxis.set_ticklabels([])  # 设置x轴刻度标签为空
    elif hide_ticklabel == 'y':
        ax.yaxis.set_ticklabels([])  # 设置y轴刻度标签为空
    elif hide_ticklabel == 'both':
        ax.xaxis.set_ticklabels([])  # 设置x轴刻度标签为空
        ax.yaxis.set_ticklabels([])  # 设置y轴刻度标签为空
    else:
        pass

    # 设置全局字体选项
    # font_type = kwargs['font_type'] if 'font_type' in kwargs else 'Arial'  # 默认字体为sans-serif
    font_type = kwargs['font_type'] if 'font_type' in kwargs else 'sans-serif'  # 默认字体为sans-serif
    font_config = {'font.family': font_type, 'font.weight': 200}  # font.family设定所有字体为font_type
    plt.rcParams.update(font_config)  # 但是对于希腊字母(e.g. α, β, γ等)跟各种数学符号之类的不适用, Latex语法如Γ会被判断为None
    # plt.rcParams['mathtext.default'] = 'regular'  # 可以通过这个选项修改所有希腊字母以及数学符号为Times New Roman
    return