import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(6,1))
    fig.subplots_adjust(bottom=0.5)

    cmap = mpl.cm.nipy_spectral
    norm = mpl.colors.Normalize(380,780)
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm,cmap=cmap), cax=ax, orientation='horizontal', label='Spectra')

    #fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    #fig.colorbar(im, cax=cbar_ax)

    plt.show(block=True)
