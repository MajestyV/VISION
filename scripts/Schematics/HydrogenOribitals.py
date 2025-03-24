import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from src import Quantus
from src.Visual.colors import iColormap

# 量子数列表
orbital_list = [(1,0,0),
                (2,0,0), (3,0,0),
                (2,1,0), (3,1,0), (3,1,1),
                (2,1,1), (3,2,0), (3,2,1), (3,2,2),
                (4,0,0), (4,1,0), (4,1,1), (4,2,0), (4,2,1),
                (4,2,2), (4,3,0), (4,3,1), (4,3,2), (4,3,3)]

# 画图区域参数
ploting_list = [(-17,17,0.2),
                (-17,17,0.2),(-17,17,0.2),
                (-17,17,0.2),(-17,17,0.2),(-17,17,0.2),
                (-34,34,0.4),(-34,34,0.4),(-34,34,0.4),(-34,34,0.4),
                (-34,34,0.4),(-34,34,0.4),(-34,34,0.4),(-34,34,0.4),(-34,34,0.4),
                (-34,34,0.4),(-34,34,0.4),(-34,34,0.4),(-34,34,0.4),(-34,34,0.4)]


num_map_list = [1,3,6,10,15,20]  # 不同阶数生成的轨道数目

if __name__ == '__main__':

    # 可视化模块
    n_order = 4
    n_map = num_map_list[n_order-1]  # 生成的轨道数目

    # 生成图像坐标列表
    map_coord_list = []
    i = 0  # 初始化计数器
    while i < n_order:
        for j in range(i+1):  # 生成每一层的坐标
            map_coord_list.append((i, -j-1))

        i += 1  # 计数器自增

    print(map_coord_list)

    map_hash = dict()  # 初始化哈希表
    area_hash = dict()  # 初始化面积哈希表
    for n in range(n_map):
        map_hash[map_coord_list[n]] = orbital_list[n]
        area_hash[map_coord_list[n]] = ploting_list[n]

    # 生成图像
    fig, axes = plt.subplots(nrows=n_order, ncols=n_order, figsize=(10, 10))
    fig.subplots_adjust(hspace=0., wspace=0.)

    # 关闭所有子图坐标轴
    for i in range(n_order):
        for j in range(n_order):
            axes[i, j].axis('off')

    for map in map_hash:
        # 创建一个三维网格
        # zmin, zmax, dz = area_hash[map]
        zmin, zmax, half_width = -17, 17, 100
        x = np.concatenate((np.linspace(zmin, 0, half_width), np.linspace(0, zmax, half_width)))  # 保证计算xOz面的投影
        y = np.concatenate((np.linspace(zmin, 0, half_width), np.linspace(0, zmax, half_width)))
        z = np.concatenate((np.linspace(zmin, 0, half_width), np.linspace(0, zmax, half_width)))
        X, Y, Z = np.meshgrid(x, y, z)
        # X, Y, Z are 3d arrays that tell us the values of x, y, and z at every point in space

        n, l, m = map_hash[map]
        data = Quantus.Hydrogen_Wavefunction(n, l, m, X, Y, Z)
        data = abs(data) ** 2
        proj_xz = data[half_width, :, :]

        max_val = np.max(proj_xz)

        R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)

        ax = axes[map]
        ax.imshow(proj_xz, norm=mcolors.LogNorm(vmin=10**(-4.5),vmax=max_val), cmap=iColormap['Blues'], extent=[zmin, zmax, zmin, zmax])


    for fmt in ['eps', 'pdf', 'png']:
        saving_dir = 'C:/Users/DELL/Desktop'
        plt.savefig(f"{saving_dir}/HydrogenOrbital.{fmt}", dpi=300)

    plt.show(block=True)





    # Change these to change which orbital to plot
    # n = 1
    # l = 0
    # m = 0

    # data = Quantus.Hydrogen_Wavefunction(n, l, m, X, Y, Z)
    # data = abs(data) ** 2

    # max_val = np.max(data[int((0 - zmin) / dz), :, :])
    # print(np.log10(max_val))
    # print(data[int((0 - zmin) / dz), 0, 0])

    # R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)

    # fig, ax = plt.subplots()
    # plt.axis('off')

    # plt.subplots_adjust(left=0.15, bottom=0.15)
    # plt.imshow(data[int((0 - zmin) / dz), :, :], vmin=0, vmax=max_val, cmap='bwr', extent=[zmin, zmax, zmin, zmax])
    # plt.imshow(data[int((0 - zmin) / dz), :, :], norm=mcolors.LogNorm(vmin=10**(-4.5),vmax=max_val), cmap=iColormap['Blues'], extent=[zmin, zmax, zmin, zmax])
    # plt.axis('off')
    # plt.colorbar()
    # sli = Slider(plt.axes([0.25, 0.025, 0.65, 0.03]), "Y", z[0], z[len(z) - 1], valinit=0)
    # ax.set_title("Hydrogen Orbital xz Slice : n=" + str(n) + ", l=" + str(l) + ", m=" + str(m))

    # plt.show(block=True)

    # saving_dir = 'C:/Users/DELL/Desktop'
    # plt.savefig(f"{saving_dir}/HydrogenOrbital.png", dpi=300)
    # plt.show(block=True)
