"""
This file represents the Dash app for the project EG AI 2020.
"""

# Run this file and visit http://127.0.0.1:8050/ in your web browser.

# IMPORTING LIBRARIES AND FUNCTIONS
from libs_and_funcs import *

# READING FILES
from files_to_read import *

# Uncomment the next line and line 107 if you want to show the 'plotly plot'
# fig = plot_buses_and_lines(bus_data, line_x_coord, line_y_coord, line_data)

# SETTING THE CSS STYLESHEETS
external_stylesheets = [' https://codepen.io/chriddyp/pen/dZVMbK.css']

# CREATING A DASH OBJECT - THE APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# CREATING THE LAYOUT OF THE APP
app.layout = html.Div([
    html.H1(
        children='EG AI 2020',
        style={
            'color': colors['text']
        }
    ),
    dcc.Markdown(
        '> ### * **Information about the transformers in the Gorenjska region** *',
        style={
            'color': colors['text']
        }
    ),
    dcc.Markdown(
        '''
        ---
        Type in the **NodeID** to get information about the transformer:
        ''',
        style={
            'color': colors['text']
        }
    ),
    dcc.Input(
        id='NodeID',
        type='number',
        size='40',
        placeholder='Enter a NodeID',
        style={
            'color': colors['background']
        }
    ),
    html.Br(),
    html.Br(),
    html.Div([
        dcc.Markdown(
            id='measurements table heading',
            style={
                'color': colors['text']
            }
        ),
        html.Div(
            id='measurements table',
            style={
                'height': 250,
                'width': 350,
                'color': colors['text']
            }
        ),
        dcc.Markdown(
            id='metadata table heading',
            style={
                'color': colors['text']
            }
        ),
        html.Div(
            id='metadata table',
            style={
                'height': 250,
                'width': 600,
                'color': colors['text']
            }
        )
    ],
        id='tables',
        style={
            'columnCount': 2,
            'height': 250,
            'width': 1200,
            'color': colors['text']
        }
    ),
    html.Div(
        id='ts_measurements_plot',
        style={
            'width': 1200,
            'margin': 'auto',
            'backgroundColor': colors['background']
        }
    ),
    html.Div(
        [dcc.Graph(
            # figure=fig,   # uncomment this line if you want to show the 'plotly plot'
            figure=simple_plotly(pp_net, use_line_geodata=True),  # with this line you make the 'pandapower plot'
            config={
                'scrollZoom': True,
                # 'fillFrame': True
            }
        )],
        id='plot_network_on_map',
        style={
            'width': 1000,
            'height': 1200,
            'margin': 'auto'
        },
    )
],
    style={
        'backgroundColor': colors['background']
    }
)


# APP CALLBACKS
@app.callback(
    Output('measurements table heading', 'children'),
    [Input('NodeID', 'value')]
)
def write_heading_measurements(nodeID):
    """
    :param nodeID: number, the NodeID of the transformer (user input)
    :return: string, the measurements table heading
    """
    if nodeID not in matching_table.index:
        raise PreventUpdate
    else:
        return 'MEASUREMENTS TABLE'


@app.callback(
    Output('measurements table', 'children'),
    [Input('NodeID', 'value')]
)
def show_ts_measurements(nodeID):
    """
    :param nodeID: number, the NodeID of the transformer (user input)
    :return: measurements_table, dash_table.DataTable, table with the first 5 measurements for a certain
            transformer
    """
    if nodeID not in matching_table.index:
        raise PreventUpdate
    else:
        desired_transformer = matching_table.loc[matching_table.index == nodeID].values[0, 0]
        desired_transformer_measurements = ts_measurements[desired_transformer].head(5).values
        measurements = pd.DataFrame(
            {'Timestamps': ts_measurements.index[:5],
             'Measurements': desired_transformer_measurements}
        )
        measurements_table = dash_table.DataTable(
            id='measurements table',
            columns=[{'name': col_name, 'id': col_name} for col_name in measurements.columns],
            data=measurements.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': colors['text']
            }
        ),
        return measurements_table


@app.callback(
    Output('metadata table heading', 'children'),
    [Input('NodeID', 'value')]
)
def write_heading_metadata(nodeID):
    """
    :param nodeID: number, the NodeID of the transformer (user input)
    :return: string, transformer metadata heading
    """
    if nodeID not in matching_table.index:
        raise PreventUpdate
    else:
        return 'TRANSFORMER META DATA'


@app.callback(
    Output('metadata table', 'children'),
    [Input('NodeID', 'value')]
)
def show_metadata(nodeID):
    """
    :param nodeID: number, the NodeID of the transformer (user input)
    :return: metadata_table, dash_table.DataTable, table with the metadata for a certain transformer
    """
    if nodeID not in matching_table.index:
        raise PreventUpdate
    else:
        metadata = bus_table.loc[bus_table['name'] == nodeID]
        metadata_table = dash_table.DataTable(
            id='metadata table',
            columns=[{'id': col_name, 'name': col_name} for col_name in metadata.columns],
            data=metadata.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': colors['text']
            }
        )
        return metadata_table


@app.callback(
    Output('ts_measurements_plot', 'children'),
    [Input('NodeID', 'value')]
)
def plot_ts_measurements(nodeID):
    """
    :param nodeID: number, the nodeID of the transformer (user input)
    :return: dcc.Graph, interactive plot of the measurements for a certain transformer
    """
    if nodeID not in matching_table.index:
        raise PreventUpdate
    else:
        desired_transformer = matching_table.loc[matching_table.index == nodeID].values[0, 0]
        desired_transformer_measurements = ts_measurements[desired_transformer]
        measurements = pd.Series(desired_transformer_measurements,
                                 index=ts_measurements.index)
        fig_measurements = plotly_df(measurements, nodeID, slider=True)
        return dcc.Graph(figure=fig_measurements)


if __name__ == '__main__':
    app.run_server(debug=True)