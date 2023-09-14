import pyvista as pv

CHECKBOX_SIZE = 40
SPACING = 10


class Smoke:
    def __init__(self, plotter: pv.Plotter):
        self.plotter = plotter
        self.enabled = True
        self.data: pv.PolyData = pv.PolyData()

        self.plotter.add_checkbox_button_widget(self.__toggle, value=self.enabled, color_on='#999897', color_off='#000000',
                                                size=CHECKBOX_SIZE, position=(SPACING, CHECKBOX_SIZE + 2 * SPACING))
        self.plotter.add_text(text="Smoke", position=(CHECKBOX_SIZE + 2 * SPACING, CHECKBOX_SIZE + 2 * SPACING))
        return

    def update_time_frame(self, curr_mesh: pv.DataSet):
        """Create smoke surface using marching cubes"""
        print("\tCreating smoke surface using marching cubes")
        self.data = curr_mesh.contour(300, "theta", method='marching_cubes', rng=[304, 800])
        self.data.rename_array(self.data.array_names[0], "smoke_surface")
        self.__plot()
        return

    def __toggle(self, enabled: bool):
        self.enabled = enabled
        self.__plot()
        return

    def __plot(self):
        if self.data is not None and self.data.n_cells > 0 and self.enabled:
            print("\tAdding smoke surface\n")
            self.plotter.add_mesh(
                self.data,
                scalars="smoke_surface",
                opacity=0.3,
                name="smoke",
                show_scalar_bar=False,
                cmap="Greys",
                clim=[100, 600],
                smooth_shading=True
            )
        else:
            print("\tRemoving smoke surface\n")
            self.plotter.remove_actor("smoke")

        return
