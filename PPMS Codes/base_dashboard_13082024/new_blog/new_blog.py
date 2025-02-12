import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
# import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# UDF for number cards ##########################################################################################
def create_number_cards(projects_total, projects_completed, assets_total, assets_under_maintenance):
    # Define the number cards data
    cards = [
        {'title': 'Total Projects', 'value': projects_total},
        {'title': 'Completed Projects', 'value': projects_completed},
        {'title': 'Total Assets', 'value': assets_total},
        {'title': 'Assets Under Maintenance', 'value': assets_under_maintenance}
    ]

    # Create a subplot layout
    fig = go.Figure()

    # Add each card as a subplot in a single row
    for i, card in enumerate(cards):
        fig.add_trace(
            go.Indicator(
                mode='number',
                value=card['value'],
                title={'text': card['title'], 'font': {'size': 21}},
                number={'font': {'size': 32}},
                domain={'row': 0, 'column': i}
            )
        )

    # Update layout to arrange the cards in a single row
    fig.update_layout(
        grid=dict(rows=1, columns=4),
        height=250,
        width=1200,
        title_x=0.1
    )

    return fig


# Example usage
# fig = create_number_cards(projects_total=120, projects_completed=88, assets_total=300, assets_under_maintenance=45)
# fig.show()


# UDF for gradient bar chart ####################################################################################
def generate_gradient_bar_chart(df, x_col, y_col, title='Gradient Bar Chart'):
    # Create the bar chart
    fig = go.Figure()

    # Add bars to the figure with a gradient color based on y_col values
    fig.add_trace(go.Bar(
        x=df[x_col],
        y=df[y_col],
        marker=dict(
            color=df[y_col],  # Use y_col values for gradient color
            colorscale='Viridis',  # You can change this to any other colorscale
            colorbar=dict(title=y_col)
        )
    ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        coloraxis_colorbar_title=y_col
    )

    return fig


# Sample DataFrame
# data = {
#     'Project Category': ['Proj A', 'Proj B', 'Proj C', 'Proj D', 'Proj E'],
#     'Value': [10, 15, 7, 20, 12]
# }
# df = pd.DataFrame(data)
#
# # Generate the bar chart
# fig = generate_gradient_bar_chart(df, 'Project Category', 'Value')
# fig.show()


# UDF for exploded donut chart ##################################################################################
def generate_exploded_donut_chart(df, names_col, values_col, explode_amount=0.09, title='Exploded Donut Chart'):
    # Create the explode list with the specified amount for all slices
    explode = [explode_amount] * len(df)

    # Create the pie chart
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=df[names_col],
        values=df[values_col],
        pull=explode,  # Apply the explosion
        textinfo='label+percent',  # Display label and percentage
        hole=0.9  # Optional: makes it a donut chart
    ))

    # Update layout
    fig.update_layout(
        title=title,
        legend_title='Project Categories'
    )

    return fig


# Generate the donut chart with all slices exploded
# fig = generate_exploded_donut_chart(df, 'Project Category', 'Value')
# fig.show()


# UDF for performance gauge chart ##############################################################################
def generate_gauge_chart(value, max_value=100, title='Performance Gauge Chart'):
    # Create the gauge chart
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 21}},
        gauge=dict(
            axis=dict(
                range=[0, max_value],
                tickwidth=2,
                tickcolor='black'
            ),
            bar=dict(
                color='lightblue'
            ),
            bgcolor='white',
            bordercolor='black',
            borderwidth=2,
            steps=[
                dict(range=[0, max_value * 0.2], color='lightcoral'),
                dict(range=[max_value * 0.2, max_value * 0.3], color='lightsalmon'),
                dict(range=[max_value * 0.3, max_value], color='lightgreen')
            ],
            threshold=dict(
                line=dict(color='red', width=4),
                thickness=0.75,
                value=value
            )
        )
    ))

    # Update layout
    fig.update_layout(
        font=dict(size=16)
    )

    return fig


# Generate the gauge chart with a current value of 75
# fig = generate_gauge_chart(value=75)
# fig.show()


# UDF for project stage funnel chart ###########################################################################
def generate_funnel_chart(stage_labels, stage_values, title='Funnel Chart'):
    # Create the funnel chart
    fig = go.Figure()

    fig.add_trace(go.Funnel(
        y=stage_labels,
        x=stage_values,
        textinfo="value+percent initial"
    ))

    # Update layout to add title
    fig.update_layout(
        title_text=title,
        xaxis_title='Value',
        yaxis_title='Stage'
    )

    return fig


# # Sample data for the funnel chart
# stage_labels = ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4']
# stage_values = [1000, 800, 500, 200]
#
# # Generate the funnel chart
# fig = generate_funnel_chart(stage_labels, stage_values, title='Project Stage Funnel')
# fig.show()


