import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = (
    spacex_df['Launch Site']
    .dropna()
    .unique()
)
launch_sites = sorted(launch_sites)

dropdown_options= [
    {'label': 'All Sites', 'value': 'ALL'}
    
] + [
    {'label': site, 'value': site} for site in launch_sites
]

suc_launch = spacex_df.groupby('Launch Site')['class'].sum().reset_index()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
 # TASK 1: Add a dropdown list to enable Launch Site selection                               
    html.Div([
        html.Label("Launch Site Selection:"),
        dcc.Dropdown(
            id='site-dropdown',     # dcc.Dropdown(id='site-dropdown',...)
            options= dropdown_options,
            value='ALL',    # The default select value is for ALL sites
            placeholder='Select A Launch Site'
        ),   

    ]),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites 
    html.Div([
        dcc.Graph(id='success-pie-chart')
    ]),   

     html.Br(),                       

# If a specific launch site was selected, show the Success vs. Failed counts for the site
                                                 
    html.Div([dcc.Graph(id='success-pie-chart',
        figure=px.pie(suc_launch,
        names='Launch Site',
        values='class',
        title= "Total Successful Launches by Site"
        )
    )
    ])
    ]),
    html.Br(),

# TASK 3: Add a slider to select payload range

    html.P("Payload range (Kg):"),                           
    dcc.RangeSlider(id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={
            int(min_payload): str(int(min_payload)),
            int(max_payload): str(int(max_payload))         
        },
        value=[min_payload,max_payload]
    ),

# TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                
                                #])
    html.Br(),

    # Scatter Plot
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart')
    ]),

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)

def get_pie_chart(selected_site):

    if selected_site == 'All':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Sucessful Counts of Launch'
        )
    else: # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Fails for {selected_site}'
        )
    return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)

def update_scatter(selected_site, payload_range):
    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site != 'ALL':
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]


    fig = px.scatter(
        filtered_df,
        x='payload Mass',
        y='class',
        color='Booster version Category',
        title='Paylaod vs Launch Results'
    )
    return fig
# Run the app
if __name__ == '__main__':
    app.run()
