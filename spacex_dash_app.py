# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                options=[
                                        {'label': 'All Site', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                    placeholder='Select a Launch site here',
                                    searchable=True,
                                    style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,
                                    value = [0, 10000]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( [Output(component_id='success-pie-chart', component_property='figure')],
               [Input(component_id='site-dropdown', component_property='value')],
            )
def get_pie_chart(launch_site):
    print(launch_site)
    if launch_site == 'ALL':
        success_rate_all_df = spacex_df.groupby('Launch Site')['class'].mean()
        success_rate_all_df = success_rate_all_df.to_frame()
        success_rate_all_df.reset_index(inplace=True)
        pie_chart = px.pie(success_rate_all_df, values='class', names='Launch Site', title='Success rate of all launch sites')
    else:
        site_wise_df = spacex_df.loc[spacex_df['Launch Site'] == launch_site]['class'].value_counts()
        site_wise_df = site_wise_df.to_frame()
        site_wise_df.reset_index(inplace=True)
        site_wise_df.columns = ['class', 'counts']
        pie_chart = px.pie(site_wise_df, values='counts', names='class', title='Success & Failure for selecte site')
    return [pie_chart]
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( [Output(component_id='success-payload-scatter-chart', component_property='figure')],
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')
               ],
            )
def get_scatter_plot(launch_site, value):
    if launch_site == 'ALL':
        min_val = value[0]
        max_val = value[1]
        # df_sub = df.loc[df['Launch Site'] == 'CCAFS LC-40']
        df_sub = spacex_df.loc[spacex_df['Payload Mass (kg)'] <= max_val]
        df_sub = df_sub[df_sub['Payload Mass (kg)'] >= min_val]
        scatter_plot = px.scatter(x='Payload Mass (kg)', y='class', color='Booster Version Category', data_frame=df_sub)
    else:
        min_val = value[0]
        max_val = value[1]
        df_sub = spacex_df.loc[spacex_df['Launch Site'] == launch_site]
        df_sub = df_sub.loc[df_sub['Payload Mass (kg)'] <= max_val]
        df_sub = df_sub[df_sub['Payload Mass (kg)'] >= min_val]
        scatter_plot = px.scatter(x='Payload Mass (kg)', y='class', color='Booster Version Category', data_frame=df_sub)
    return [scatter_plot]

# Run the app
if __name__ == '__main__':
    app.run_server()
