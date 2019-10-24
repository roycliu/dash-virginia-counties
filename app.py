import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff
import pandas as pd

########### Define a few variables ######

tabtitle = 'Virginia Counties'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data/download'
githublink = 'https://github.com/austinlasseter/dash-template'
varlist=['TotalPop', 'Men', 'Women', 'Hispanic',
       'White', 'Black', 'Native', 'Asian', 'Pacific', 'VotingAgeCitizen',
       'Income', 'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment', 'RUCC_2013']

df=pd.read_pickle('resources/va-stats.pkl')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H1('Virginia Census Data 2017'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select census variable:'),
                dcc.Dropdown(
                    id='stats-drop',
                    options=[{'label': i, 'value': i} for i in varlist],
                    value='TotalPop'
                ),
        ], className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='va-map')
        ], className='nine columns'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output('va-map', 'figure'),
              [Input('stats-drop', 'value')])
def display_results(selected_value):
    fig = ff.create_choropleth(
                            fips=df['FIPS'],
                            values=df[selected_value],
                            scope=['VA'],
                            county_outline={'color': 'rgb(255,255,255)', 'width': 0.5})
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
