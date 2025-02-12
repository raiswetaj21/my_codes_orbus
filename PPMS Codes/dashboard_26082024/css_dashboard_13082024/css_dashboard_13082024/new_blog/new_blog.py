import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')


# UDF for number cards ##########################################################################################
def create_number_card(title, value):
    # Create a single number card
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode='number',
            value=value,
            title={'text': title, 'font': {'size': 21}},
            number={'font': {'size': 32}},
            domain={'x': [0, 1], 'y': [0, 1]}
        )
    )

    # Update layout
    fig.update_layout(
        height=250,
        width=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    return fig

def create_number_card1(title, value):
    # Create a single number card
    data = {'title': title, 'value': value}

    return data


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
        title={
            'text': title,
            'font': {
                'size': 24,
                'color': 'Black'
            },
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',  # Center the title horizontally
            'y': 0.95  # Adjust vertical position if needed
        },
        margin=dict(t=50, l=50, r=50, b=50)  # Adjust margins as needed
    )

    return fig


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

#################################################################################################################