# UDF for actual vs expected line chart ########################################################################
def generate_line_chart(actual_dates, actual_values, expected_dates, expected_values, title):
    # Create the figure
    fig = go.Figure()

    # Add trace for actual data
    fig.add_trace(go.Scatter(
        x=actual_dates,
        y=actual_values,
        mode='lines+markers',
        name='Actual',
        line=dict(width=4)  # Thickness of the line for actual data
    ))

    # Add trace for expected data
    fig.add_trace(go.Scatter(
        x=expected_dates,
        y=expected_values,
        mode='lines+markers',
        name='Expected',
        line=dict(width=2, dash='dash')  # Thickness and style of the line for expected data
    ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Value',
        legend_title='Legend',
        xaxis=dict(
            tickformat='%Y-%m-%d'  # Adjust the date format if needed
        )
    )

    return fig


# # Sample data
# actual_dates = ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']
# actual_values = [10, 15, 13, 17]
#
# expected_dates = ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01']
# expected_values = [12, 14, 15, 16]
#
# # Generate the line chart
# fig = generate_line_chart(actual_dates, actual_values, expected_dates, expected_values, title='Actual vs Expected Timeline')
# fig.show()


# UDF for project timeline gantt chart ##########################################################################
def generate_gantt_chart(tasks, title):
    # Create the Gantt chart
    fig = ff.create_gantt(
        tasks,
        show_colorbar=True,  # Show the color bar
        index_col='Task',  # Use 'Task' as the color grouping
        title=title,
        showgrid_x=True,  # Show grid lines for x-axis
        showgrid_y=True,  # Show grid lines for y-axis
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Timeline',
        yaxis_title='Tasks',
        xaxis=dict(
            type='date',
            tickformat='%Y-%m-%d'  # Adjust the date format if needed
        ),
        yaxis=dict(
            autorange="reversed"  # Reverse the y-axis to show tasks from top to bottom
        )
    )

    return fig


# # Sample data for the Gantt chart
# tasks = [
#     dict(Task="Project A", Start='2024-01-01', Finish='2024-02-28'),
#     dict(Task="Project B", Start='2024-03-05', Finish='2024-04-15'),
#     dict(Task="Project C", Start='2024-02-20', Finish='2024-05-30')
# ]
#
# # Generate and show the Gantt chart
# fig = generate_gantt_chart(tasks, title='Project Timeline Gantt Chart:\n')
# fig.show()


# UDF for project data sunburst chart ##########################################################################
def generate_sunburst_chart(df, path, values, color, title):
    # Create the sunburst chart
    fig = px.sunburst(
        df,
        path=path,
        values=values,
        color=color
    )

    # Update layout for better readability
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=24, color='Black')
        ),
        margin=dict(t=50, l=50, r=50, b=50)  # Adjust margins as needed
    )

    return fig


# # Sample data for the sunburst chart
# df = px.data.tips()
#
# # Generate and show the sunburst chart
# fig = generate_sunburst_chart(df, path=['sex', 'day', 'time'], values='total_bill', color='day',
#                               title='Project Data Sunburst Chart')
# fig.show()


# UDF for 100% stacked horizontal bar chart for projects #######################################################
def generate_100_percent_stacked_bar_chart(df, x_col, y_col, color_col, title):
    # Calculate total values per category
    total_values = df.groupby(y_col)[x_col].transform('sum')

    # Calculate percentage values
    df['Percentage'] = df[x_col] / total_values * 100

    # Create the 100% stacked horizontal bar chart
    fig = px.bar(
        df,
        x='Percentage',
        y=y_col,
        color=color_col,
        text='Percentage',
        orientation='h',
        title=title,
        labels={x_col: x_col, y_col: y_col, color_col: color_col}
    )

    # Update layout to stack bars and normalize to 100%
    fig.update_layout(
        barmode='stack',
        xaxis_title='Percentage',
        yaxis_title=y_col,
        yaxis=dict(
            title='',
            autorange='reversed'
        )
    )

    # Format the text to show percentages inside the bars
    fig.update_traces(
        texttemplate='%{text:.1f}%',  # Format percentage labels
        textposition='inside'
    )

    return fig


# # Sample data for the chart
# data = {
#     'Category': ['Proj A', 'Proj A', 'Proj B', 'Proj B', 'Proj C', 'Proj C', 'Proj D', 'Proj D'],
#     'Subcategory': ['Complete', 'Incomplete', 'Complete', 'Incomplete', 'Complete', 'Incomplete', 'Complete',
#                     'Incomplete'],
#     'Value': [10, 20, 30, 40, 50, 60, 70, 80]
# }
# df = pd.DataFrame(data)
#
# # Generate and show the 100% stacked horizontal bar chart
# fig = generate_100_percent_stacked_bar_chart(df, x_col='Value', y_col='Category', color_col='Subcategory',
#                                              title='100% Stacked Horizontal Bar Chart for Projects')
# fig.show()


# UDF for bar chart with trend line ############################################################################
def create_bar_with_trend_line(df, x_col, y_col, trend_line_col=None, title='Bar Graph with Trend Line'):
    fig = go.Figure()

    # Add bars to the figure
    fig.add_trace(
        go.Bar(
            x=df[x_col],
            y=df[y_col],
            name='Target Values',
            marker_color='rgba(58, 51, 70, 0.6)'  # Bar color
        )
    )

    # Add trend line if specified
    if trend_line_col:
        fig.add_trace(
            go.Scatter(
                x=df[x_col],
                y=df[trend_line_col],
                mode='lines+markers',
                name='Trend Line',
                line=dict(color='red', width=2)  # Trend line color and width
            )
        )

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        xaxis=dict(
            title='Month',
            tickmode='linear'  # Use linear mode for x-axis ticks
        ),
        yaxis=dict(
            title='Target'
        ),
        barmode='group'
    )

    return fig


# Sample DataFrame with trend line
# data = {
#     'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
#     'Target': [200, 300, 250, 400, 350, 450],
#     'Trend': [210, 310, 260, 390, 360, 470]
# }
# df = pd.DataFrame(data)
#
# # Generate and show the bar graph with trend line
# fig = create_bar_with_trend_line(df, x_col='Month', y_col='Target', trend_line_col='Trend',
#                                  title='Monthly Target with Trend Line')
# fig.show()
#################################################################################################################
