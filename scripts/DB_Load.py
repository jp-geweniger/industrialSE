import sqlite3
import csv


# Verbindung zur Datenbank herstellen
connection = sqlite3.connect('../Database.db')
cursor = connection.cursor()

# Tabelle erstellen (falls noch nicht vorhanden)
class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS StoreData (
        
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

    def insert_data_from_csv(self, csv_file_path):
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                self.cursor.execute("""
                INSERT INTO StoreData (ProductVariety, MarketingSpend, CustomerFootfall, StoreSize, EmployeeEfficiency, StoreAge, CompetitorDistance, PromotionsCount, EconomicIndicator, StoreLocation, StoreCategory, MonthlySalesRevenue) 
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

    def commit_and_close(self):
        self.connection.commit()
        self.connection.close()

# Usage
db_manager = DatabaseManager('Database.db')
db_manager.create_table()
db_manager.insert_data_from_csv('../data/Store_CA Überarbeitet.csv')
db_manager.commit_and_close()

print("Daten erfolgreich in die Datenbank importiert.")
