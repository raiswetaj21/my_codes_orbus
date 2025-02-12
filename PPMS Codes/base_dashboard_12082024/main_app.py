import dash
from dash import dcc
from dash import html
from new_blog import new_blog  # Importing chart creation functions
import pandas as pd
import plotly.express as px

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
app = dash.Dash(__name__)

# Layout for the dashboard
app.layout = html.Div([
    # Top row: Number cards
    html.Div([
        dcc.Graph(figure=new_blog.create_number_cards(projects_total=120, projects_completed=88, assets_total=300, assets_under_maintenance=45)),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px', 'height': '20vh'}),

    # Second row: Bar Chart with Trend Line, Exploded Donut Chart, Gauge Chart
    html.Div([
        html.Div([
            dcc.Graph(figure=new_blog.create_bar_with_trend_line(df_bar_with_trend, x_col='Month', y_col='Target', trend_line_col='Trend', title='Monthly Target with Trend Line')),
        ], style={'width': '32%', 'margin': '10px', 'box-sizing': 'border-box', 'height': '100%', 'overflow': 'hidden', 'border': '1px solid #ccc', 'border-radius': '8px'}),

        html.Div([
            dcc.Graph(figure=new_blog.generate_exploded_donut_chart(df_exploded_pie, 'Project Category', 'Value')),
        ], style={'width': '32%', 'margin': '10px', 'box-sizing': 'border-box', 'height': '100%', 'overflow': 'hidden', 'border': '1px solid #ccc', 'border-radius': '8px'}),

        html.Div([
            dcc.Graph(figure=new_blog.generate_gauge_chart(value=75)),
        ], style={'width': '32%', 'margin': '10px', 'box-sizing': 'border-box', 'height': '100%', 'overflow': 'hidden', 'border': '1px solid #ccc', 'border-radius': '8px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'height': '30vh'}),

    # Third row: Line Chart, Funnel Chart
    html.Div([
        html.Div([
            dcc.Graph(figure=new_blog.generate_line_chart(actual_dates, actual_values, expected_dates, expected_values, title='Actual vs Expected Timeline')),
        ], style={'width': '48%', 'margin': '10px', 'box-sizing': 'border-box', 'height': '100%', 'overflow': 'hidden', 'border': '1px solid #ccc', 'border-radius': '8px'}),

        html.Div([
            dcc.Graph(figure=new_blog.generate_funnel_chart(stage_labels, stage_values, title='Project Stage Funnel')),
        ], style={'width': '48%', 'margin': '10px', 'box-sizing': 'border-box', 'height': '100%', 'overflow': 'hidden', 'border': '1px solid #ccc', 'border-radius': '8px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'height': '30vh'}),

    # Bottom row: Gantt Chart, Sunburst Chart
    html.Div([
        html.Div([
            dcc.Graph(figure=new_blog.generate_gantt_chart(tasks, title='Project Timeline Gantt Chart')),
        ], style={'width': '48%', 'margin': '10px', 'box-sizing': 'border-box', 'height': '100%', 'overflow': 'hidden', 'border': '1px solid #ccc', 'border-radius': '8px'}),

        html.Div([
            dcc.Graph(figure=new_blog.generate_sunburst_chart(df_sunburst, path=['sex', 'day', 'time'], values='total_bill', color='day', title='Project Data Sunburst Chart')),
        ], style={'width': '48%', 'margin': '10px', 'box-sizing': 'border-box', 'height': '100%', 'overflow': 'hidden', 'border': '1px solid #ccc', 'border-radius': '8px'}),
    ], style={'display': 'flex', 'justify-content': 'space-between', 'height': '30vh'}),
], style={'height': '100vh', 'width': '100vw', 'padding': '10px', 'box-sizing': 'border-box', 'overflow': 'hidden'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=2121)
