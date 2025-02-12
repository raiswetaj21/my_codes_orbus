import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dal.dal import get_data_from_db
from business_logic.business_logic import generate_pie_chart
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Get today's date
today_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Sweeper Attendance Count Pie Chart"),

    # Single date picker set to current date
    html.Div([
        html.Label("Select Valid Date: "),
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
    df = get_data_from_db('DP_SWEEPER_ATT_BASE_2', 'ATTENDANCE', selected_date)
    return generate_pie_chart(df, 'ATTENDANCE')


# Run the server
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=9500)
