import sqlite3


class StoreDataUpdater:
    """
    Diese Klasse kapselt die Logik, in eine bestehende SQLite-Tabelle
    eine neue Spalte einzufügen und diese fortlaufend zu befüllen.
    """

    def __init__(self, db_path: str = "Database.db"):
        """
        Legt die Verbindung zur SQLite-Datenbank an und erstellt ein Cursor-Objekt.

        :param db_path: Pfad zur SQLite-Datenbankdatei.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def add_column(self, table_name: str, column_name: str, column_type: str = "INTEGER"):
        """
        Fügt eine neue Spalte zur angegebenen Tabelle hinzu.
        Hinweis: Wenn die Spalte bereits existiert, wird SQLite einen Fehler werfen.

        :param table_name: Name der Tabelle.
        :param column_name: Name der neuen Spalte.
        :param column_type: Datentyp der Spalte. Standard: 'INTEGER'.
        """
        alter_statement = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        self.cursor.execute(alter_statement)
        self.conn.commit()

    def fill_with_incrementing_values(self, table_name: str, column_name: str):
        """
        Befüllt die neu angelegte Spalte mit aufsteigenden Werten, beginnend bei 1.
        Die Reihenfolge der Zeilen wird nach rowid bestimmt.

        :param table_name: Name der Tabelle, in der die Spalte liegt.
        :param column_name: Name der Spalte, die gefüllt werden soll.
        """
        # 1) Alle Zeilen nach rowid holen
        select_statement = f"SELECT rowid FROM {table_name} ORDER BY rowid"
        self.cursor.execute(select_statement)
        rows = self.cursor.fetchall()

        # 2) Aufsteigend hochzählen und in die Spalte eintragen
        counter = 1
        update_statement = f"UPDATE {table_name} SET {column_name} = ? WHERE rowid = ?"
        for (rid,) in rows:
            self.cursor.execute(update_statement, (counter, rid))
            counter += 1

        # 3) Änderungen speichern
        self.conn.commit()

    def close(self):
        """
        Schließt die Verbindung zur Datenbank.
        """
        self.conn.close()


if __name__ == "__main__":
    # Beispielhafte Verwendung:
    updater = StoreDataUpdater("../Database.db")

    # Neue Spalte hinzufügen
    updater.add_column("StoreData", "StoreID", "INTEGER")

    # Spalte mit fortlaufenden Werten füllen
    updater.fill_with_incrementing_values("StoreData", "StoreID")

    # Verbindung schließen
    updater.close()
