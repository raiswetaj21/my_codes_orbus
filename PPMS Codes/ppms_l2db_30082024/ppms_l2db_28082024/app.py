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
card_1_value, card_2_value, card_3_value, card_4_value = generate_number_card_data()
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
number_card_3 = create_number_card(card_3_value, "Total Number of Milestones")
number_card_4 = create_number_card(card_4_value, "Total Number of Orders")
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
    # Title row
    dbc.Row([
        dbc.Col(html.H2('PPMS Level 2 Dashboard', className='text-center text-bg-primary bg-opacity-75'), className='p-0'),
    ]),

    # First row with dropdowns and date picker
    dbc.Row([
        dbc.Col(
            html.Div(dcc.Dropdown(id='dropdown-1', options=[{'label': 'Option 1', 'value': '1'}], value='1'),
                     className='h-100')
            , md=4, className='mt-3'),
        dbc.Col(
            html.Div(dcc.Dropdown(id='dropdown-2', options=[{'label': 'Option 2', 'value': '2'}], value='2'),
                     className='h-100')
            , md=4, className='mt-3'),
        dbc.Col(
            html.Div(dcc.DatePickerSingle(id='date-picker', date='2024-08-28'), className='w-100')
            , md=4, className='mt-3'),
    ]),

    # Second row with cards and gauge charts
    dbc.Row([
        dbc.Col(
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                f"{number_card_1['title']}: {number_card_1['value']}",
                                body=True,
                                className='h-100'
                            ),
                            width=12
                        ),
                        dbc.Col(
                            dbc.Card(
                                f"{number_card_2['title']}: {number_card_2['value']}",
                                body=True,
                                className='h-100'
                            ),
                            width=12
                        ),
                        dbc.Col(
                            dbc.Card(
                                f"{number_card_3['title']}: {number_card_3['value']}",
                                body=True,
                                className='h-100'
                            ),
                            width=12
                        ),
                        dbc.Col(
                            dbc.Card(
                                f"{number_card_4['title']}: {number_card_4['value']}",
                                body=True,
                                className='h-100'
                            ),
                            width=12
                        ),
                    ],
                    className='g-2',  # Optional: Remove gutter spacing between columns
                ),
                fluid=True, className='p-0'
            ),
            md=4,
            className='mt-3'
        ),
        dbc.Col(
            html.Div(dcc.Graph(figure=gauge_chart_1), className='border shadow-sm p-3 rounded')
            , md=4, className='mt-3'),
        dbc.Col(
            html.Div(dcc.Graph(figure=gauge_chart_2), className='border shadow-sm p-3 rounded')
            , md=4, className='mt-3'),
    ]),

    # Third row with line chart, area chart, pie chart and exploded donut chart
    dbc.Row([
        dbc.Col(
            html.Div(dcc.Graph(figure=line_chart), className='border shadow-sm p-3 rounded')
            , md=3, className='mt-3'),
        dbc.Col(
            html.Div(dcc.Graph(figure=area_chart), className='border shadow-sm p-3 rounded')
            , md=3, className='mt-3'),
        dbc.Col(
            html.Div(dcc.Graph(figure=pie_chart), className='border shadow-sm p-3 rounded')
            , md=3, className='mt-3'),
        dbc.Col(
            html.Div(dcc.Graph(figure=exploded_donut_chart), className='border shadow-sm p-3 rounded')
            , md=3, className='mt-3'),
    ]),

    # Fourth row with bar chart, sunburst chart and table
    dbc.Row([
        dbc.Col(
            html.Div(dcc.Graph(figure=bar_chart), className='border shadow-sm p-3 rounded')
            , md=3, className='mt-3'),
        dbc.Col(
            html.Div(dcc.Graph(figure=sunburst_chart), className='border shadow-sm p-3 rounded')
            , md=3, className='mt-3'),
        dbc.Col(
            html.Div(detailed_table, className='border shadow-sm p-3 rounded h-100')
            , md=6, className='mt-3'),
    ]),
], className='container-fluid py-3')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9200)
