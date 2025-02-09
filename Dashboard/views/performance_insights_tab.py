import plotly.express as px


class PerformanceInsightsTab:
    """Klasse für die Erstellung von Diagrammen im Performance Insights-Tab. (JE und JPG)"""

    @staticmethod
    def create_scatter_marketing_revenue(df):
        """
        Erzeugt ein Streudiagramm, das den Zusammenhang zwischen Marketingausgaben und Umsatz darstellt.

        - X-Achse: MarketingSpend (Marketingausgaben, z. B. in Tausend $)
        - Y-Achse: MonthlySalesRevenue (Monatlicher Umsatz)
        - Farb-Codierung: StoreCategory (zeigt branchenspezifische Unterschiede)
        - Trendlinie: Fügt eine lineare Regressionslinie (OLS) hinzu, um den generellen Zusammenhang zu verdeutlichen.

        Die lineare Regression funktioniert wie in den bereits dokumentierten Beispielen. (JPG und JE)
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
        """Erzeugt ein verbessertes Boxplot-Diagramm für den Umsatz nach Geschäftskategorie mit festen Farben. (JE)"""

        # Sortiere Kategorien nach Medianwert
        category_order = df.groupby("StoreCategory")["MonthlySalesRevenue"].median().sort_values().index

        fig = px.box(
            df,
            x="StoreCategory",
            y="MonthlySalesRevenue",
            color="StoreCategory",
            title="Revenue by Store Category",
            labels={"StoreCategory": "Store Category", "MonthlySalesRevenue": "Revenue"},
            hover_data=["StoreID"],
            points="all",  # Zeigt alle Datenpunkte zusätzlich zum Boxplot
            category_orders={"StoreCategory": category_order},  # Sortiere nach Median
        )

        fig.update_layout(boxmode="overlay")  # Mehrere Boxplots überlagert anzeigen

        return fig

    @staticmethod
    def create_scatter_promotions_revenue(df):
        """
        Erzeugt ein Streudiagramm mit Trendlinie, das den Zusammenhang zwischen PromotionsCount
        (Anzahl der Promotion-Events) und MonthlySalesRevenue (Monatlicher Umsatz) darstellt. (JPG)

        - X-Achse: PromotionsCount (Anzahl der Promotion-Events)
        - Y-Achse: MonthlySalesRevenue (Monatlicher Umsatz)
        - Farb-Codierung: StoreCategory (zeigt branchenspezifische Unterschiede)
        - Trendlinie: Fügt eine lineare Regressionslinie (OLS) hinzu, um den generellen Trend zu verdeutlichen.
        """
        fig = px.scatter(
            df,
            x="PromotionsCount",
            y="MonthlySalesRevenue",
            color="StoreCategory",  # Unterscheidung nach StoreCategory
            trendline="ols",  # Trendlinie als lineare Regression (OLS)
            title="Promotions vs Revenue",
            labels={
                "PromotionsCount": "Promotions Count (Anzahl der Promotion-Events)",
                "MonthlySalesRevenue": "Monthly Sales Revenue (Umsatz)"
            },
            hover_data=["StoreID"]
        )
        return fig
