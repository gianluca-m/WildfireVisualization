import pyvista as pv


class Terrain:
    def __init__(self, plotter: pv.Plotter):
        terrain_point_0 = [700.0, -500.0, 0.0]
        terrain_point_1 = [400.0, -500.0, 0.0]
        terrain_point_2 = [0.0, -500.0, 200.0]
        terrain_point_3 = [-415.0, -500.0, 0.0]
        terrain_point_4 = [-500.0, -500.0, 0.0]
        terrain_point_5 = [-500.0, 500.0, 0.0]
        terrain_point_6 = [-415.0, 500.0, 0.0]
        terrain_point_7 = [0.0, 500.0, 200.0]
        terrain_point_8 = [400.0, 500.0, 0.0]
        terrain_point_9 = [700.0, 500.0, 0.0]

        terrain_0 = pv.Rectangle([terrain_point_0, terrain_point_4, terrain_point_5, terrain_point_9])
        terrain_1 = pv.Rectangle([terrain_point_1, terrain_point_2, terrain_point_7, terrain_point_8])
        terrain_2 = pv.Rectangle([terrain_point_2, terrain_point_3, terrain_point_6, terrain_point_7])
        terrain_3 = pv.Triangle([terrain_point_1, terrain_point_2, terrain_point_3])
        terrain_4 = pv.Triangle([terrain_point_8, terrain_point_7, terrain_point_6])

        color = "#A38268"
        plotter.add_mesh(terrain_0, color=color, name="terrain_0")
        plotter.add_mesh(terrain_1, color=color, name="terrain_1")
        plotter.add_mesh(terrain_2, color=color, name="terrain_2")
        plotter.add_mesh(terrain_3, color=color, name="terrain_4")
        plotter.add_mesh(terrain_4, color=color, name="terrain_5")
