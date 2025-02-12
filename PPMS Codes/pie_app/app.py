import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dal.dal import get_data_from_db
from business_logic.business_logic import generate_pie_chart_agg
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Get today's date
today_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Project Status Pie Chart"),

    # Single date picker set to current date
    html.Div([
        html.Label("Select Start Date: "),
        dcc.DatePickerSingle(
            id='date-picker',
            date=today_date  # Default date to today
        )
    ]),

    # Container for the pie chart
    html.Div(id='chart')
])


# Callback to update the chart based on the date picker input
@app.callback(
    Output('chart', 'children'),
    Input('date-picker', 'date')
)
def update_chart(selected_date):
    df = get_data_from_db('Projects', 'ProjectStatus', 'Budget', selected_date)
    return generate_pie_chart_agg(df, 'ProjectStatus', 'Budget')


# Run the server
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8500)
