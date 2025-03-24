import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

# 创建图例
fig = plt.figure(figsize=(14,10))
ax = fig.add_subplot(111,projection='3d')

# 目标函数（target function）
def f(x, y):
    return (x+1)*(x-2)*x*(x+2) + 2*y ** 2

# 目标函数的梯度（gradient）
def df(x, y):
    return [4*x**3 - 3*x**2 - 4*x, 4*y]

def GradientDescent(initial_point, lr, nstep):
    '''
    此函数实现梯度下降算法
    initial_point: 初始点
    lr: learning rate (学习率)
    nstep: 迭代次数
    '''
    traj = np.zeros((nstep+1, 2),dtype=float)  # 轨迹，点数为nstep+1，包含初始点

    x, y = initial_point  # 解压初始的x,y值

    traj[0] = np.array(initial_point)  # 轨迹的起点是初始点
    for i in range(1,nstep+1):
        x = x - lr * df(x, y)[0]  # 梯度下降更新x
        y = y - lr * df(x, y)[1]  # 梯度下降更新y

        traj[i] = np.array([x, y])  # 更新轨迹

    return traj

if __name__ == '__main__':
    # 创建二维网格数据
    x = np.linspace(-2, 2, 30)
    y = np.linspace(-2, 2, 30)

    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    # 梯度下降轨迹（在表面之上部分）
    traj_1 = GradientDescent([0.1, 2], 0.01, 37)
    x_traj_1, y_traj_1 = traj_1[:,0], traj_1[:,1]
    z_traj_1 = f(x_traj_1, y_traj_1)
    # 梯度下降轨迹（在表面之下部分）
    traj_2 = GradientDescent([x_traj_1[-1], y_traj_1[-1]], 0.01, 45)
    x_traj_2, y_traj_2 = traj_2[:,0], traj_2[:,1]
    z_traj_2 = f(x_traj_2, y_traj_2)

    # 绘制轨迹
    descent_traj_1 = ax.plot(x_traj_1, y_traj_1, z_traj_1, color='r', marker='o', markersize=5, zorder=3) # zorder=3表示在表面之上
    descent_traj_2 = ax.plot(x_traj_2, y_traj_2, z_traj_2, color='r', marker='o', markersize=5, zorder=1)  # zorder=2表示在表面之下

    # 绘制loss表面的3D图像
    surface = ax.plot_surface(X, Y, Z, cmap='Blues', edgecolor='none', antialiased=False, alpha=.5)

    # 设置loss表面的色条
    fig.colorbar(surface, shrink=0.5, aspect=5)



    # 增加指向向量
    #px = 2
    #py = 1.5
    #P = [px, py, f(px, py)]

    #Q = [1.5, 2, 1]

    #ax.quiver(*P, *Q, color='r')  # we change color for better visualization

    # 保存图像
    saving_directory = 'D:/PhD_research/ESN4Science/Figures/Pycharm_gallery'  # Lingjiang
    title = 'GradientDescent'
    plt.savefig(saving_directory + '/' + title + '.pdf', dpi=100)

    plt.show(block=True)