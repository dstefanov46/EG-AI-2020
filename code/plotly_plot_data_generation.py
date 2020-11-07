"""
In this file we read Miha's pandapower net and extract the coordinates of the buses and the lines, as well as some
additional data for them. We need this data in order to later generate the 'plotly plot' in app_v1.py.
"""

# IMPORTING LIBRARIES
from libs_and_funcs import *

# READING FILES
pp_net = pp.from_excel('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/SBS_skofja_loka_model/SBS_skofja_loka.xlsx')
pp_net_df = pd.read_excel('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/SBS_skofja_loka_model/SBS_skofja_loka.xlsx',
                          sheet_name='line_geodata',
                          index_col=0)

# GENERATION OF BUS DATA
bus_data = pd.DataFrame({
    'LNodeType': pp_net.bus['LNodeType'],
    'x': pp_net.bus_geodata['x'],
    'y': pp_net.bus_geodata['y'],
    'NodeId': pp_net.bus['NodeId'],
    'LNodeName': pp_net.bus['LNodeName']
})

bus_data.to_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/bus_data.xlsx')

# GENERATION OF X COORDINATES OF THE LINES
x_coord = pd.DataFrame()
for col in pp_net_df.columns:
    if 'x' in col:
        x_coord_tmp = pd.Series(pp_net_df[col])
        x_coord = pd.concat([x_coord, x_coord_tmp], axis=1)

x_coord.to_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/line_x_coord.xlsx')

# GENERATION OF Y COORDINATES OF THE LINES
y_coord = pd.DataFrame()
for col in pp_net_df.columns:
    if 'y' in col:
        y_coord_tmp = pd.Series(pp_net_df[col])
        y_coord = pd.concat([y_coord, y_coord_tmp], axis=1)

y_coord.to_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/line_y_coord.xlsx')

# GENERATION OF ADDITIONAL DATA FOR THE LINES
line_data = pd.DataFrame({
    'BranchId': pp_net.line['BranchId'],
    'Name': pp_net.line['Name']
})

line_data.to_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/line_data.xlsx')