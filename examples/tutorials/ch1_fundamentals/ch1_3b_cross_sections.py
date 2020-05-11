"""
1.3b: 2-D sections
==================

"""

# %%
# Importing
import gempy as gp
import numpy as np
import matplotlib.pyplot as plt

# %%
# Setup the model
# ~~~~~~~~~~~~~~~
# 

# %% 
geo_model = gp.create_model('Tutorial_ch1-1_Basics')

# Importing the data from CSV-files and setting extent and resolution
data_path = 'https://raw.githubusercontent.com/cgre-aachen/gempy_data/master/'

gp.init_data(geo_model, [0, 2000., 0, 2000., 0, 2000.], [5, 5, 5],
             path_o=data_path + "/data/input_data/tut_chapter1/simple_fault_model_orientations.csv",
             path_i=data_path + "/data/input_data/tut_chapter1/simple_fault_model_points.csv", default_values=True)
gp.map_stack_to_surfaces(geo_model,
                         {"Fault_Series": 'Main_Fault',
                          "Strat_Series": ('Sandstone_2', 'Siltstone',
                                           'Shale', 'Sandstone_1', 'basement')}, remove_unused_series=True)
geo_model.set_is_fault(['Fault_Series'])

# %%
# Add sections
# ~~~~~~~~~~~~
# 


# %%
# pass section dictionary with startpoint, endpoint and resolution for
# every section:
# 

# %% 
section_dict = {'section1': ([0, 0], [2000, 2000], [100, 80]),
                'section2': ([800, 0], [800, 2000], [150, 100]),
                'section3': ([0, 200], [1500, 500], [200, 150])}  # p1,p2,resolution
geo_model.set_section_grid(section_dict)

# %%
# Add topography
# ~~~~~~~~~~~~~~
# 

# %% 
geo_model.set_topography(fd=1.2, d_z=np.array([600, 2000]), resolution=np.array([50, 50]))

# %%
# Active grids:
# 

# %% 
geo_model.get_active_grids()

# %% 
gp.plot.plot_section_traces(geo_model)
plt.show()

# %% 
gp.set_interpolator(geo_model)

# %% 
sol = gp.compute_model(geo_model, compute_mesh=False)

# %% 
gp.plot_2d(geo_model, section_names=['topography'])

# %% 
gp.plot_2d(geo_model, section_names=['section1'])
plt.show()

# %% 
gp.plot_2d(geo_model, section_names=['section1', 'section2',
                                     'section3', 'topography'])
plt.show()

# %%
# Get polygons of formations in sections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

# %% 
from gempy.core.grid_modules import section_utils

# %% 
polygondict, cdict, extent = section_utils.get_polygon_dictionary(geo_model, 'section1')

# %% 
# this stores the xy points in the sections for every surface.
polygondict

# %%
# Look at resulting polygons:
# '''''''''''''''''''''''''''
# 

# %% 
form = 'Sandstone_2'
pointslist = np.array(polygondict[form])
c = cdict[form]
if pointslist.shape != ():
    for points in pointslist:
        plt.plot(points[:, 0], points[:, 1], color=c)
    plt.ylim(extent[2:4])
    plt.xlim(extent[:2])

# %% 
#### The same in geological map
polygondict, cdict, extent = section_utils.get_polygon_dictionary(geo_model, 'topography')

# %% 
form = 'Siltstone'
pointslist = np.array(polygondict[form])
c = cdict[form]
if pointslist.shape != ():
    for points in pointslist:
        plt.plot(points[:, 0], points[:, 1], color=c)
    plt.ylim(extent[2:4])
    plt.xlim(extent[:2])
plt.show()