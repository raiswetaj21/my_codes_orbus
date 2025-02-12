import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dal.dal import get_data_from_db
from business_logic.business_logic import create_chart
import datetime

app = dash.Dash(__name__)

# Get today's date
today_date = datetime.datetime.now().strftime('%Y-%m-%d')

app.layout = html.Div([
    dcc.DatePickerSingle(
        id='date-picker',
        date=today_date,
    ),
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'},
        ],
        value='bar'
    ),
    dcc.Graph(id='chart')
])


@app.callback(
    Output('chart', 'figure'),
    [Input('date-picker', 'date'),
     Input('chart-type', 'value')]
)
def update_chart(selected_date, chart_type):
    df = get_data_from_db('DP_SWEEPER_ATT_BASE_2', 'ATTENDANCE', selected_date)
    if chart_type == 'bar':
        return create_chart('bar', df, 'ATTENDANCE', title='Bar Chart', xlabel='ATTENDANCE')
    elif chart_type == 'pie':
        return create_chart('pie', df, 'ATTENDANCE', title='Pie Chart')


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=7500)
