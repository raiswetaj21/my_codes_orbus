import plotly.express as px
from dash import html


def generate_pie_chart(df, x_column):
    try:
        # Check if dataframe is empty
        if df.empty:
            return html.Div("\nNo data available for the selected date. Please choose another valid date.")

        # Plotting the pie chart
        fig = px.pie(df, names=x_column, values='Count', title=f'Pie Chart of {x_column} Distribution')

        # Convert figure to HTML
        graph_html = fig.to_html(full_html=False)

        return html.Div([html.Iframe(srcDoc=graph_html, width='100%', height='500px')])
    except Exception as e:
        print(f"Error plotting chart: {e}")
        return html.Div("Error generating chart.")
