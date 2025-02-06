from dash import html


class OverviewTab:
    @staticmethod
    def create_overview_section(df):
        """Erzeugt Übersichts-Sektion mit Top & Flop 5 Stores nach Umsatz."""

        # Wichtige Kennzahlen berechnen
        total_revenue = df["MonthlySalesRevenue"].sum()
        avg_footfall = df["CustomerFootfall"].mean()
        total_marketing_spend = df["MarketingSpend"].sum()
        total_promotions = df["PromotionsCount"].sum()

        # Top 5 und Flop 5 Stores nach Umsatz berechnen
        top_5_stores = df.nlargest(5, "MonthlySalesRevenue")[["StoreID", "MonthlySalesRevenue"]].reset_index(drop=True)
        flop_5_stores = df.nsmallest(5, "MonthlySalesRevenue")[["StoreID", "MonthlySalesRevenue"]].reset_index(
            drop=True)

        # HTML Liste für Top 5 Stores mit Platzierungen
        top_5_list = html.Ul([
            html.Li(f"🏆 {i + 1}. Platz - Store {row['StoreID']}: ${row['MonthlySalesRevenue']:,.2f}")
            for i, row in top_5_stores.iterrows()
        ])

        # HTML Liste für Flop 5 Stores mit Platzierungen
        flop_5_list = html.Ul([
            html.Li(f"❌ {i + 1}. Platz - Store {row['StoreID']}: ${row['MonthlySalesRevenue']:,.2f}")
            for i, row in flop_5_stores.iterrows()
        ])

        # Sektion erstellen
        return html.Div([
            html.H3("Overview"),
            html.Ul([
                html.Li(f"Total Monthly Sales Revenue: ${total_revenue:,.2f}"),
                html.Li(f"Average Customer Footfall: {avg_footfall:,.0f}"),
                html.Li(f"Total Marketing Spend: ${total_marketing_spend:,.2f}"),
                html.Li(f"Total Promotions: {total_promotions}")
            ]),

            html.H3("🏅 Top 5 Stores by Revenue"),
            top_5_list,

            html.H3("📉 Flop 5 Stores by Revenue"),
            flop_5_list
        ])