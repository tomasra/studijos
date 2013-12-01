from matplotlib import animation
from matplotlib import pyplot as plt
from constants import Constants
from helpers import Helpers

# pasiremta:
# http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
class Plot:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = plt.axes(xlim = (0,1), ylim = (-0.5, 2))
        self.line = self.ax.plot([], [], linewidth=2)
        self.time_label = self.ax.text(0.02, 0.90, '', transform=self.ax.transAxes)

    # visi atvaizduojami taskai
    def set_data(self, func_points, time_points):
        self.func_points = func_points
        self.time_points = time_points

    # braizomas grafikas 
    def _plot_one(self, i):
        self.time_label.set_text('t = %.2f' % self.time_points[i])      # laiko momentas
        x, y = Helpers.data_to_xy(self.func_points[i])                  # funkcijos reiksmes tuo laiko momentu
        self.line[0].set_data(x, y)
        return self.line

    def animate(self, speed=1.0):
        interval = 1.0 / (len(self.time_points) / (speed * Constants.t_max)) * 1000.0
        anim = animation.FuncAnimation(self.fig, self._plot_one, init_func=None, frames=len(self.func_points), interval=interval, blit=False)
        plt.grid(True)
        plt.show()
