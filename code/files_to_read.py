"""
In this file we read all the files we need in app_v1.py. We read the files here only to make the code in app_v1.py
clearer.
"""

# IMPORTING LIBRARIES
import pandas as pd
import pandapower as pp


# READING FILES

# (make sure you change the filepaths below; would've used the Sharepoint URL to the files, but PyCharm
# wouldn't recognise the link, so I continued reading the files from my local directories)
matching_table = pd.read_excel('C:/Users/User/EIMV OVDES/2020 EG AI - project - demo/input_data/network/SBS_skofja_loka – bus&line.xlsx',
                                sheet_name='povezovalna_tabela',
                                index_col=0)
bus_table = pd.read_excel('C:/Users/User/EIMV OVDES/2020 EG AI - project - demo/input_data/network/SBS_skofja_loka – bus&line.xlsx',
                                sheet_name='bus')
ts_measurements = pd.read_csv('C:/Users/User/EIMV OVDES/2020 EG AI - project - demo/input_data/measurements/TS_measurements.csv',
                                index_col=0)

# The following line imports the pandapower net which is the basis for the 'pandapower plot'
pp_net = pp.from_excel('C:/Users/User/EIMV OVDES/2020 EG AI - Documents/project - demo/input_data/network/SBS_skofja_loka_model/SBS_skofja_loka.xlsx')

# If you want to use the 'plotly plot', then comment line 19, and uncomment the next couple of lines
# bus_data = pd.read_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/bus_data.xlsx',
#                          index_col=0)
# line_x_coord = pd.read_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/line_x_coord.xlsx',
#                              index_col=0)
# line_y_coord = pd.read_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/line_y_coord.xlsx',
#                              index_col=0)
# line_data = pd.read_excel('C:/Users/User/Desktop/EIMV/Delo/Dash_app/line_data.xlsx',
#                           index_col=0)