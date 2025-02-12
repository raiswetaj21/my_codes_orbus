# app.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dal.dal import (generate_number_card_data, generate_gauge_chart_data, generate_line_chart_data,
                 generate_area_chart_data, generate_pie_chart_data, generate_exploded_donut_data,
                 generate_bar_chart_data, generate_sunburst_chart_data, generate_table_data)
from business_logic.business_logic import (create_number_card, create_gauge_chart, create_line_chart,
                            create_area_chart, create_pie_chart, create_exploded_donut_chart,
                            create_bar_chart, create_sunburst_chart, create_detailed_table)

# Initialize Dash app with an external stylesheet for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Fetch synthetic data
card_1_value, card_2_value = generate_number_card_data()
gauge_value_1, gauge_value_2 = generate_gauge_chart_data()
line_data = generate_line_chart_data()
area_data = generate_area_chart_data()
pie_labels, pie_values = generate_pie_chart_data()
exploded_labels, exploded_values = generate_exploded_donut_data()
bar_categories, bar_values = generate_bar_chart_data()
sunburst_data = generate_sunburst_chart_data()
table_data = generate_table_data()

# Create charts
number_card_1 = create_number_card(card_1_value, "Total Number of Projects")
number_card_2 = create_number_card(card_2_value, "Total Number of Tasks")
gauge_chart_1 = create_gauge_chart(gauge_value_1, "Project Performance Meter")
gauge_chart_2 = create_gauge_chart(gauge_value_2, "Task Performance Meter")
line_chart = create_line_chart(line_data)
area_chart = create_area_chart(area_data)
pie_chart = create_pie_chart(pie_labels, pie_values)
exploded_donut_chart = create_exploded_donut_chart(exploded_labels, exploded_values)
bar_chart = create_bar_chart(bar_categories, bar_values)
sunburst_chart = create_sunburst_chart(sunburst_data)
detailed_table = create_detailed_table(table_data)

# Define the layout
app.layout = html.Div([
    # First row with dropdowns, number cards, and date picker
    dbc.Row([
        dbc.Col(dcc.DatePickerSingle(id='date-picker', date='2024-08-28'), width=2),
        dbc.Col(dcc.Dropdown(id='dropdown-1', options=[{'label': 'Option 1', 'value': '1'}], value='1'), width=2),
        dbc.Col(dcc.Dropdown(id='dropdown-2', options=[{'label': 'Option 2', 'value': '2'}], value='2'), width=2),
        dbc.Col(dbc.Card(f"{number_card_1['title']}: {number_card_1['value']}", body=True), width=2),
        dbc.Col(dbc.Card(f"{number_card_2['title']}: {number_card_2['value']}", body=True), width=2),
    ], className="mb-4"),

    # Second row with line chart, area chart, and pie chart
    dbc.Row([
        dbc.Col(dcc.Graph(figure=line_chart), width=4),
        dbc.Col(dcc.Graph(figure=area_chart), width=4),
        dbc.Col(dcc.Graph(figure=pie_chart), width=4),
    ]),

    # Third row with exploded donut chart, bar chart, and sunburst chart
    dbc.Row([
        dbc.Col(dcc.Graph(figure=exploded_donut_chart), width=4),
        dbc.Col(dcc.Graph(figure=bar_chart), width=4),
        dbc.Col(dcc.Graph(figure=sunburst_chart), width=4),
    ]),

    # Fourth row with gauge charts
    dbc.Row([
        dbc.Col(dcc.Graph(figure=gauge_chart_1), width=6),
        dbc.Col(dcc.Graph(figure=gauge_chart_2), width=6),
    ]),

    # Fifth row with detailed table
    dbc.Row([
        dbc.Col(detailed_table, width=12),
    ])
], style={'padding': '20px'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9200)
