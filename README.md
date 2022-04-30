# Problem statement.
Most poeple on twitter try to draw attention to their content by mentioning a twitter handle that has established itself and it has a high traffic of followers. Such activities can create a negative mentality about the twitter handle if the tweets mentioning the twitter handle are negative. 
To make twitter users aware of the type of associations their handles have, TweetAnalyzer was built.
# TweetAnalyzer
This is a dash app that has access to the advanced twitter search engine, hence enabling the app to fetch tweets of the mentioned twitter handle. The tweets are cleaned and sentiment analysis(analyzing the emotion/mood of the tweet) is performed on the tweets. The results are diaplyed in a bar chart. The results tell us if the tweets associated with the searched twitter handle are positive or negative. The scatter plot demonstrates the realationship between the likes and the followers.
## libraries used build the dashboard.
The following python libraries were used to build the dashboard:
- Dash plotly
- Twitter (python twitter)
- NLTK(Natural Language ToolKit)
- Re(Regular Expressions)
- ScikitLearn
- Plotly Express
- Pandas
- wordcloud.
## Model used.
### VADER(Valence Aware Dictionary and sEntiment Reasoner.
VADER is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media, and works well on texts from other domains.
The Compound Normalized result it returns, is based on several factors (such as punctuation, CASE , emojis, degree modifiers, slang & conjunctions)
## How to use the Dashboard.
Upon loading the dashboard
Input the twitter handle you'd like to perform sentiment analysis on and the number of tweeets to analyze
Click on the submit button.
Let the dashboard update for results.
