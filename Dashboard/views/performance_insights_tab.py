import plotly.express as px

class PerformanceInsightsTab:

    @staticmethod
    def create_scatter_marketing_revenue(df):
        """
        Erzeugt ein Streudiagramm, das den Zusammenhang zwischen Marketingausgaben und Umsatz darstellt. (JPG)

        - X-Achse: MarketingSpend (Marketingausgaben, z. B. in Tausend $)
        - Y-Achse: MonthlySalesRevenue (Monatlicher Umsatz)
        - Farb-Codierung: StoreCategory (zeigt branchenspezifische Unterschiede)
        - Trendlinie: Fügt eine lineare Regressionslinie (OLS) hinzu, um den generellen Zusammenhang zu verdeutlichen.

        Die Funktionsweise der trendline wurde bereits in Beispielen anderer Tabs dieses Projekts dokumentiert.
        """
        fig = px.scatter(
            df,
            x="MarketingSpend",
            y="MonthlySalesRevenue",
            color="StoreCategory",  # Farb-Codierung nach StoreCategory, um Unterschiede zwischen Branchen zu zeigen
            trendline="ols",  # Fügt eine Trendlinie mittels linearer Regression (OLS) hinzu
            title="Marketing Spend vs Revenue",
            labels={
                "MarketingSpend": "Marketing Spend (in Tausend $)",
                "MonthlySalesRevenue": "Revenue (Umsatz)"
            },
            hover_data=["StoreID"]
        )
        return fig

    @staticmethod
    def create_box_plot_category(df):
        """Erzeugt das Boxplot-Diagramm für den Umsatz nach Geschäftskategorie."""
        return px.box(df, x="StoreCategory", y="MonthlySalesRevenue",
                      title="Revenue by Store Category",
                      color="StoreCategory",
                      labels={"StoreCategory": "Store Category", "MonthlySalesRevenue": "Revenue"},
                      hover_data=["StoreID"])