import sqlite3
import pandas as pd

class SQLiteConnector:
    def __init__(self, db_path):
        self.db_path = db_path

    def fetch_data(self, query):
        """Fetch data from the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df