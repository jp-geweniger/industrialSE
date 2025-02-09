import sqlite3
import pandas as pd
import os

# Datenbank- und CSV-Dateipfade
DB_PATH = "Database.db"
CSV_PATH = "../data/Store_CA Überarbeitet.csv"  # Falls CSV woanders liegt, hier anpassen

""" JE """


def create_database():
    """Erstellt die SQLite-Datenbank, falls sie nicht existiert."""
    if not os.path.exists(DB_PATH):
        connection = sqlite3.connect(DB_PATH)
        connection.close()
        print(f" Datenbank '{DB_PATH}' wurde erstellt.")
    else:
        print(f" Datenbank '{DB_PATH}' existiert bereits.")


def create_table():
    """Erstellt die Tabelle StoreData, falls sie noch nicht existiert."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS StoreData (
        StoreID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Automatische Store-ID
        ProductVariety INTEGER,
        MarketingSpend INTEGER,
        CustomerFootfall INTEGER,
        StoreSize INTEGER,
        EmployeeEfficiency REAL,
        StoreAge INTEGER,
        CompetitorDistance INTEGER,
        PromotionsCount INTEGER,
        EconomicIndicator REAL,
        StoreLocation TEXT,
        StoreCategory TEXT,
        MonthlySalesRevenue REAL
    )
    """)

    connection.commit()
    connection.close()
    print(" Tabelle 'StoreData' wurde überprüft/erstellt.")


def insert_data_from_csv():
    """Lädt Daten aus der CSV-Datei in die SQLite-Datenbank."""
    if not os.path.exists(CSV_PATH):
        print(f" Fehler: Die CSV-Datei '{CSV_PATH}' wurde nicht gefunden.")
        return

    #  CSV-Datei einlesen
    df = pd.read_csv(CSV_PATH, delimiter=";", encoding="utf-8")

    #  Verbindung zur Datenbank
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    #  Prüfen ob die Tabelle Daten enthält
    cursor.execute("SELECT COUNT(*) FROM StoreData")
    count = cursor.fetchone()[0]

    if count > 0:
        print("⚠️ Die Tabelle 'StoreData' enthält bereits Daten. Lösche alte Einträge und lade neue Daten...")
        cursor.execute("DELETE FROM StoreData")  # Alle alten Einträge entfernen
        connection.commit()

    # 🔹 Daten in die Tabelle einfügen
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO StoreData 
        (ProductVariety, MarketingSpend, CustomerFootfall, StoreSize, EmployeeEfficiency, StoreAge, 
         CompetitorDistance, PromotionsCount, EconomicIndicator, StoreLocation, StoreCategory, MonthlySalesRevenue) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row['ProductVariety']),
            int(row['MarketingSpend']),
            int(row['CustomerFootfall']),
            int(row['StoreSize']),
            float(row['EmployeeEfficiency']),
            int(row['StoreAge']),
            int(row['CompetitorDistance']),
            int(row['PromotionsCount']),
            float(row['EconomicIndicator']),
            row['StoreLocation'],
            row['StoreCategory'],
            float(row['MonthlySalesRevenue']),
        ))

    connection.commit()
    connection.close()
    print(f" Daten aus 'data/Store_CA Überarbeitet.csv' erfolgreich in 'StoreData' gespeichert.")


#  Skript ausführen
if __name__ == "__main__":
    create_database()  # Erstellt die Datenbank
    create_table()  # Erstellt die Tabelle
    insert_data_from_csv()  # Lädt die CSV-Daten in die DB
