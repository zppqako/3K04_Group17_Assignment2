import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from DCM_serial import receive


def plot_atrium():
    x = []
    y1 = []

    fig, ax = plt.subplots()
    line1, = ax.plot([], [], label='Atrium')
    ax.legend()

    def update_plot():
        i = len(x)
        x.append(i)

        atr, _ = receive()  # Assuming receive() returns data for Input 1 and Input 2
        y1.append(atr)

        line1.set_data(x, y1)
        ax.relim()
        ax.autoscale_view()

        canvas.draw_idle()
        root.after(100, update_plot)

    update_plot()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()


def plot_ventricle():
    x = []
    y2 = []

    fig, ax = plt.subplots()
    line2, = ax.plot([], [], label='Ventricle')
    ax.legend()

    def update_plot():
        i = len(x)
        x.append(i)

        _, vent = receive()  # Assuming receive() returns data for Input 1 and Input 2
        y2.append(vent)

        line2.set_data(x, y2)
        ax.relim()
        ax.autoscale_view()

        canvas.draw_idle()
        root.after(100, update_plot)

    update_plot()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()


root = tk.Tk()


root.mainloop()
