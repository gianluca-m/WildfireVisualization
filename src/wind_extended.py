"""
    Author: Eric Enzler
    Description:
        Displays different components of the Wind with Glyphs and Streamlines
"""

import pyvista as pv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NUM_DATA_FRAMES = 15
SCALAR_NAMES = ['u', 'O2', 'convht_1', 'frhosiesrad_1', 'rhof_1', 'rhowatervapor', 'theta', 'v', 'w']
DATA_FOLDER = './data/'
CHECKBOX_SIZE = 40
SPACING = 10
initial_frame = 1
wind_mesh = pv.read("data/wind.vtk")
glyph_checker = False
dataset = pd.read_csv('data/chart_data.csv', sep=',')
x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

def swap_mesh(timestamp):
    time_frame = int(timestamp)
    print(f"Update frame: {time_frame}")
    file_name = f"output.{time_frame:02d}000.vti"
    print(f"\tReading file '{file_name}'")
    curr_mesh = pv.read(DATA_FOLDER + file_name)
    print("\tFinished reading file")

    return curr_mesh

def add_subplot(scalar, y_lim, y_label, title, curr_time, ax):
    y = dataset[scalar]
    ax.set_title(title)
    ax.plot(x, y)
    curr_time_axis = ax.plot([curr_time, curr_time], y_lim)
    ax.set_ylim(y_lim)
    ax.set_xlabel("Timestep")
    ax.set_ylabel(y_label)
    ax.set_xlim(left=x[0], right=x[-1])
    ax.set_xticks([i for i in range(x[0], x[-1]+1, 2)])
    return curr_time_axis

def update_charts(time_frame, plotter, histograms, time_axes):
    
    plotter.remove_chart(histograms)

    print("\tUpdating plot timestamps")
    for time_axis in time_axes:
        time_axis[0].set_xdata([time_frame, time_frame])

    plotter.add_chart(histograms)

    plt.close('all')
    return

def setup_charts():    
    fig = plt.figure(tight_layout=True)
    ax0, ax1, ax2, ax3, = fig.subplots(4, 1)
    fig.tight_layout()
    time_axes = [
            add_subplot("wind_max", [23.0, 30.0], "km/h", "Max Wind Speed Combined", initial_frame, ax0),
            add_subplot("u_max", [23.0, 28.0], "km/h", "Max Wind Speed horizontal", initial_frame, ax1),
            add_subplot("v_max", [8.0, 20.0], "km/h", "Max Wind Speed lateral", initial_frame, ax2),
            add_subplot("w_max", [10.0, 24.0], "km/h", "Max Wind Speed vertical", initial_frame, ax3)
        ]
    histograms = pv.ChartMPL(fig, size=(0.4, 1.0), loc=(0.6, 0.0))
    histograms.background_color = (1.0, 1.0, 1.0, 0.8)

    return histograms, time_axes
    
def static_terrain(plotter):
    terrain_point_0 = [700.0, -500.0, 0.0]
    terrain_point_1 = [400.0, -500.0, 0.0]
    terrain_point_2 = [0.0, -500.0, 200.0]
    terrain_point_3 = [-415.0, -500.0, 0.0]
    terrain_point_4 = [-500.0, -500.0, 0.0]
    terrain_point_6 = [-415.0, 500.0, 0.0]
    terrain_point_7 = [0.0, 500.0, 200.0]
    terrain_point_8 = [400.0, 500.0, 0.0]
    terrain_point_5 = [-500.0, 500.0, 0.0]
    terrain_point_9 = [700.0, 500.0, 0.0]

    terrain_0 = pv.Rectangle([terrain_point_0, terrain_point_4, terrain_point_5, terrain_point_9])
    terrain_1 = pv.Rectangle([terrain_point_1, terrain_point_2, terrain_point_7, terrain_point_8])
    terrain_2 = pv.Rectangle([terrain_point_2, terrain_point_3, terrain_point_6, terrain_point_7])
    terrain_3 = pv.Triangle([terrain_point_1, terrain_point_2, terrain_point_3])
    terrain_4 = pv.Triangle([terrain_point_8, terrain_point_7, terrain_point_6])

    color = "#C4A484"
    plotter.add_mesh(terrain_0, color=color, name="terrain_0")
    plotter.add_mesh(terrain_1, color=color, name="terrain_1")
    plotter.add_mesh(terrain_2, color=color, name="terrain_2")
    plotter.add_mesh(terrain_3, color=color, name="terrain_4")
    plotter.add_mesh(terrain_4, color=color, name="terrain_5")
