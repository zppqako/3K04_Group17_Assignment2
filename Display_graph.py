import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from DCM_serial import receive


class RealTimeDualGraphs:
    def __init__(self, master):
        self.master = master
        self.master.title("Real-time Dual Graphs")

        self.x = []
        self.y1 = []
        self.y2 = []

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.line1, = self.ax1.plot([], [], label='Input 1')
        self.line2, = self.ax2.plot([], [], label='Input 2')
        self.ax1.legend()
        self.ax2.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        self.master.after(100, self.update_plot)

    def update_plot(self):
        i = len(self.x)
        self.x.append(i)

        atr, vent = receive()
        if atr < 5:
            atr = 0
        self.y2.append(atr)
        self.y2.append(vent)

        self.line1.set_data(self.x, self.y1)
        self.line2.set_data(self.x, self.y2)
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()

        self.canvas.draw_idle()

        self.master.after(100, self.update_plot)

def create_real_time_dual_graphs(master):
    return RealTimeDualGraphs(master)
# root = tk.Tk()
#
# real_time_dual_graphs = RealTimeDualGraphs(root)
#
# root.mainloop()