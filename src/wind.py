import pyvista as pv

CHECKBOX_SIZE = 40
SPACING = 10


class Wind:
    def __init__(self, plotter: pv.Plotter, initial_time_step: int = 1):
        self.plotter = plotter

        file_name = "data/wind.vtk"
        print(f"Reading file '{file_name}'")
        self.data = pv.read(file_name)
        self.wind_n_points = 350
        self.curr_time_step = initial_time_step
        self.enabled = True

        self.plotter.add_slider_widget(self.__update_streamlines, [100, 1000], title='Streamline Points',
                                       value=self.wind_n_points, pointa=(0.6, 0.1), pointb=(0.95, 0.1),
                                       fmt="%0.0f", style='modern')

        self.plotter.add_checkbox_button_widget(self.__toggle, value=self.enabled, color_on='blue', color_off='#000000',
                                                size=CHECKBOX_SIZE, position=(SPACING, 2 * CHECKBOX_SIZE + 3 * SPACING))
        self.plotter.add_text(text="Wind", position=(CHECKBOX_SIZE + 2 * SPACING, 2 * CHECKBOX_SIZE + 3 * SPACING))
        return

    def update_time_frame(self, time_step: int):
        print("\tUpdate wind")
        self.curr_time_step = time_step
        self.__plot_streamlines()
        print("\tFinished updating wind\n")
        return

    def __plot_streamlines(self):
        if self.enabled:
            print("\tCreating wind streamlines")
            streamlines = self.data.streamlines(vectors=f"wind{self.curr_time_step:02d}", source_radius=700,
                                                n_points=self.wind_n_points)
            print("\tAdding wind streamlines")
            self.plotter.add_mesh(streamlines.tube(radius=1.0), scalars = f"mag{self.curr_time_step:02d}",show_scalar_bar=False, name="streamline-tubes")
        else:
            print("\tRemoving wind streamlines")
            self.plotter.remove_actor("streamline-tubes")

        return

    def __update_streamlines(self, value):
        print("\tUpdate streamline points")
        self.wind_n_points = int(value)
        self.__plot_streamlines()
        print("\tFinished updating streamline points\n")
        return

    def __toggle(self, enabled: bool):
        self.enabled = enabled
        self.__plot_streamlines()