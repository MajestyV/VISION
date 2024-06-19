import matplotlib.pyplot as plt

if __name__ == '__main__':
    red = (1, 0, 0)
    pink = (1, 0.9, 0.9)
    for i in range(200):
        plt.plot(record[i], color=interpolateColor(pink, red, i / 200))
