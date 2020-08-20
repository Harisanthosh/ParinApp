import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import requests
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
parin_url = 'https://api.parin.io/sensor/4221'
headers = {'x-api-key': 'w3HkNadqoJ2KKtM1hgOn76RhGfwdi2dH1E2FW1sZ'}


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div(style={'textAlign': 'center'},children=[
    html.H1(children='Parin App'),

    html.Div(children='''
        Parin: A real time production line monitoring system which collects data every 2 minutes
    '''),

    dcc.Graph(
        id='example-graph'
    ),
    html.H4(id='live-update-text'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # 2000 milliseconds = 2 seconds
        n_intervals=0
    )
     
])
             
@app.callback(Output('example-graph', 'figure'),[Input('interval-component', 'n_intervals')])
def update_layout(n):
    r = requests.get('https://api.parin.io/sensor/4221', headers=headers)
    
    #dict_r = r.json()
    temp_arr = []
    timestamp_arr = []
    
    dict_val = json.loads(r.text)
    for val in dict_val:
        temp_arr.append(val['temperature'])
        timestamp_arr.append(val['timestamp'])
    
    df = pd.DataFrame({
        "Temp": temp_arr,
        "Date": timestamp_arr
    })
    
    fig = px.line(df, x="Date", y="Temp")
    
    return fig

application = app.server

if __name__ == '__main__':
    application.run(debug=True, port=8080)