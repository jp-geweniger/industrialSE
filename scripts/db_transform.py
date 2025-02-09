import sqlite3
import os

#JE

class StoreDataUpdater:
    """
    Diese Klasse kapselt die Logik, in eine bestehende SQLite-Tabelle
    eine neue Spalte einzufügen und diese fortlaufend zu befüllen.
    """

    def __init__(self, db_path: str):
        """
        Legt die Verbindung zur SQLite-Datenbank an und erstellt ein Cursor-Objekt.
        :param db_path: Pfad zur SQLite-Datenbankdatei.
        """
        self.db_path = os.path.abspath(db_path)  # Wandelt relativen in absoluten Pfad um
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.ensure_table_exists("StoreData")  # Stellt sicher, dass die Tabelle existiert

    def ensure_table_exists(self, table_name: str):
        """Prüft, ob die Tabelle existiert, und erstellt sie falls nötig."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        table_exists = self.cursor.fetchone()

        if not table_exists:
            print(f" Tabelle '{table_name}' existiert nicht. Sie wird nun erstellt...")
            self.cursor.execute(f"""
                CREATE TABLE {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT
                )
            """)
            self.conn.commit()
            print(f" Tabelle '{table_name}' erfolgreich erstellt!")

    def column_exists(self, table_name: str, column_name: str) -> bool:
        """Prüft, ob eine Spalte in der Tabelle existiert."""
        query = f"PRAGMA table_info({table_name})"
        self.cursor.execute(query)
        columns = [col[1] for col in self.cursor.fetchall()]
        return column_name in columns

    def add_column(self, table_name: str, column_name: str, column_type: str = "INTEGER"):
        """Fügt eine neue Spalte zur Tabelle hinzu, falls sie nicht existiert."""
        if self.column_exists(table_name, column_name):
            print(f" Spalte '{column_name}' existiert bereits in Tabelle '{table_name}'.")
            return

        try:
            alter_statement = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            self.cursor.execute(alter_statement)
            self.conn.commit()
            print(f" Spalte '{column_name}' wurde erfolgreich hinzugefügt.")
        except sqlite3.Error as e:
            print(f" Fehler beim Hinzufügen der Spalte: {e}")

    def fill_with_incrementing_values(self, table_name: str, column_name: str):
        """Befüllt die neu angelegte Spalte mit aufsteigenden Werten, beginnend bei 1."""
        try:
            if not self.column_exists(table_name, column_name):
                print(f" Spalte '{column_name}' existiert nicht in '{table_name}'.")
                return

            select_statement = f"SELECT rowid FROM {table_name} ORDER BY rowid"
            self.cursor.execute(select_statement)
            rows = self.cursor.fetchall()

            if not rows:
                print(f" Tabelle '{table_name}' enthält keine Einträge.")
                return

            update_statement = f"UPDATE {table_name} SET {column_name} = ? WHERE rowid = ?"
            data = [(i + 1, rid[0]) for i, rid in enumerate(rows)]
            self.cursor.executemany(update_statement, data)

            self.conn.commit()
            print(f" Spalte '{column_name}' erfolgreich mit fortlaufenden Werten gefüllt.")

        except sqlite3.Error as e:
            print(f" Fehler beim Aktualisieren der Werte: {e}")

    def close(self):
        """Schließt die Verbindung zur Datenbank."""
        self.conn.close()


if __name__ == "__main__":
    # Verzeichnis des aktuellen Skripts (liegt in "scripts/")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "Database.db")  # Setzt den relativen Pfad

    # Instanz erstellen
    updater = StoreDataUpdater(db_path)

    # Neue Spalte hinzufügen
    updater.add_column("StoreData", "StoreID", "INTEGER")

    # Spalte mit fortlaufenden Werten füllen
    updater.fill_with_incrementing_values("StoreData", "StoreID")

    # Verbindung schließen
    updater.close()
