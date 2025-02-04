from dash import html

class OverviewTab:
    @staticmethod
    def create_overview_section(df):
        """Erzeugt Übersichts-Sektion."""
        total_revenue = df["MonthlySalesRevenue"].sum()
        avg_footfall = df["CustomerFootfall"].mean()
        total_marketing_spend = df["MarketingSpend"].sum()
        total_promotions = df["PromotionsCount"].sum()

        return html.Ul([
            html.Li(f"Total Monthly Sales Revenue: ${total_revenue:,.2f}"),
            html.Li(f"Average Customer Footfall: {avg_footfall:,.0f}"),
            html.Li(f"Total Marketing Spend: ${total_marketing_spend:,.2f}"),
            html.Li(f"Total Promotions: {total_promotions}")
        ])