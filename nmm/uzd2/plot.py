from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt

from settings import Input

class Plot:
    # funkcijos kompleksiniu reiksmiu atvaizdavimas
    def plot(self, f):
        fig = plt.figure()
        ax = Axes3D(fig)
        x = Input.x_range
        z, y = Plot.complex_to_xy(f)
        ax.plot(xs=x, ys=y, zs=z, zdir='z', label='ys=0, zdir=z')
        # ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.show()

    # kompleksiniu skaiciu masyvo isskaidymas i du atskirus su realiosiomis ir menamosiomis dalimis
    @staticmethod
    def complex_to_xy(c_list):
        x = [c.real for c in c_list]
        y = [c.imag for c in c_list]
        return x, y
