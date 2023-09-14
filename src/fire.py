import pyvista as pv

CHECKBOX_SIZE = 40
SPACING = 10


class Fire:
    def __init__(self, plotter: pv.Plotter):
        self.plotter = plotter
        self.enabled = True
        self.data: pv.PolyData = pv.PolyData()

        self.plotter.add_checkbox_button_widget(self.__toggle, value=self.enabled, color_on='#fa3605', color_off='#000000',
                                                size=CHECKBOX_SIZE, position=(SPACING, SPACING))
        self.plotter.add_text(text="Fire", position=(CHECKBOX_SIZE + 2 * SPACING, SPACING))
        return

    def update_time_frame(self, curr_mesh: pv.DataSet):
        """Create fire surface using marching cubes"""
        print("\tCreating fire surface using marching cubes")
        self.data = curr_mesh.contour(300, "theta", method='marching_cubes', rng=[399, 800])
        self.data.rename_array(self.data.array_names[0], "fire_surface")
        self.__plot()
        return

    def __toggle(self, enabled: bool):
        self.enabled = enabled
        self.__plot()
        return

    def __plot(self):
        if self.data is not None and self.data.n_cells > 0 and self.enabled:
            print("\tAdding fire surface\n")
            self.plotter.add_mesh(
                self.data,
                scalars="fire_surface",
                opacity=0.8,
                name="fire",
                show_scalar_bar=False,
                smooth_shading=True,
                specular=5,
                cmap="hot",
                clim=[200, 800],
                ambient=1.0
            )
        else:
            print("\tRemoving fire surface\n")
            self.plotter.remove_actor("fire")

        return
