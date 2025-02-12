import plotly.express as px
from dash import html


def generate_pie_chart_agg(df, x_column, y_column):
    """
    Generates a pie chart from the specified DataFrame columns using Plotly.

    Parameters:
    df (DataFrame): The DataFrame containing the data.
    x_column (str): The column name for the labels.
    y_column (str): The column name for the values.

    Returns:
    html.Div: The HTML representation of the pie chart.
    """
    try:
        # Check if dataframe is empty
        if df.empty:
            return html.Div("\nNo data available for the selected date. Please choose another valid date.")

        # Aggregate the data by the x_column
        aggregated_df = df.groupby(x_column).sum().reset_index()

        # Plotting the pie chart
        fig = px.pie(aggregated_df, names=x_column, values=y_column,
                     title=f'Pie Chart of {x_column} vs {y_column}')

        # Convert figure to HTML
        graph_html = fig.to_html(full_html=False)

        return html.Div([html.Iframe(srcDoc=graph_html, width='100%', height='500px')])
    except Exception as e:
        print(f"Error plotting chart: {e}")
        return html.Div("Error generating chart.")
