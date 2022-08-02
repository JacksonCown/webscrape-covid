from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
print("Starting")

app.layout = html.Div(children=[
    html.H1(children='Database Management - CSCI 4370'),

    dcc.Dropdown(["Test1", "Test2", "Test3"], "Test2", id="dropdown"),

    html.Div(children='''
        Select Response Variable:
    '''),

    dcc.RadioItems(
        id='metric', 
        options=[
            {'label': "Confirmed Cases", 'value': 'Confirmed'},
            {'label': "Confirmed Deaths", 'value': 'Deaths'},
            {'label': "Testing Rate", 'value': 'Testing_Rate'},
            {'label': "Mortality Rate", 'value': 'Mortality_Rate'}
        ],
        value="Confirmed",
        inline=True
    ),

    dcc.Graph(
        id='graph'
    ),

    dcc.Graph(
        id='graph2'
    )



])

@app.callback(
    Output("graph", "figure"), 
    Input("metric", "value"))
def display_choropleth(metric):
    df = pd.read_csv("data/bigTable.csv")
    # Our Graph
    fig = px.choropleth(df, locations='Province_State', locationmode="USA-states", color=metric,
                           animation_frame="Date",
                           color_continuous_scale="Blackbody_r",
                           scope="usa")

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)