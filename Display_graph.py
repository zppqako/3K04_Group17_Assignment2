import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from DCM_serial import receive

# class RealTimeSineWave:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Real-time Sine Wave")
#
#         # 初始化空的 x 和 y 列表
#         self.x = []
#         self.y = []
#
#         # 创建 Matplotlib 图表
#         self.fig, self.ax = plt.subplots()
#         self.line, = self.ax.plot([], [], label='Sine Wave')
#         self.ax.legend()
#
#         # 创建 Canvas 组件
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
#         self.canvas.get_tk_widget().pack()
#
#         # 打开交互模式
#         self.master.after(100, self.update_plot)  # 定时更新图表
#
#     def update_plot(self):
#         # 生成新的 x 和 y 值
#         i = len(self.x)
#         self.x.append(i)
#         y = np.sin(i / 10)  # sine wave 的生成方式
#         self.y.append(y)
#
#         # 更新折线图
#         self.line.set_data(self.x, self.y)
#         self.ax.relim()
#         self.ax.autoscale_view()
#
#
#         self.canvas.draw_idle()
#
#
#         self.master.after(100, self.update_plot)
#
#
#
# root = tk.Tk()
#
#
# real_time_sine_wave = RealTimeSineWave(root)
#
#
# root.mainloop()
class RealTimeDualGraphs:
    def __init__(self, master):
        self.master = master
        self.master.title("Real-time Dual Graphs")

        self.x = []
        self.y1 = []
        self.y2 = []

        # self.input1 = input1
        # self.input2 = input2

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
        # y1 = self.input1
        # y2 = self.input2
        
        atr, vent = receive()
        
        self.y1.append(atr)
        self.y2.append(vent)

        self.line1.set_data(self.x, self.y1)
        self.line2.set_data(self.x, self.y2)
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()

        self.canvas.draw_idle()

        self.master.after(100, self.update_plot)



root = tk.Tk()




real_time_dual_graphs = RealTimeDualGraphs(root)


root.mainloop()
