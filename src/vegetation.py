import pyvista as pv

CHECKBOX_SIZE = 40
SPACING = 10


class Vegetation:
    def __init__(self, plotter: pv.Plotter):
        self.plotter = plotter
        self.enabled = True
        self.data: pv.PolyData = pv.PolyData()
        self.burnt_terrain: pv.PolyData = pv.PolyData()

        file_name = 'data/vegetation.vtk'
        print(f"Reading file '{file_name}'")
        self.all_vegetation = pv.read(file_name)

        self.plotter.add_checkbox_button_widget(self.__toggle, value=self.enabled, color_on='#00FF00', color_off='#000000',
                                                size=CHECKBOX_SIZE, position=(SPACING,3 * CHECKBOX_SIZE + 4 * SPACING))
        self.plotter.add_text(text="Vegetation", position=(CHECKBOX_SIZE + 2 * SPACING, 3 * CHECKBOX_SIZE + 4 * SPACING))

        return

    def update_time_frame(self, curr_time: int):
        """Create Vegetation using marching cubes"""
        print("\tCreating Vegetation surface using marching cubes")
        self.data = self.all_vegetation.contour(100, f"vegetation.{curr_time}", method='marching_cubes', rng=[0.1, 5.0])
        self.data.rename_array(self.data.array_names[0], "vegetation")

        burnt_vegetation = self.all_vegetation.contour(10, f"burnt_vegetation.{curr_time}",
                                                       method='marching_cubes', rng=[0.001, 5.0])
        if burnt_vegetation.n_cells > 0:
            self.burnt_terrain = burnt_vegetation.project_points_to_plane(  # plane = hill side
                origin=[0.0, -500.0, 201.0],
                normal=[-0.44721362, 0.0, -0.89442724])
        else:
            self.burnt_terrain = None

        self.__plot()

        return

    def __toggle(self, enabled: bool):
        self.enabled = enabled
        self.__plot()
        return

    def __plot(self):
        if self.enabled and self.data is not None and self.data.n_cells > 0:
            print("\tAdding Vegetation\n")
            self.plotter.add_mesh(
                self.data,
                scalars="vegetation",
                opacity=0.2,
                name="vegetation",
                show_scalar_bar=False,
                cmap="summer"
            )
        else:
            print("\tRemoving Vegetation\n")
            self.plotter.remove_actor("vegetation")

        if self.enabled and self.burnt_terrain is not None and self.burnt_terrain is not None:
            self.plotter.add_mesh(
                self.burnt_terrain,
                color='#3D2B1E',
                name="burnt_vegetation"
            )
        else:
            self.plotter.remove_actor("burnt_vegetation")

        return
