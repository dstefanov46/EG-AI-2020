"""
This file contains the libraries and functions needed in the script app_v1.py.
"""

# IMPORTING LIBRARIES
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandapower as pp
from pandapower.plotting.plotly import simple_plotly
from pandapower import runpp

# DICTIONARY OF COLORS FOR THE BACKGROUND AND THE TEXT IN THE APP
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# DICTIONARIES OF PARAMETERS (used to set different features in the qGIS plot)
qGIS_parameters = {
    'colors': {
        'O': 'green',
        'TP': 'red',
        'RTP': 'pink',
        'RP': 'violet'
    },
    'symbols': {
        'O': 'circle',
        'TP': 'square',
        'RTP': 'triangle-up',
        'RP': 'pentagon'
    }
}


# FUNCTION DEFINITIONS

# FUNCTION TO PLOT A DATAFRAME USING PLOTLY
def plotly_df(df_in, nodeID, slider=False):
    """
    :param df_in: pd.DataFrame, the DataFrame to plot
    :param slider: Boolean, variable to choose whether or not to add the slider to the plot
    :param nodeID: number, the NodeID of the transformer (user input)
    :return: plotly.graph_object, plot of all columns of a DataFrame
    """

    if isinstance(df_in, pd.Series):
        df = df_in.to_frame()
    else:
        df = df_in.copy()

    title = 'Measurements for the transformer with NodeID: ' + str(nodeID)

    plot_data = []

    for i, col in enumerate(df.columns):
        go_scatter = go.Scatter(
            name=col,
            x=df.index,
            y=df.loc[:, col],
            line={'width': 2, 'color': colors['text']},
            opacity=0.8
        )
        plot_data.append(go_scatter)  # interesting: graph object appended to a list

    layout = go.Layout(
        height=600,
        width=1200,
        font={
            'size': 15
        },
        title=title,
        xaxis={
            'title': 'Timestamps',
            # Range selector with buttons
            'rangeselector': {
                # Buttons for selecting time scale
                'buttons': [
                    # button for time scale of 1 day
                    {
                        'count': 1,
                        'label': '  1 day   ',
                        'step': 'day',
                        'stepmode': 'todate'
                    },
                    # button for time scale of 1 week
                    {
                        'count': 7,
                        'label': '  1 week   ',
                        'step': 'day',
                        'stepmode': 'todate'
                    },
                    # button for time scale of 1 month
                    {
                        'count': 1,
                        'label': '  1 month   ',
                        'step': 'month',
                        'stepmode': 'backward'
                    },
                    # entire scale
                    {
                        'label': '  ALL  ',
                        'step': 'all'
                    }
                ]
            },
            'rangeslider': {
                'visible': True
            }
        },
        yaxis={
            'title': 'Measurements'
        }
    )

    if not slider: layout = None
    fig = go.Figure(
        data=plot_data,
        layout=layout
    )
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background']
    )

    return fig


# FUNCTION TO PLOT BOTH THE BUSES AND THE LINES
def plot_buses_and_lines(bus_data, line_x_coord, line_y_coord, line_data):
    """
    :param bus_data: pandas.DataFrame, a DataFrame in which we have all the info for our buses needed for the 'plotly
                     plot'
    :param line_x_coord: pandas.DataFrame, a DataFrame in which we have the x coordinates of our lines
    :param line_y_coord: pandas.DataFrame, a DataFrame in which we have the y coordinates of our lines
    :param line_data: pandas.DataFrame, a DataFrame in which we have the BranchIDs and Names of our lines
    :return fig: plotly.graph_object.Figure, a map on which we have plotted our buses and lines
    """
    fig = go.Figure()

    # PLOTTING OF THE LINES
    for i in range(len(line_data.index)):
        x_coord = line_x_coord.loc[i].dropna().values / 10000
        y_coord = line_y_coord.loc[i].dropna().values / 10000
        branch_id = line_data['BranchId'].values[i]
        name = line_data['Name'].values[i]
        fig.add_trace(
            go.Scattermapbox(
                name='line',
                lon=x_coord,
                lat=y_coord,
                mode='markers+lines',
                # line={
                #     'color': 'blue',
                #     'width': 2
                # },
                marker={
                    'size': 0.5,
                    'color': 'blue'
                },
                hovertext='BranchID: ' + str(branch_id) + '<br>Name: ' + str(name),
                showlegend=False
            )
        )

    for i in range(bus_data['LNodeType'].nunique()):
        node_type = bus_data['LNodeType'].unique()[i]
        x_coord = bus_data.loc[bus_data['LNodeType'] == node_type]['x'].values / 10000
        y_coord = bus_data.loc[bus_data['LNodeType'] == node_type]['y'].values / 10000
        node_info_df = bus_data.loc[bus_data['LNodeType'] == node_type][['NodeId', 'LNodeName', 'LNodeType']].values
        fig.add_trace(
            go.Scattermapbox(
                name=node_type,
                lon=x_coord,
                lat=y_coord,
                mode='markers',
                marker={
                    'size': 10,
                    'color': qGIS_parameters['colors'][node_type]
                },
                hovertext=['LNodeID: ' + str(node_ID) + '<br>Name: ' + str(node_name) + '<br>Type: ' + str(node_type)
                           for [node_ID, node_name, node_type] in node_info_df],
                showlegend=True
            )
        )

    fig.update_layout(
        height=700,
        width=1000,
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'style': "stamen-terrain",
            'zoom': 1,
            'center': {'lon': 40, 'lat': 40}
        }
    )

    return fig