'''
def slice_mesh(mesh,x_cord, y_cord,z_cord):
    slices = mesh.slice_orthogonal(x=x_cord,y=y_cord,z=z_cord)
'''

def plot_wind(initial_frame: int = 1):
    windplot = pv.Plotter(shape='2/3')
    mesh = pv.read(DATA_FOLDER + f"output.{initial_frame:02d}000.vti")
    outline = mesh.outline()
    arrowX = pv.Arrow(direction = [1,0,0])
    arrowY = pv.Arrow(direction = [0,1,0])
    arrowZ = pv.Arrow(direction = [0,0,1])
    curr_mesh = mesh
    histograms, time_axes = setup_charts()


    def glyphmode(value):
        setup_plots(curr_mesh, value)

    def setup_plots(curr_mesh, glyph_bool):
        global glyph_checker
        glyph_checker = glyph_bool
        print("Setup Plots: Glyphs = " + str(glyph_bool))
        windplot.subplot(0)
        if(glyph_bool):
            windplot.remove_actor("u-map")
            windplot.add_mesh(curr_mesh.glyph(orient=False, scale = "u",factor = 3,tolerance = 0.05, geom = arrowX), scalars = "u", cmap="seismic", name="u-glyph")
        else:
            windplot.remove_actor("u-glyph")
            windplot.add_mesh(curr_mesh, scalars = "u", cmap='jet', name = "u-map")
       
        windplot.subplot(1)
        if(glyph_bool):
            windplot.remove_actor("v-map")
            windplot.add_mesh(curr_mesh.glyph(orient=False, scale = "v",factor = 20,tolerance = 0.05, geom = arrowY), scalars = "v", cmap="seismic",name="v-glyph")
        else:
            windplot.remove_actor("v-glyph")
            windplot.add_mesh(curr_mesh, scalars = "v", cmap='jet',name = "v-map")

        windplot.subplot(2)
        if(glyph_bool):
            windplot.remove_actor("w-map")
            windplot.add_mesh(curr_mesh.glyph(orient=False, scale = "w",factor = 10,tolerance = 0.05, geom = arrowZ), scalars = "w", cmap="seismic",name="w-glyph")
        else:
            windplot.remove_actor("w-glyph")
            windplot.add_mesh(curr_mesh, scalars = "w", cmap='jet',name = "w-map")

        print("\tFinished updating Plots")
        return


    def update_frame(value):   
        timestep = int(value)
        curr_mesh = (swap_mesh(value))
        setup_plots(curr_mesh,glyph_checker)

        windplot.subplot(4)
        update_charts(timestep, windplot, histograms,time_axes)

        windplot.subplot(3)
        windplot.remove_actor("full_glyph")
        windplot.add_mesh(wind_mesh.glyph(orient=f"wind{timestep:02d}", scale = f"mag{timestep:02d}",factor = 3,tolerance = 0.05), scalars = f"mag{timestep:02d}", cmap="seismic", name = "full_glyph")
        
        print("\tFinished updating frame")
        return

    windplot.subplot(0)
    static_terrain(windplot)
    windplot.add_mesh(outline)
    windplot.add_text("Wind Horizontal component", color='white')

    windplot.subplot(1)
    static_terrain(windplot)
    windplot.add_mesh(outline)
    windplot.add_text("Wind Lateral component", color='white')

    windplot.subplot(2)
    static_terrain(windplot)
    windplot.add_mesh(outline)
    windplot.add_text("Wind Vertical component", color='white')

    windplot.subplot(3)
    static_terrain(windplot)
    windplot.add_mesh(outline)
    windplot.add_text("Wind vector Combined displacement", color='white')
    windplot.view_zx()
    windplot.link_views()
    windplot.add_camera_orientation_widget()
        
    windplot.subplot(4)
    windplot.add_text("Input & Charts", color='white',)
    windplot.add_checkbox_button_widget(glyphmode, value=False, color_on='#00FFFF', color_off='#000000',
                                                size=CHECKBOX_SIZE, position=(SPACING, 5 * CHECKBOX_SIZE + 6 * SPACING))
    windplot.add_text(text="Glyphmode", position=(CHECKBOX_SIZE + 2 * SPACING, 5 * CHECKBOX_SIZE + 6 * SPACING))
    windplot.add_chart(histograms)
    windplot.add_slider_widget(update_frame, [1, NUM_DATA_FRAMES], title='Timestep Slider', value=1, pointa=(0.05,0.2),pointb=(0.55,0.2),fmt="%0.0f", style='modern')

    windplot.show()

    return

def main():
    plot_wind()


if __name__ == '__main__':
    main()

