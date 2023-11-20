import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from itertools import count


class RealTimeSineWave:
    def __init__(self, master):
        self.master = master
        self.master.title("Real-time Sine Wave")

        # 初始化空的 x 和 y 列表
        self.x = []
        self.y = []

        # 创建 Matplotlib 图表
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], label='Sine Wave')
        self.ax.legend()

        # 创建 Canvas 组件
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        # 打开交互模式
        self.master.after(100, self.update_plot)  # 定时更新图表

    def update_plot(self):
        # 生成新的 x 和 y 值
        i = len(self.x)
        self.x.append(i)
        y = np.sin(i / 10)  # sine wave 的生成方式
        self.y.append(y)

        # 更新折线图
        self.line.set_data(self.x, self.y)
        self.ax.relim()
        self.ax.autoscale_view()

        # 手动触发图形更新
        self.canvas.draw_idle()

        # 定时更新图表
        self.master.after(100, self.update_plot)


# 创建主窗口
root = tk.Tk()

# 创建 RealTimeSineWave 实例
real_time_sine_wave = RealTimeSineWave(root)

# 启动主循环
root.mainloop()