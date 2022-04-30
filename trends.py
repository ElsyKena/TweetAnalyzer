import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import dash_table
from dash.dash_table.Format import Group
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
import twitter  
from api_initialization import app, api
import nltk
from wordcloud import WordCloud

# Create stopword list for wordcloud analysis later:
stopwords = nltk.corpus.stopwords.words('english')
stopwords = set(stopwords)
stopwords.update(["https", "plotlygraphs"])

def f(row):
    return "[{0}]({0})".format(row["url"])

# layout of trends
trends_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Most trending topics and a presentation of the most common words in the trends")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='table-div', children="")
        ], width=6),
        dbc.Col([
            html.Div(id='figure-div', children="")
        ], width=6),
    ], className="mt-3",),
    dcc.Interval(id='timer', interval=1000*300, n_intervals=0)
])


# pull trending tweets and create the table 
@app.callback(
    Output(component_id="table-div", component_property="children"),
    Input(component_id="timer", component_property="n_intervals"),
)
def display_trend(timer):
    trnd_name, trnd_vol, trnd_url = [], [], []
    trends = api.GetTrendsCurrent()
    for trend in trends:
        print(trend)
        if trend.tweet_volume:
            trnd_name.append(trend.name)
            trnd_vol.append(trend.tweet_volume)
            trnd_url.append(trend.url)
    d = {
        "trending": trnd_name,
        "url": trnd_url,
        "volume": trnd_vol,
    }
    df = pd.DataFrame(d)
    # apply function so you can insert url link inside Dash DataTable
    df["url"] = df.apply(f, axis=1)
    print(df.head())

    return dash_table.DataTable(
        id='datatable-trends',
        columns=[
            {"name": i, "id": i}
            if i == "trending" or i == "volume"
            else {"name": i, "id": i, 'type': 'text', "presentation":"markdown"}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        markdown_options=dict(html=True, link_target='_blank'),
        page_action='native',
        page_size=6,
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'minWidth': '50px', 'width': '80px', 'maxWidth': '120px',
        },
    )


# pull liked tweets by user 
@app.callback(
    Output(component_id="figure-div", component_property="children"),
    Input(component_id="timer", component_property="n_intervals"),
)
def display_trend(timer):
    trend_twt = []

    # get tweets metadata
    x = api.GetTrendsCurrent()
    # extract the tweet text, from the metadata, into a list
    for trend in x:
        trend_twt.append(trend.name)

    # join all tweet text into one string
    alltweets = " ".join(tweet for tweet in trend_twt)

    # generate wordcloud from all tweets
    my_wordcloud = WordCloud(
        stopwords=stopwords,
        background_color='white',
        height=275
    ).generate(alltweets)

    # visualize wordcloud inside plotly figure
    fig = px.imshow(my_wordcloud, template='ggplot2')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    return dcc.Graph(figure=fig, config={"displayModeBar":False})
