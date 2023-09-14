import pyvista as pv

CHECKBOX_SIZE = 40
SPACING = 10


class Outline:
    def __init__(self, plotter: pv.Plotter):
        self.plotter = plotter
        self.enabled = False

        corner0 = [-500.0, -500.0, 0]
        corner1 = [-500.0, 500.0, 0]
        corner2 = [700.0, 500.0, 0]
        corner3 = [700.0, -500.0, 0]
        corner4 = [corner0[0], corner0[1], 900.0]
        corner5 = [corner1[0], corner1[1], 900.0]
        corner6 = [corner2[0], corner2[1], 900.0]
        corner7 = [corner3[0], corner3[1], 900.0]

        self.outline_data = pv.PolyData(
            [
                corner0,
                corner1,
                corner2,
                corner3,
                corner4,
                corner5,
                corner6,
                corner7
            ],
            lines=[5, 0, 1, 2, 3, 0,
                   5, 4, 5, 6, 7, 4,
                   2, 0, 4,
                   2, 1, 5,
                   2, 2, 6,
                   2, 3, 7]
        )

        self.plotter.add_checkbox_button_widget(self.__toggle, value=False, color_on='#FAC668', color_off='#000000',
                                                size=CHECKBOX_SIZE, position=(SPACING,4 * CHECKBOX_SIZE + 5 * SPACING))
        self.plotter.add_text(text="Outline", position=(CHECKBOX_SIZE + 2 * SPACING, 4 * CHECKBOX_SIZE + 5 * SPACING))
        return

    def __toggle(self, enabled: bool):
        self.enabled = enabled
        self.__plot()
        return

    def __plot(self):
        if self.enabled:
            print("Adding outlines")
            self.plotter.add_mesh(self.outline_data, name="outline", line_width=2)
        else:
            print("Removing outlines")
            self.plotter.remove_actor("outline")
        return
