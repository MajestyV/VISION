import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.special import sph_harm, genlaguerre
from src.colors import iColormap

def Hydrogen_Wavefunction(n, l, m, X, Y, Z):
    ''' Calculate the hydrogen atom wave function '''

    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    theta = np.arccos(Z / r)
    phi = np.arctan2(Y, X)

    rho = 2. * r / n
    s_harm = sph_harm(m, l, phi, theta)
    l_poly = genlaguerre(n - l - 1, 2 * l + 1)(rho)

    prefactor = np.sqrt((2. / n) ** 3 * math.factorial(n - l - 1) / (2. * n * math.factorial(n + l)))
    wavefunc = prefactor * np.exp(-rho / 2.) * rho ** l * s_harm * l_poly
    wavefunc = np.nan_to_num(wavefunc)
    return wavefunc

if __name__ == '__main__':
    dz = 0.2
    zmin = -15
    zmax = 15
    x = np.arange(zmin, zmax, dz)
    y = np.arange(zmin, zmax, dz)
    z = np.arange(zmin, zmax, dz)
    X, Y, Z = np.meshgrid(x, y, z)
    # X, Y, Z are 3d arrays that tell us the values of x, y, and z at every point in space

    # Change these to change which orbital to plot
    n = 2
    l = 0
    m = 0

    data = Hydrogen_Wavefunction(n, l, m, X, Y, Z)
    data = abs(data) ** 2

    max_val = np.max(data[int((0 - zmin) / dz), :, :])
    print(np.log10(max_val))
    print(data[int((0 - zmin) / dz), 0, 0])

    R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)

    fig, ax = plt.subplots()
    plt.axis('off')

    plt.subplots_adjust(left=0.15, bottom=0.15)
    # plt.imshow(data[int((0 - zmin) / dz), :, :], vmin=0, vmax=max_val, cmap='bwr', extent=[zmin, zmax, zmin, zmax])
    plt.imshow(data[int((0 - zmin) / dz), :, :], norm=mcolors.LogNorm(vmin=10**(-4.5),vmax=max_val), cmap=iColormap['Blues'], extent=[zmin, zmax, zmin, zmax])
    plt.axis('off')
    # plt.colorbar()
    # sli = Slider(plt.axes([0.25, 0.025, 0.65, 0.03]), "Y", z[0], z[len(z) - 1], valinit=0)
    ax.set_title("Hydrogen Orbital xz Slice : n=" + str(n) + ", l=" + str(l) + ", m=" + str(m))

    # plt.show(block=True)

    saving_dir = 'C:/Users/DELL/Desktop'
    plt.savefig(f"{saving_dir}/HydrogenOrbital.png", dpi=300)
    plt.show(block=True)
