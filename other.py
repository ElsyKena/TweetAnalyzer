import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
import twitter 
from api_initialization import app, api


# layout of other tab
other_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("More Twitter analysis to come...")
        ], width=12)
    ])
])