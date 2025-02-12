import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd
from new_blog import new_blog  # Importing chart creation functions


# Synthetic Data Creation for charts and graphs
# Sample DataFrame for bar chart with trend line
data1 = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'Target': [200, 300, 250, 400, 350, 450],
    'Trend': [210, 310, 260, 390, 360, 470]
}
df_bar_with_trend = pd.DataFrame(data1)

# Sample DataFrame for exploded pie chart
data2 = {
    'Project Category': ['Proj A', 'Proj B', 'Proj C', 'Proj D', 'Proj E'],
    'Value': [10, 15, 7, 20, 12]
}
df_exploded_pie = pd.DataFrame(data2)

# 26082024
cardData = [
    {'title': 'card-1', 'value': 100},
    {'title': 'card-2', 'value': 200},
    {'title': 'card-3', 'value': 300},
    {'title': 'card-4', 'value': 400},
]

def generateCards(data):
    cards = []
    for x in data:
        card = dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(x['title'], className="card-title text-center"),
                        html.H4(x['value'], className="card-title text-center"),
                    ]
                ),
            ),
            md=3, className='mt-2'
        )
        cards.append(card)
    return cards

# Sample list for line chart
actual_dates = ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']
actual_values = [10, 15, 13, 17]
expected_dates = ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']
expected_values = [12, 14, 15, 16]

# Sample list for the funnel chart
stage_labels = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4']
stage_values = [1000, 800, 500, 200]

# Sample list for the gantt chart
tasks = [
    dict(Task="Project A", Start='2024-01-01', Finish='2024-02-28'),
    dict(Task="Project B", Start='2024-03-05', Finish='2024-04-15'),
    dict(Task="Project C", Start='2024-02-20', Finish='2024-05-30')
]

# Sample DataFrame for the sunburst chart
df_sunburst = px.data.tips()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

x = new_blog.create_number_card1('hello', 100);

# Layout for the dashboard
app.layout = dbc.Container([
    # Dashboard Heading
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Level 1 Dashboard", className='text-center text-primary')
            ]),
        ])
    ]),
    # Top Row Cards
    dbc.Row(generateCards(cardData)),
    # 1st Row Charts
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(figure=new_blog.create_bar_with_trend_line(df_bar_with_trend, x_col='Month', y_col='Target',
                                                                     trend_line_col='Trend',
                                                                     title='Monthly Target with Trend Line')),
            ],className='border border-secondary my-3' ),
        ], md=4, ),
        dbc.Col([
            html.Div([
                dcc.Graph(figure=new_blog.generate_sunburst_chart(df_sunburst, path=['sex', 'day', 'time'],
                                                                  values='total_bill', color='day',
                                                                  title='Project Data Sunburst Chart')),
            ],className='border border-secondary  my-3' ),

        ], md=4),
        dbc.Col([
            html.Div([
                dcc.Graph(figure=new_blog.generate_gauge_chart(value=75)),
            ],className='border border-secondary  my-3' ),
        ], md=4)
    ]),
    # 2nd Row Charts
    dbc.Row([
      dbc.Col([
          html.Div([
              dcc.Graph(figure=new_blog.generate_exploded_donut_chart(df_exploded_pie, 'Project Category', 'Value')),
          ],className='border border-secondary mb-3' ),
      ], md=4),
        dbc.Col([
            html.Div([
                dcc.Graph(
                    figure=new_blog.generate_funnel_chart(stage_labels, stage_values, title='Project Stage Funnel')),
            ],className='border border-secondary  mb-3' ),
        ], md=4),
        dbc.Col([
            html.Div([
                dcc.Graph(
                    figure=new_blog.generate_line_chart(actual_dates, actual_values, expected_dates, expected_values,
                                                        title='Actual vs Expected Timeline')),
            ] ,className='border border-secondary  mb-3'),
        ], md=4),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(figure=new_blog.generate_gantt_chart(tasks, title='Project Timeline Gantt Chart')),
            ],className='border border-secondary  my-3' ),
        ], md=12),
    ]),

], fluid=True, className='container-fluid')


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=2121)
