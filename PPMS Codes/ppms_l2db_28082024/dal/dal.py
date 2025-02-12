# dal.py
import pandas as pd
import numpy as np

def generate_number_card_data():
    # Generate synthetic data for number cards
    card_1_value = np.random.randint(100, 1000)
    card_2_value = np.random.randint(100, 1000)
    return card_1_value, card_2_value

def generate_gauge_chart_data():
    # Generate synthetic data for gauge charts
    gauge_value_1 = np.random.randint(0, 100)
    gauge_value_2 = np.random.randint(0, 100)
    return gauge_value_1, gauge_value_2

def generate_line_chart_data():
    # Generate synthetic data for a line chart
    dates = pd.date_range(start='2024-01-01', periods=100)
    values = np.random.randint(50, 150, size=100)
    return pd.DataFrame({'Date': dates, 'Value': values})

def generate_area_chart_data():
    # Generate synthetic data for an area chart
    categories = ['Project A', 'Project B', 'Project C', 'Project D']
    values = np.random.rand(4, 3) * 100
    return pd.DataFrame(values, columns=['Q1', 'Q2', 'Q3'], index=categories)

def generate_pie_chart_data():
    # Generate synthetic data for a pie chart
    labels = ['Task 1', 'Task 2', 'Task 3']
    values = np.random.randint(10, 100, 3)
    return labels, values

def generate_exploded_donut_data():
    # Generate synthetic data for an exploded donut chart
    labels = ['Order 1', 'Order 2', 'Order 3']
    values = np.random.randint(20, 80, 3)
    return labels, values

def generate_bar_chart_data():
    # Generate synthetic data for a bar chart
    categories = ['Milestone 1', 'Milestone 2', 'Milestone 3']
    values = np.random.randint(50, 200, 3)
    return categories, values

def generate_sunburst_chart_data():
    # Generate synthetic data for a sunburst chart
    data = pd.DataFrame({
        'labels': ['Root', 'Branch 1', 'Branch 2', 'Leaf 1', 'Leaf 2'],
        'parents': ['', 'Root', 'Root', 'Branch 1', 'Branch 2'],
        'values': [100, 50, 50, 25, 25]
    })
    return data

def generate_table_data():
    # Generate synthetic data for a detailed table
    data = pd.DataFrame({
        'Project Name': ['Project A', 'Project B', 'Project C'],
        'Start Date': ['2024-01-01', '2024-02-01', '2024-03-01'],
        'End Date': ['2024-06-01', '2024-07-01', '2024-08-01'],
        'Status': ['In Progress', 'Completed', 'Not Started'],
        'Budget': [50000, 75000, 60000]
    })
    return data
