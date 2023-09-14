"""
    Author: Gianluca Moro, Eric Enzler
    Description:
        Displays terrain, vegetation, wind (streamlines), fire, smoke, and some Histograms.
"""
import pyvista as pv
from fire import Fire
from smoke import Smoke
from wind import Wind
from vegetation import Vegetation
from outline import Outline
from terrain import Terrain
from charts2d import Charts2d

NUM_DATA_FRAMES = 15
DATA_FOLDER = './data/'


def visualize_wildfire():
    plotter = pv.Plotter(title="Wildfire")
    plotter.camera.position = (2000, -2500, 1200)
    plotter.camera.azimuth = 90
    plotter.camera.zoom(1.75)

    initial_time_step = 12

    terrain = Terrain(plotter)
    wind = Wind(plotter, initial_time_step)
    fire = Fire(plotter)
    smoke = Smoke(plotter)
    vegetation = Vegetation(plotter)
    outline = Outline(plotter)
    chart = Charts2d(plotter, initial_time_step)

    def update_frame(value):
        time_frame = round(value)
        print(f"Update frame: {time_frame}")
        plotter.add_text("Updating...", font_size=8, name="update_notification")

        file_name = f"output.{time_frame:02d}000.vti"
        print(f"\tReading file '{file_name}'")
        curr_mesh = pv.read(DATA_FOLDER + file_name)
        print("\tFinished reading file\n")

        wind.update_time_frame(time_frame)
        fire.update_time_frame(curr_mesh)
        smoke.update_time_frame(curr_mesh)
        vegetation.update_time_frame(time_frame)
        chart.update_time_frame(time_frame)

        plotter.remove_actor("update_notification")
        print("Finished updating frame\n")
        return

    plotter.add_slider_widget(update_frame, [1, NUM_DATA_FRAMES], value=initial_time_step,
                              title='Timestep', pointa=(0.2, 0.1), pointb=(0.55, 0.1),
                              fmt="%0.0f", style='modern')
    plotter.add_camera_orientation_widget()
    plotter.show()


def main():
    visualize_wildfire()


if __name__ == '__main__':
    main()
