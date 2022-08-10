import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

tabtitle = 'A map of poor wages'
sourceurl = 'https://www.kaggle.com/datasets/lislejoem/us-minimum-wage-by-state-from-1968-to-2017'
githublink = 'https://github.com/daniel-varela-3/306-agriculture-exports-dropdown'
# here's the list of possible columns to choose from.
list_of_columns =['Lowest minimum wage','Highest minimum wage','Median minimum wage']


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/min_wage_data_v4.csv')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1('Historical Minimum Wage'),
    html.Div([
        html.Div([
                html.H6('Select a statistic for your analysis:'),
                dcc.Dropdown(
                    id='options-drop',
                    options=[{'label': i, 'value': i} for i in list_of_columns],
                    value='Lowest minimum wage'
                ),
        ], className='two columns'),
        html.Div([dcc.Graph(id='figure-1'),
            ], className='ten columns'),
    ], className='twelve columns'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('options-drop', 'value')])
def make_figure(varname):
    mygraphtitle = f'{varname} since 1968, by state'
    mycolorscale = 'algae' # Note: The error message will list possible color scales.
    mycolorbartitle = "Minimum wage (USD)"

    data=go.Choropleth(
        locations=df['State_code'], # Spatial coordinates
        locationmode = 'USA-states', # set of locations match entries in `locations`
        z = df[varname].astype(float), # Data to be color-coded
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    )
    fig = go.Figure(data)
    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
