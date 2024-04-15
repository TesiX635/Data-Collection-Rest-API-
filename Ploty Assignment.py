# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
Site_df = spacex_df['Launch Site'].unique()
min_payload = int(min_payload)  # Replace min_payload with your DataFrame's min payload value
max_payload = int(max_payload)  # Replace max_payload with your DataFrame's max payload value
# Create a dash application
app = dash.Dash(__name__)

dropdown_list = [ {'label': 'ALL sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label':'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, {'label': 'KSC LC-39A', 'value':'KSC LC-39A'}, {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}]
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites

                                dcc.Dropdown(id='site-dropdown',
                                            options= dropdown_list,
                                            value= 'ALL',
                                            placeholder="All Sites",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload,max_payload],
                                                marks={i: str(i) for i in range(min_payload, max_payload + 1, 2000)},
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')])
def updated_pie_chart(selected_site):
    filtered_df = spacex_df
    if selected_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
                     names='Launch Site',
                     title='Total successful launches by site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== selected_site]

        success_count = filtered_df['class'].sum()
        failure_count = len(filtered_df) - success_count

        labels = ['1', '0']
        values = [success_count, failure_count]

        fig = px.pie(filtered_df, values=values,labels=labels,names=labels, title='Launch Success and Failure Rates for ' +selected_site)
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_plot(selected_site, payload_range):
    # Filter the DataFrame based on the payload range
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]

    # If a specific launch site is selected (not 'ALL'), filter for that site
    if selected_site == 'ALL':
        filtered_df = spacex_df

    # Create the scatter plot
        fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y='class',
        color="Booster Version Category",  # Optional: color points by class to differentiate success/failure
        title="Correlation between Payload and Success for all sites",
        labels={"class": "Launch Success"})  # Optional: Improve axis label readability
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1])]
        fig = px.scatter(
           filtered_df,
           x="Payload Mass (kg)",
           y='class',
           color="Booster Version Category",  # Optional: color points by class to differentiate success/failure
           title=f"Launch Success by Payload Mass for {selected_site} Site",
           labels={"class": "Launch Success"})
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()