import plotly.express as px


def create_chart(chart_type, df, *cols, **kwargs):
    if chart_type == 'bar':
        return create_bar_chart(df, *cols, **kwargs)
    elif chart_type == 'pie':
        return create_pie_chart(df, *cols, **kwargs)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")


def create_bar_chart(df, *cols, title='Bar Chart', xlabel='X', ylabel='Count'):
    if len(cols) == 1:
        counts = df[cols[0]].value_counts().reset_index()
        counts.columns = [cols[0], 'Count']
        fig = px.bar(counts, x=cols[0], y='Count', title=title, labels={cols[0]: xlabel, 'Count': ylabel})
    elif len(cols) == 2:
        fig = px.bar(df, x=cols[0], y=cols[1], title=title, labels={cols[0]: xlabel, cols[1]: ylabel})
    else:
        raise ValueError("Bar chart requires 1 or 2 columns")
    return fig


def create_pie_chart(df, *cols, title='Pie Chart'):
    if len(cols) == 1:
        # Single column: Count the occurrences and create a pie chart
        counts = df[cols[0]].value_counts().reset_index()
        counts.columns = [cols[0], 'Count']
        fig = px.pie(counts, names=cols[0], values='Count', title=title)
    elif len(cols) == 2:
        fig = px.pie(df, names=cols[0], values=cols[1], title=title)
    else:
        raise ValueError("Pie chart requires 1 or 2 columns")
    return fig