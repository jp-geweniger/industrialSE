from dash import html
import pandas as pd

class OverviewTab:
    @staticmethod
    def create_overview_section(df):
        """Erzeugt die Übersichts-Sektion mit den wichtigsten Kennzahlen und Top/Flop Stores."""

        # Debugging: Prüfen, ob DataFrame existiert und Spalten korrekt geladen wurden
        print(f"📌 DEBUG: Spalten im DataFrame: {df.columns}")
        print(f"📌 DEBUG: Erste Zeilen des DataFrames:\n{df.head()}")
        print(f"📌 DEBUG: Datentypen:\n{df.dtypes}")

        # Falls df leer ist oder nicht existiert
        if df is None or df.empty:
            return html.P("⚠️ Keine Daten verfügbar.")

        # Überprüfung, ob alle notwendigen Spalten existieren
        required_columns = ["MonthlySalesRevenue", "CustomerFootfall", "MarketingSpend", "PromotionsCount", "StoreID", "StoreCategory", "StoreLocation"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            return html.P(f"⚠️ Fehler: Fehlende Spalten im DataFrame: {', '.join(missing_columns)}")

        # Konvertiere 'MonthlySalesRevenue' in numerischen Typ, falls nötig
        df["MonthlySalesRevenue"] = pd.to_numeric(df["MonthlySalesRevenue"], errors="coerce")

        # Prüfen, ob nach der Konvertierung noch gültige Werte existieren
        if df["MonthlySalesRevenue"].isna().all():
            return html.P("⚠️ Fehler: Alle Umsatzwerte sind ungültig oder fehlen!")

        # Berechnungen der wichtigsten KPIs
        total_revenue = df["MonthlySalesRevenue"].sum()
        avg_footfall = df["CustomerFootfall"].mean()
        total_marketing_spend = df["MarketingSpend"].sum()
        total_promotions = df["PromotionsCount"].sum()

        # Top 5 und Flop 5 Stores nach Umsatz bestimmen
        top_5_stores = df.nlargest(5, "MonthlySalesRevenue")[["StoreID", "MonthlySalesRevenue", "StoreCategory", "StoreLocation"]].reset_index(drop=True)
        flop_5_stores = df.nsmallest(5, "MonthlySalesRevenue")[["StoreID", "MonthlySalesRevenue", "StoreCategory", "StoreLocation"]].reset_index(drop=True)

        # HTML-Listen für die Stores erstellen
        def create_store_list(stores, icon):
            return html.Ul([
                html.Li(
                    f"{icon} {i + 1}. Platz - Store {row['StoreID']} "
                    f"({row['StoreCategory']}, {row['StoreLocation']}): "
                    f"${row['MonthlySalesRevenue']:,.2f}"
                )
                for i, row in stores.iterrows()
            ])

        # Endgültige HTML-Struktur zurückgeben
        return html.Div([
            html.H3("📊 Alle Zahlen in k$"),
            html.Ul([
                html.Li(f"📈 Gesamtumsatz: ${total_revenue:,.2f}"),
                html.Li(f"👥 Durchschnittliche Kundenfrequenz: {avg_footfall:,.0f}"),
                html.Li(f"💰 Gesamt-Marketingbudget: ${total_marketing_spend:,.2f}"),
                html.Li(f"🎯 Gesamtanzahl der Werbeaktionen: {total_promotions}")
            ]),
            html.H3("🏅 Top 5 Stores nach Umsatz"),
            create_store_list(top_5_stores, "🏆"),
            html.H3("📉 Flop 5 Stores nach Umsatz"),
            create_store_list(flop_5_stores, "❌")
        ])
