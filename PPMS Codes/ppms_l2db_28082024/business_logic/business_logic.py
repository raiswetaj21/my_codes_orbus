# business_logic.py
import plotly.express as px
import plotly.graph_objects as go
import dash_table

def create_number_card(value, title):
    return {
        'title': title,
        'value': value
    }

def create_gauge_chart(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [0, 100]}}
    ))
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_line_chart(data):
    fig = px.line(data, x='Date', y='Value', title='Line Chart')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_area_chart(data):
    fig = px.area(data, x=data.index, y=data.columns, title='Area Chart')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_pie_chart(labels, values):
    fig = px.pie(names=labels, values=values, title='Pie Chart')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_exploded_donut_chart(labels, values):
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4, pull=[0.1, 0.1, 0.1])])
    fig.update_layout(title_text="Exploded Donut Chart", margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_bar_chart(categories, values):
    fig = px.bar(x=categories, y=values, title='Bar Chart')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_sunburst_chart(data):
    fig = px.sunburst(data, path=['parents', 'labels'], values='values', title='Sunburst Chart')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

def create_detailed_table(data):
    return dash_table.DataTable(
        data=data.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in data.columns],
        page_size=10,  # Set the number of rows per page
        filter_action='native',  # Enable filtering by column
        sort_action='native',    # Enable sorting
        editable=True,           # Make cells editable
        style_table={'overflowX': 'auto'},  # Make table responsive
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold',
            'textAlign': 'center',
        },
        style_cell={
            'textAlign': 'left',
            'padding': '5px',
            'minWidth': '100px',
            'maxWidth': '200px',
            'whiteSpace': 'normal',
        },
        style_data_conditional=[  # Conditional formatting example
            {
                'if': {'column_id': 'Status', 'filter_query': '{Status} = "Completed"'},
                'backgroundColor': '#c8e6c9',
                'color': 'black',
            },
            {
                'if': {'column_id': 'Status', 'filter_query': '{Status} = "In Progress"'},
                'backgroundColor': '#ffecb3',
                'color': 'black',
            },
            {
                'if': {'column_id': 'Status', 'filter_query': '{Status} = "Not Started"'},
                'backgroundColor': '#ffcdd2',
                'color': 'black',
            }
        ]
    )