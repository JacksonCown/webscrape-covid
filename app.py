from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
print("Starting")

# HTML Layout
app.layout = html.Div(id="page", children=[
    # Header
    html.H1(children='Database Management - CSCI 4370'),

    html.Div(children="Choose Graph Data: "),
    # Dropdown Graph Select
    dcc.Dropdown(id='dropdown',
        options=[
            {'label': "Confirmed Cases, Deaths, Rates USA", 'value': 'cases'},
            {'label': "Sex and Age USA", 'value': 'sexAge'},
            {'label': "Vaccination USA", 'value': 'vaccine'}
        ],
        value="cases",
        persistence=False),
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

# Dynamically update graph components
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
        cases = pd.read_csv("data/bigTable.csv")

        # Render Graph
        fig = px.choropleth(cases, locations='Province_State', locationmode="USA-states", color=metric,
                            animation_frame="Date",
                            color_continuous_scale="Blackbody_r",
                            scope="usa")

        # Adjust layout
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return f'Select Response Metric: ', choices, fig
    elif dropdown == "sexAge":
        # Multichoice for Demographics Data Graph
        choices = [{'label': "Male", 'value': 'male'},
            {'label': "Female", 'value': 'female'},
            {'label': "Both", 'value': 'both'}]

        # Retrieve Data and build DataFrame
        sex_age = pd.read_csv("data/SexAndAge/COVID-19_Death_Counts_by_Age_2020-2022.csv")
        # Compute Ratio of Total Deaths to Covid-19 Deaths for graphing
        sex_age = sex_age.assign(percent_deaths_from_covid = (sex_age["COVID-19 Deaths"] / sex_age["Total deaths"])*100)

        # Update Based on Sex Toggle
        if metric == "male":
            male = sex_age[sex_age.Sex == "Male"]
            fig = px.bar(male, x="Age Years", y="percent_deaths_from_covid")
        elif metric == "female":
            female = sex_age[sex_age.Sex == "Female"]
            fig = px.bar(female, x="Age Years", y="percent_deaths_from_covid")
        else:
            fig = px.bar(sex_age, x="Age Years", y="percent_deaths_from_covid", color="Sex")

        return f'Select Sex: ', choices, fig
    else:
        # Multichoice for Vaccine Data Graph
        choices = [{'label': "Moderna", 'value': 'Moderna'},
                    {'label': "Janssen", 'value': 'Janssen'},
                    {'label': "Pfizer", 'value': 'Pfizer'}, 
                    {'label': "All", 'value': 'All'}]

        # Access Data tables and build DataFrames
        vaccine_df = pd.read_csv("data/Vaccine2.csv")
        location = pd.read_csv("data/location.csv")
        
        # Merge the DataFrames into one table
        vaccine_df = vaccine_df.merge(location, on='FIPS')

        # Update Graph components based on Vaccine Type Toggle
        if metric == "Moderna":
            Moderna = vaccine_df[vaccine_df.Vaccine == "Moderna"]
            fig = px.choropleth(Moderna, locations="Province_State", locationmode="USA-states", color="Vax_Full",
                            animation_frame="Date",
                            color_continuous_scale="RdBu",
                            scope="usa")

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        elif metric == "Janssen":
            Janssen = vaccine_df[vaccine_df.Vaccine == "Janssen"]
            fig = px.choropleth(Janssen, locations="Province_State", locationmode="USA-states", color="Vax_Full",
                            animation_frame="Date",
                            color_continuous_scale="RdBu",
                            scope="usa")

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        elif metric == "Pfizer":
            Pfizer = vaccine_df[vaccine_df.Vaccine == "Pfizer"]
            fig = px.choropleth(Pfizer, locations="Province_State", locationmode="USA-states", color="Vax_Full",
                            animation_frame="Date",
                            color_continuous_scale="RdBu",
                            scope="usa")

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        else:
            all = vaccine_df[vaccine_df.Vaccine == "All"]
            fig = px.choropleth(all, locations="Province_State", locationmode="USA-states", color="Vax_Full",
                            animation_frame="Date",
                            color_continuous_scale="RdBu",
                            scope="usa")

            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return f'Select Vaccine Type: ', choices, fig

if __name__ == '__main__':
    app.run_server(debug=True)