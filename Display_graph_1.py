import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time
from DCM_serial import receive
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RealTimeDualGraphs:
    def __init__(self, master):
        self.master = master
        self.master.title("Atrium Graph")

        self.x = []
        self.y1 = []

        self.fig, self.ax1 = plt.subplots()
        self.line1, = self.ax1.plot([], [], label='Atrium Amplitude(V)')
        self.ax1.legend()

        self.ax1.set_xlabel('Time(ms)')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        self.master.after(100, self.update_plot)

    def update_plot(self):
        i = len(self.x)
        self.x.append(i)

        atr,_ = receive()
        self.y1.append(atr)


        self.line1.set_data(self.x, self.y1)
        self.ax1.relim()
        self.ax1.autoscale_view()


        self.canvas.draw_idle()

        self.master.after(100, self.update_plot)

def create_real_time_dual_graphs_1(master):
    return RealTimeDualGraphs(master)
