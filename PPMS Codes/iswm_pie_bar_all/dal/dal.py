import pandas as pd
from iswm_pie_bar_all.db_config.db_config import get_db_connection
import warnings
warnings.filterwarnings("ignore") # suppress all warning messages


def get_data_from_db(table_name, x_column, date=None):
    try:
        conn = get_db_connection()
        query = f"SELECT {x_column}, COUNT(*) as Count, DATE_CLEAN_NEW FROM {table_name}"
        if date:
            query += f" WHERE DATE_CLEAN_NEW = '{date}'"
        query += f" GROUP BY {x_column}, DATE_CLEAN_NEW"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error querying database: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
