import plotly.express as px

class PerformanceInsightsTab:

    @staticmethod
    def create_scatter_marketing_revenue(df):
        """Erzeugt das Streudiagramm für Marketingausgaben vs. Umsatz."""
        return px.scatter(df, x="MarketingSpend", y="MonthlySalesRevenue",
                          title="Marketing Spend vs Revenue",
                          labels={"MarketingSpend": "Marketing Spend", "MonthlySalesRevenue": "Revenue"},
                          hover_data=["StoreID"])

    @staticmethod
    def create_box_plot_category(df):
        """Erzeugt das Boxplot-Diagramm für den Umsatz nach Geschäftskategorie."""
        return px.box(df, x="StoreCategory", y="MonthlySalesRevenue",
                      title="Revenue by Store Category",
                      labels={"StoreCategory": "Store Category", "MonthlySalesRevenue": "Revenue"},
                      hover_data=["StoreID"])