import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from os import path

class plot:
    """ This class of functions is designed to plot scientific figures in a uniform format."""
    def __init__(self):
        self.name = plot
        self.default_directory = path.dirname(__file__) + '/'  # 设置这个代码文件所在的文件夹为默认读写目录

    ###############################################################################################################
    # 颜色模块
    # RGB值转换函数
    def RGB(self,r,g,b): return np.array([r,g,b])/255.0  # 将RGB值归一化的函数，只有归一化的RGB值才能被matplotlib读取

    # 此函数可以转换CMYK色值到RGB色值
    def CMYK_to_RGB(self,c, m, y, k, cmyk_scale=100, rgb_scale=255):
        r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
        return np.array([r, g, b])/255.0

    # 常用配色
    def Color(self,mode):
        color_dict = {
                      'Black_n_Red': [self.RGB(7,7,7),self.RGB(255,59,59)],
                      'Red_n_Black': [self.RGB(255,59,59),self.RGB(7,7,7)],
                      'Blue_n_Grey': [self.RGB(57, 83, 163),self.RGB(92,92,92)],
                      'Three_contrast_OldFashion': [self.RGB(7, 7, 7), self.RGB(57, 83, 163), self.RGB(255, 59, 59)],
                      'Red_n_Blue': [self.RGB(239,76,77),self.RGB(70,148,203)],
                      'Red_n_Grey': [self.RGB(239,76,77),self.RGB(92,92,92)],
                      'Three_contrast': [self.RGB(7,7,7),self.RGB(57,83,163),self.RGB(239,76,77)],
                      'One_color': [self.RGB(7,7,7)],
                      'Two_color': [self.RGB(254,129,125),self.RGB(129,184,223)],
                      'Three_color': [self.RGB(77,133,189),self.RGB(247,144,61),self.RGB(89,169,90)],
                      'Four_color': [self.RGB(23,23,23),self.RGB(6,223,6),self.RGB(255,28,0),self.RGB(0,37,255)],
                      'Five_color': [self.RGB(1,86,153),self.RGB(250,192,15),self.RGB(243,118,74),
                                     self.RGB(95,198,201),self.RGB(79,89,109)]
                      }
        return color_dict[mode]

    # 莫兰迪色系
    def MorandiColor(self,mode,**kwargs):
        c, m, y, k =  kwargs['cmyk'] if 'cmyk' in kwargs else (1,1,1,1)      # 测试色值，通过输入这个值可以方便地测试新颜色的效果
        c1,m1,y1,k1 = kwargs['custom'] if 'custom' in kwargs else (1,1,1,1)  # 自定义色值，通过这个值可以输入自定义颜色

        color_dict = {
                      'Testing':    self.CMYK_to_RGB(c,m,y,k),
                      'Custom':     self.CMYK_to_RGB(c1,m1,y1,k1),
                      'Black':      self.CMYK_to_RGB(80,72,69,36),
                      'Pinkgrey':   self.CMYK_to_RGB(0,10,10,30),
                      'Grey':       self.CMYK_to_RGB(0,0,0,54),
                      'Lightgrey':  self.CMYK_to_RGB(0,0,0,33),
                      'Deepgrey':   self.CMYK_to_RGB(0,0,0,73),
                      'Darkgrey':   self.CMYK_to_RGB(0,0,0,83),
                      'Orangered':  self.CMYK_to_RGB(0,81,81,30),
                      'Redred':     self.CMYK_to_RGB(0,90,90,10),
                      'Red':        self.CMYK_to_RGB(0,75,75,35),
                      'Wine':       self.CMYK_to_RGB(0,69,51,42),
                      'Green':      self.CMYK_to_RGB(67,50,62,0),
                      'Spring':     self.CMYK_to_RGB(32,22,27,0),
                      'Forrest':    self.CMYK_to_RGB(87,70,82,0),
                      'Blue':       self.CMYK_to_RGB(78,65,44,3),
                      'Lightblue':  self.CMYK_to_RGB(30,20,8,8),
                      'Deepblue':   self.CMYK_to_RGB(86,73,46,8),
                      'Paris':      self.CMYK_to_RGB(80,70,48,8),
                      'Magicblue':  self.CMYK_to_RGB(43,19,0,13),
                      'Purpleblue': self.CMYK_to_RGB(40,30,8,8),
                      'Red_n_Black': (self.CMYK_to_RGB(0,90,90,10),self.CMYK_to_RGB(80,72,69,36)),
                      'Five_color': (self.CMYK_to_RGB(0,32,38,38),self.CMYK_to_RGB(0,22,31,25),
                                     self.CMYK_to_RGB(16,28,0,22),self.CMYK_to_RGB(0,26,28,12),
                                     self.CMYK_to_RGB(6,21,0,51)),
                      'Colormap_grey':   (self.CMYK_to_RGB(0,0,0,33),self.CMYK_to_RGB(0,0,0,83)),
                      'Colormap_red':    (self.CMYK_to_RGB(0,10,10,30),self.CMYK_to_RGB(0,81,81,30)),
                      'Colormap_green':  (self.CMYK_to_RGB(32,22,27,0),self.CMYK_to_RGB(87,70,82,0)),
                      'Colormap_blue':   (self.CMYK_to_RGB(30,20,8,8),self.CMYK_to_RGB(80,70,48,8))
                      }

        return color_dict[mode]
