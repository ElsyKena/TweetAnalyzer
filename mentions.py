#importing all the necessary libraries.
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
import pandas as pd
import twitter
import sklearn
import nltk
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import wordcloud
import statsmodels.api as sm
from api_initialization import app, api
#mention tab layout.
mentions_layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Number of Tweets to analyze"),
                        dcc.Dropdown(
                            id="count-mentions",
                            multi=False,
                            value=100,
                            options=[
                                {"label": "100", "value": 100},
                                {"label": "200", "value": 200},
                                {"label": "300", "value": 300},
                            ],
                            clearable=False,
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.Label("Search account handle"),
                        dcc.Input(
                            id="input-handle",
                            type="text",
                            placeholder="Mentioning this account",
                            value="KFC",
                        ),
                    ],
                    width=3,
                ),
            ],
            className="mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Button(
                            id="hit-button",
                            children="Submit",
                            style={"background-color": "blue", "color": "white"},
                        )
                    ],
                    width=2,
                )
            ],
            className="mt-2",
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="bargragh", figure={})], width=6),
                dbc.Col([dcc.Graph(id="scatter_fig", figure={})], width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            id="notification",
                            children="",
                            style={"textAlign": "center"},
                        )
                    ],
                    width=12,
                )
            ]
        ),
    ]
)


# pull data from twitter and create the figures
@app.callback(
    Output(component_id="bargragh", component_property="figure"),
    Output(component_id="scatter_fig", component_property="figure"),
    Output(component_id="notification", component_property="children"),
    Input(component_id="hit-button", component_property="n_clicks"),
    State(component_id="count-mentions", component_property="value"),
    State(component_id="input-handle", component_property="value"),
)
def display_value(n_clicks, num, acnt_handle):
    results = api.GetSearch(
        raw_query=f"q=%40{acnt_handle}&src=typed_query&count={num}"
    )      
    twt_followers, twt_likes, twt_text, twt_friends, twt_name = [], [], [], [], [],
    for line in results:
        twt_likes.append(line.user.favourites_count)
        twt_followers.append(line.user.followers_count)
        twt_friends.append(line.user.friends_count)
        twt_name.append(line.user.screen_name)
        twt_text.append(line.user.description)

        print(line)

    d = {
        "followers": twt_followers,
        "likes": twt_likes,
        "friends": twt_friends,
        "name": twt_name,
        "text": twt_text,
    }
    #creating a pandas DataFrame for the tweets fetched.
    df = pd.DataFrame(d)
    print(df.head())

    '''functions for data cleaning : 
    removal of punctuation marks, extra spaces and lemmatization'''
# removing @ and #
    def clean_data(df):
        df = re.sub(r"@\S+ ", r"", df) 
        df = re.sub(r"#\S+", r"", df)
        #removing extra spaces
        df = re.sub("\s+", '', df)
        return df
#cleaning the data
    df['text'] = df['text'].apply(lambda x:clean_data(x))
#lemmatization
    lemmatizer = WordNetLemmatizer()
    df["text"]= df["text"].apply(lambda x:[lemmatizer.lemmatize(word) for word in x])

# using our model VADER to perform sentiment analysis.
    sent_analyzer = SentimentIntensityAnalyzer()
    df['scores'] = df['text'].apply(lambda text: sent_analyzer.polarity_scores(text))
    df['compound']  = df['scores'].apply(lambda score_dict: score_dict['compound'])
    df['comp_score'] = df['compound'].apply(lambda c: 'positive' if c >=0 else 'negative')
    df.reset_index()
#Graphs
# 1. Bar grah for sentiments
    bargraph = px.bar(df, x= 'comp_score', y = df.index,
    labels={'index':'No. of tweets',
    'comp_score':'Sentiment analysis'},color = 'comp_score', title = "Results of the Sentiment Analysis")
    return dcc.Graph(figure=bargraph, config={"displayModeBar":False})

# 2. Scatter plot for followers and likes
    scatter_fig = px.scatter(
        df, x="followers", y="likes", trendline="ols", hover_data={"name": True}, title="A scatter plot of the no. of followers Vs no. of likes.")
    return dcc.Graph(figure=scatter_fig, config={"displayModeBar":False})
    
    message = "The dashboard displays a bar graph showing the results of the sentiment analysis carried out on the tweets fetched from the twitter handle. The positive bar shows the positive tweets and negative bar shows the negative tweets associated with the twitter handle "
    
    return message
    
   
 
  