import sqlite3
import pandas as pd
import os


class SQLiteConnector:
    """ Klasse zum Verbinden und Abfragen von SQLite-Datenbanken (JE)"""

    def __init__(self, db_path):

        self.db_path = os.path.abspath(db_path)  # Stellt sicher, dass der Pfad absolut ist

        # Überprüfe, ob die Datenbank existiert
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f" Fehler: Die Datenbank '{self.db_path}' wurde nicht gefunden.")

    def fetch_data(self, query):

        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except sqlite3.Error as e:
            print(f" SQLite-Fehler: {e}")
            return pd.DataFrame()  # Gibt einen leeren DataFrame zurück, falls ein Fehler auftritt
