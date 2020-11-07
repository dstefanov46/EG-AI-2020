"""
In this file we read the .shp files of the electrical network (buses and lines) and extract the coordinates of the
objects in this electrical network. We need this data in order to later generate the 'pandapower plot' in app_v1.py.
"""

# IMPORTING LIBRARIES
from libs_and_funcs import *

# READING FILES
# (make sure you change the filepaths below; would've used the Sharepoint URL to the files, but PyCharm
# wouldn't recognise the link, so I continued reading the files from my local directories)

# This bus_table2 is actually the 'bus' sheet imported from Miha's pandapower net. This sheet contains all the buses
# that are also in bus_table in the file app_v1.py, but we didn't use bus_table here, because the buses in bus_table
# are not ordered as we would like them to be.
bus_table_2 = pd.read_excel('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/SBS_skofja_loka_model/SBS_skofja_loka.xlsx',
                            sheet_name='bus')
line_table_2 = pd.read_excel('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/SBS_skofja_loka_model/SBS_skofja_loka.xlsx',
                            sheet_name='line')
qGIS_line = gpd.read_file('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/GIS/RTP Škofja Loka_LINE.shp')
qGIS_node = gpd.read_file('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/GIS/RTP Škofja Loka_LNODE.shp')
qGIS_point = gpd.read_file('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/GIS/RTP Škofja Loka_POINT.shp')

# GENERATION OF BUS COORDINATES DATAFRAME
bus_coord_df = pd.DataFrame({'x0': [], 'y0': []})
missing_ids = []
for id in bus_table_2['NodeId']:
    coord_tmp = qGIS_point.loc[qGIS_point['NodeId'] == str(id)]['geometry']
    if len(coord_tmp.index) == 0:
        missing_ids.append(id)
    x_coord_tmp, y_coord_tmp = list(coord_tmp.x), list(coord_tmp.y)
    bus_coord_df_tmp = pd.DataFrame({'x0': x_coord_tmp, 'y0': y_coord_tmp})
    bus_coord_df = pd.concat([bus_coord_df, bus_coord_df_tmp])

print(qGIS_point)
print(bus_coord_df)
print(missing_ids)

bus_coord_df.index = range(len(bus_coord_df.index))

# EXPORT OF BUS COORDINATES DATAFRAME TO EXCEL FILE
bus_coord_df.to_excel('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/SBS_skofja_loka_model/SBS_skofja_loka_copy2.xlsx',
                     sheet_name='bus_geodata')

# GENERATION OF LINES COORDINATES DATAFRAME
missing_ids = []
all_coord_tmp = []
for id in line_table_2['BranchId']:
    xy_coord_tmp = []
    coord_tmp = qGIS_line.loc[qGIS_line['BranchId'] == str(id)]['geometry'].values
    if len(coord_tmp) == 0:
        missing_ids.append(id)
    for value in coord_tmp:
        x_coord_tmp, y_coord_tmp = list(value.xy[0]), list(value.xy[-1])
    for i in range(len(x_coord_tmp)):
        xy_coord_tmp.append(x_coord_tmp[i])
        xy_coord_tmp.append(y_coord_tmp[i])
    all_coord_tmp.append(xy_coord_tmp)

print(qGIS_point)
print(all_coord_tmp)
print(missing_ids)  # here we'll see that there are some ids missing, so we need to go delete some line entries in
                    # Miha's pandapower net

# GETTING THE MAX LENGTH OF A LIST IN all_coord_tmp
max_len_list = 0
for el in all_coord_tmp:
    if len(el) > max_len_list:
        max_len_list = len(el)

# STACKING ALL LISTS WITH ZEROS (to make sure they all have the same length)
all_coord_new = []
for el in all_coord_tmp:
    el = np.array([el])
    if len(el) < max_len_list:
        el = np.hstack((el, np.zeros((1, max_len_list - el.shape[1]))))
        all_coord_new.append(el)

# JOIN THE COORDINATES FOR ALL LINES INTO A FINAL NUMPY MATRIX
all_coord_final = np.empty((1, max_len_list))
for array in all_coord_new:
    all_coord_final = np.vstack((all_coord_final, array))

# PREPARATION OF LINES COORDINATES DATAFRAME HEADER
columns = []
for i in range((all_coord_final.shape[1] // 2) + 1):
    columns.append('x' + str(i))
    columns.append('y' + str(i))

# CREATION OF THE DATA FOR THE DATAFRAME
data_dict = {}
for i in range(all_coord_final.shape[1]):
    data_dict[columns[i]] = all_coord_final[:, i]

# CREATION OF THE DATAFRAME
line_geodata = pd.DataFrame(data_dict)
line_geodata = line_geodata.drop(axis='index', labels=0)
line_geodata = line_geodata.replace(0, '')
line_geodata.index = range(len(line_geodata.index))

# EXPORT OF THE DATAFRAME TO EXCEL TABLE
line_geodata.to_excel('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/SBS_skofja_loka_model/SBS_skofja_loka_copy3.xlsx',
                     sheet_name='line_geodata',
                     na_rep='')

"""
So, basically what we did in this file is that we created two Excel files with the bus and line coordinates, 
correspondingly. Once we had the files, we went to Excel, and moved these sheets to the file 'SBS_skofja_loka.xlsx', 
because in this file we have Miha's pandapower net stored, so we need the coordinates there.
"""