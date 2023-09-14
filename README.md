# Wildfire-Visualization

Course project for Scientific Visualization 2022 course at ETHZ.

Authors: Eric Enzler, Gianluca Moro

---
## Disclaimer
**The program requires quite some memory, so it might not work on some laptops.**

Furthermore, the program takes 1 to 2 minutes at the beginning to load data.
Just be patient. Also, there might be warnings which can safely be ignored. 

## Python Requirements
- pyvista: https://docs.pyvista.org/getting-started/installation.html
- pandas: https://pypi.org/project/pandas/

## Important
Set up LSF before committing any large files (e.g., vti and vtk files)

## Data
The raw data files can be downloaded from https://cgl.ethz.ch/Downloads/Data/VisualizationData/Wildfire.zip   
The downloaded files need to be placed in the `src/data/` folder.

The preprocessed wind and vegetation data files need to be extracted from the `src/data/preprocessed-data.zip` archive and placed into the `src/data` folder.

## Running the Visualization
Run the main visualization by running the command:
- `python3 wildfire.py`

Run the more detailed wind visualization by running the command:
- `python3 wind_extended.py`

---
## Visualization Overview
![](images/wildfire-visualization.png)
