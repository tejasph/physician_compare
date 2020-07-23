import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import altair as alt
import plotly.express as px
import pandas as pd
from src import utils

alt.data_transformers.disable_max_rows()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE])
server = app.server
app.config['suppress_callback_exceptions'] = True

measures = pd.read_csv("data/cleaned_measures.csv")
Plotter = utils.Plotter(measures)

def make_scatter(data):
    return alt.Chart(data).mark_point().encode(
        alt.X("measure_performance_rate"),
        alt.Y("denominator_count")
        
    )
###### Layout Components

jumbotron_comp = dbc.Jumbotron([html.H1("Test"),
                                html.P("This is a dashboard to explore accountable care organisations (ACOs) in the US"),
                                html.Hr()])
org1 = dbc.Card(
    dbc.CardBody([
        html.H1("ACO1", className='cardTitle', id = 'aco1'),
        html.H5("Stats about the ACO"),
        html.P("stat 1"),
        html.P("stat 2")
        
    ])
)

org2 = dbc.Card(
    dbc.CardBody([
        html.H1("ACO1", className='cardTitle', id = 'aco2'),
        html.H5("Stats about the ACO"),
        html.P("stat 1"),
        html.P("stat 2")
        
    ])
)

# TODO adjust sizing of image to be more fluid
aco_comp = dbc.Card([

    dbc.CardBody([
        html.H1("ACO1 vs ACO2"),
        html.Iframe(
        sandbox='allow-scripts',
        id='scatter-chart',
        height='450',
        width='600',
        style={'border-width': '2', 'border': '2px solid black', 'backgroundColor': "white"},
        ################ The magic happens here
        srcDoc = Plotter.make_bar().to_html()
        ################ The magic happens here
        )
    ])
])

#### Actual Layout
app.layout = dbc.Container([
    dbc.Row([dbc.Col(jumbotron_comp)]),
    dbc.Row([
        dbc.Col(dbc.Container([
            dbc.Row(dbc.Col(org1)),
            dbc.Row(dbc.Col(org2))
        ]), width = 6),
        dbc.Col(aco_comp, width = 6)])
], fluid = True)

if __name__ == '__main__':
    app.run_server(debug=True)