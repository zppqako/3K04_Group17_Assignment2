from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from DCM_serial import receive


class RealTimeDualGraphs:
    def __init__(self, master):
        self.master = master
        self.master.title("Ventricle Graph")

        self.x = []
        self.y2 = []

        self.fig, self.ax2 = plt.subplots()
        self.line2, = self.ax2.plot([], [], label='Ventricle Amplitude(V)')
        self.ax2.legend()

        self.ax2.set_xlabel('Time(ms)')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

        self.master.after(100, self.update_plot)

    def update_plot(self):
        i = len(self.x)
        self.x.append(i)

        _, vent = receive()
        self.y2.append(vent)

        self.line2.set_data(self.x, self.y2)

        self.ax2.relim()
        self.ax2.autoscale_view()

        self.canvas.draw_idle()

        self.master.after(100, self.update_plot)

def create_real_time_dual_graphs_2(master):
    return RealTimeDualGraphs(master)