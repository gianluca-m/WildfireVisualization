import pyvista as pv
import matplotlib.pyplot as plt
import pandas as pd

CHECKBOX_SIZE = 40
SPACING = 10
x = [i for i in range(1, 16)]


class Charts2d:
    def __init__(self, plotter: pv.Plotter, initial_time):
        self.plotter = plotter
        self.enabled = False

        self.data = pd.read_csv('data/chart_data.csv', sep=',')

        fig = plt.figure(tight_layout=True)
        ax0, ax1, ax2, ax3 = fig.subplots(4, 1)
        fig.tight_layout()
        self.time_axes = [
            self.__add_subplot("theta_max", [273, 1000], "K", "Maximum Temperature", initial_time, ax0),
            self.__add_subplot("wind_max", [23.0, 30.0], "km/h", "Maximum Wind Speed", initial_time, ax1),
            self.__add_subplot("wind_avg", [12.0, 14.0], "km/h", "Average Wind Speed", initial_time, ax2),
            self.__add_subplot("rhof_1_sum", [27733.0, 27745.0], "kg/m$^3$", "Total bulk density", initial_time, ax3),
        ]
        self.histograms = pv.ChartMPL(fig, size=(0.25, 0.8), loc=(0.75, 0.2))
        self.histograms.background_color = (1.0, 1.0, 1.0, 0.5)

        self.plotter.add_checkbox_button_widget(self.__toggle, value=self.enabled, color_on='#00FFFF', color_off='#000000',
                                                size=CHECKBOX_SIZE, position=(SPACING, 5 * CHECKBOX_SIZE + 6 * SPACING))
        self.plotter.add_text(text="Histograms", position=(CHECKBOX_SIZE + 2 * SPACING, 5 * CHECKBOX_SIZE + 6 * SPACING))
        return

    def update_time_frame(self, time_frame):
        if self.enabled:
            self.plotter.remove_chart(self.histograms)

        print("\tUpdating plot timestamps")
        for time_axis in self.time_axes:
            time_axis[0].set_xdata([time_frame, time_frame])

        if self.enabled:
            self.__plot()

        plt.close('all')
        return

    def __toggle(self, enabled: bool):
        self.enabled = enabled
        self.__plot()
        return

    def __add_subplot(self, scalar, y_lim, y_label, title, curr_time, ax):
        y = self.data[scalar]
        ax.set_title(title)
        ax.plot(x, y)
        curr_time_axis = ax.plot([curr_time, curr_time], y_lim)
        ax.set_ylim(y_lim)
        ax.set_xlabel("Timestep")
        ax.set_ylabel(y_label)
        ax.set_xlim(left=x[0], right=x[-1])
        ax.set_xticks([i for i in range(x[0], x[-1]+1, 2)])
        return curr_time_axis

    def __plot(self):
        if self.enabled:
            self.plotter.add_chart(self.histograms)
        else:
            self.plotter.remove_chart(self.histograms)
        return
