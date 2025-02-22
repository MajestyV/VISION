# 此函数可以利用matplotlib自定义创建色谱（colormap），用于热度图等，需要连续变化色值的场景
import numpy as np
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import cm
import seaborn as sns
# from matplotlib.colors import Normalize,ListedColormap, LinearSegmentedColormap
from matplotlib.colors import ListedColormap,LinearSegmentedColormap

##########################################################
# Abbreviation:                                          #
# cmap - colormap，色谱                                   #
# nbins - number of bins，指定了颜色节点间插颜色值的数目       #
##########################################################

# 自定义色谱
Tron = LinearSegmentedColormap.from_list('Tron', np.array([[1., 1., 0.], [0.953, 0.490, 0.016], [0., 0., 0.], [0.176, 0.976, 0.529], [0., 1., 1.]]))  # 创战记

Blues = LinearSegmentedColormap.from_list('Blues', ['#FFFFFF', '#E8F1FA', '#C0D9ED', '#88BDDC', '#559FCE', '#1862A9', '#08478E', '#102F5D'])  # 蓝调
Blues_sns = LinearSegmentedColormap.from_list('Blues_sns', sns.color_palette('Blues').as_hex())  # 蓝调（seaborn版本）

Blue_n_Red = LinearSegmentedColormap.from_list('Red_n_Blue', ['#2EA7E0', '#FFFFFF', '#E83828'])  # 蓝红
Cool_n_Warm = LinearSegmentedColormap.from_list('Cool_n_Warm', ['#2EA7E0', '#8B7084', '#E83828'])  # 冷暖

# 黎明
Dawn = LinearSegmentedColormap.from_list('Dawn', ['#4D6098', '#5F70A8', '#757FB4', '#9593C4', '#B7A5CD',
                                                  '#DAB4CD', '#F1C5C4', '#FACE9F', '#F1AD88', '#F09671',
                                                  '#E3815C', '#D36C49', '#C45633', '#B5401F', '#AF3D22'])


iColormap = {'Tron': Tron,
             'Blues': Blues, 'Blues_sns': Blues_sns,
             'Blue_n_Red': Blue_n_Red, 'Cool_n_Warm': Cool_n_Warm,
             'Dawn': Dawn}

if __name__ == '__main__':
    print(sns.color_palette('Blues').as_hex())