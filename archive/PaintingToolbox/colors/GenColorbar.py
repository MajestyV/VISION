import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(8,1))
    fig.subplots_adjust(bottom=0.5)

    colors = ['#91BBD0', '#0F2F57']
    cmap = mcolors.LinearSegmentedColormap.from_list('cmap', colors, N=8)
    norm = mpl.colors.Normalize(0,1.4)
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm,cmap=cmap), cax=ax, orientation='horizontal', label='Blues')

    #fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    #fig.colorbar(im, cax=cbar_ax)

    saving_directory = 'C:/Users/DELL/Desktop'
    plt.savefig(saving_directory+'/'+'Blues.eps', format='eps', dpi=300)

    plt.show(block=True)