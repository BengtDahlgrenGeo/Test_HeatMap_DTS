import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import glob
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go

# Get the current directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the target file
relative_path_to_target = "../files/filtered_data.csv"

# Create the absolute path by joining the script directory with the relative path
file_path = os.path.join(script_directory, relative_path_to_target)

# Define the folder path where the .ddf files are located
#file_path = 'N:\\PDOC\Hydroc\\22230040 Fält\\22_Mätningar\\Hydroc BH3\\channel 1\\2023\jun\\filtered_data.csv'

df =  pd.read_csv(file_path)
num_columns = df.shape[1]
xx = [i for i in range(1, num_columns -1 + 1)]

# Dash application
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(
        "Test - Heatmap DTS",
        style={'text-align': 'center', 'font-size': '30px'}
    ),
    dcc.Graph(id='heatmap', style={'width': '80%', 'margin': 'auto'}),
    html.H1(
        "Temperature slider",
        style={'text-align': 'center', 'font-size': '24px'}
    ),
    html.Div(id='slider-output-container-min', style={'text-align': 'center', 'font-size': '20px'}),
    html.Div(
        dcc.RangeSlider(
        id='color-range-slider',
        min=df.iloc[:, 1:num_columns].min().min(),
        max=df.iloc[:, 1:num_columns].max().max(),
        step=(df.iloc[:, 1:num_columns].max().max()-df.iloc[:, 1:num_columns].min().min())/100,
        value=[df.iloc[:, 1:num_columns].min().min(), df.iloc[:, 1:num_columns].max().max()],
        marks={str(i): str(round(i, 1)) for i in np.linspace(df.min().min(), df.max().max(), 100)}
    ), style={'width': '75%', 'margin': 'auto'}
    ),
    html.Div(id='slider-output-container-max', style={'text-align': 'center', 'font-size': '20px'}),
])


@app.callback(
    Output('heatmap', 'figure'),
    Input('color-range-slider', 'value'),
)
def update_heatmap(color_range):
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        z=df.iloc[:, 1:num_columns].values, 
        x=xx, 
        y=-df['Depth [m]'],
        zmin=color_range[0],
        zmax=color_range[1],
        coloraxis='coloraxis', hovertemplate =
        '<i>Time</i>: %{x} min<br>' +
        '<i>Depth</i>: %{y:.0f} m<br>' +
        '<i>Temperature</i>: %{z:.1f} degC<br>' +
        '<extra></extra>',
        colorscale='Jet',
        colorbar=dict(
            title="Temperature",
            titleside='top',
            x=0.5,  # x and y are the position of the colorbar (normalized coordinates, 0-1)
            y=-0.1,
            len=0.75,  # len is the length of the colorbar (normalized, 0-1)
            lenmode='fraction',  # 'fraction' or 'pixels'
            thickness=30  #
        )
    ))

    fig.update_layout(
        # title="Hydroc - Test 1",
        title_font = dict(size=30),
        xaxis_title="Time [min]",
        yaxis_title="Depth [m]",
        autosize=True, 
        # width=800, 
        # height=600,
        xaxis=dict(
            title_font=dict(size=24),
        ),
        yaxis=dict(
            title_font=dict(size=24),
        ),
        coloraxis=dict(
        cmin=color_range[0],
        cmax=color_range[1],
        colorscale='Jet',
        colorbar=dict(title="Temperature [degC]", titleside='top',tickfont=dict(size=12), x=0.5, y=-1,
            len=0.75,  # len is the length of the colorbar (normalized, 0-1)
            lenmode='fraction',  # 'fraction' or 'pixels'
            thickness=10,
            orientation ='h')
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
