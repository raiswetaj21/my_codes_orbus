import pandas as pd
from bar_app.db_config.db_config import get_db_connection
import warnings

# Suppress specific warning from pandas
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")


def get_data_from_db(table_name, x_column, y_column, date=None):
    """
    Connects to the database and retrieves data from the specified table and columns.
    Optionally filter the data by a specific date.

    Parameters:
    table_name (str): The name of the table to query.
    x_column (str): The column name for the labels.
    y_column (str): The column name for the values.
    date (str): Optional date for filtering (format: 'YYYY-MM-DD').

    Returns:
    DataFrame: The resulting DataFrame from the query.
    """
    try:
        conn = get_db_connection()
        query = f"SELECT {x_column}, {y_column}, DeliveryDate FROM {table_name}"
        if date:
            query += f" WHERE DeliveryDate = '{date}'"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error querying database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
