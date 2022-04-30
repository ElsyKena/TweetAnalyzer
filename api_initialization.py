import dash
import dash_bootstrap_components as dbc
import twitter

import os
from decouple import config

# Authenticating the twitter api.
api = twitter.Api(
    consumer_key=config("TWITTER_CONSUMER_KEY"),
    consumer_secret=config("TWITTER_CONSUMER_SECRET"),
    access_token_key=config("TWITTER_TOKEN_KEY"),
    access_token_secret=config("TWITTER_TOKEN_SECRET"))
    
#initializing dash
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    external_stylesheets=[dbc.themes.CERULEAN],
    meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0'}])
