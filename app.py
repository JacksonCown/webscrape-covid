from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
print("Starting")

# HTML Layout
app.layout = html.Div(id="page", children=[
    # Header
    html.H1(children='Database Management - CSCI 4370'),

    # Dropdown Graph Select
    dcc.Dropdown(id='dropdown',
        options=[
            {'label': "Confirmed Cases, Deaths, Rates USA", 'value': 'cases'},
            {'label': "Sex and Age USA", 'value': 'sexAge'},
            {'label': "Vaccination USA", 'value': 'vaccine'}
        ],
        value="cases"),
    html.Div(id="dropdown-output"),

    # Individual Graph Selects
    dcc.RadioItems(
        id='metric', 
        inline=True
    ),

    # Render Graph
    dcc.Graph(
        id='graph'
    )
])

# No clue how to break this into smaller subcomponents yet
@app.callback(
    [Output("dropdown-output", "children"), Output("metric", "options"), Output("graph", "figure")], 
    [Input("dropdown", "value"), Input("metric", "value")])
def display_choropleth(dropdown, metric):
    print(f'Dropdown Choice: {dropdown}')
    if dropdown == "cases":
        # Multichoice for Cases Data Graph
        choices = [{'label': "Confirmed Cases", 'value': 'Confirmed'},
            {'label': "Confirmed Deaths", 'value': 'Deaths'},
            {'label': "Testing Rate", 'value': 'Testing_Rate'},
            {'label': "Mortality Rate", 'value': 'Mortality_Rate'}]
        
        # Read data and build DataFrame
        df = pd.read_csv("data/bigTable.csv")

        # Render Graph
        fig = px.choropleth(df, locations='Province_State', locationmode="USA-states", color=metric,
                            animation_frame="Date",
                            color_continuous_scale="Blackbody_r",
                            scope="usa")

        # Adjust layout
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return f'Select Response Metric: ', choices, fig
    elif dropdown == "sexAge":
        # Multichoice for Demographics data
        choices = [{'label': "Male", 'value': 'male'},
            {'label': "Female", 'value': 'female'},
            {'label': "Both", 'value': 'both'}]

        # Read data and build DataFrame
        sex_age = pd.read_csv("data/SexAndAge/COVID-19_Death_Counts_by_Age_2020-2022.csv")

        # Swap data used for male, female, and both case
        if metric == "male":
            male = sex_age[sex_age.Sex == "Male"]
            fig = px.bar(male, x="Age Years", y="COVID-19 Deaths")
        elif metric == "female":
            female = sex_age[sex_age.Sex == "Female"]
            fig = px.bar(female, x="Age Years", y="COVID-19 Deaths")
        else:
            fig = px.bar(sex_age, x="Age Years", y="COVID-19 Deaths", color="Sex")

        return f'Select Sex: ', choices, fig
    else:
        
        # Multichoice for Demographics data
        choices = [{'label': "Male", 'value': 'male'},
            {'label': "Female", 'value': 'female'},
            {'label': "Both", 'value': 'both'}]
        # Todo: Implement correct graph for vaccine table
        # Place Holder Code Below
        df = pd.read_csv("data/bigTable.csv")
        # Our Graph
        fig = px.choropleth(df, locations='Province_State', locationmode="USA-states", color=metric,
                            animation_frame="Date",
                            color_continuous_scale="Blackbody",
                            scope="usa")

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return f'Test', _,  fig

if __name__ == '__main__':
    app.run_server(debug=True)