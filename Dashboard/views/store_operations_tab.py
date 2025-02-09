import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierung

class StoreOperationsTab:

    @staticmethod
    def create_bubble_chart_operations(df):
        """Erzeugt das Blasendiagramm für Filialgröße, Effizienz und Umsatz. (JE)"""
        return px.scatter(
            df, x="StoreSize", y="MonthlySalesRevenue",
            size="EmployeeEfficiency", color="StoreCategory",
            title="Store Size, Efficiency, and Revenue",
            labels={"StoreSize": "Store Size", "MonthlySalesRevenue": "Revenue", "EmployeeEfficiency": "Efficiency"},
            hover_data=["StoreID"]
        )

    @staticmethod
    def create_histogram_efficiency(df):
        """Erzeugt das Histogramm für die Verteilung der Mitarbeitereffizienz. (JE)"""
        return px.histogram(
            df, x="EmployeeEfficiency",
            title="Employee Efficiency Distribution",
            labels={"EmployeeEfficiency": "Efficiency"},
            hover_data=["StoreID"]
        )

    @staticmethod
    def create_scatter_productvariety_revenue(df):
        """
        Erzeugt ein Streudiagramm, das den Zusammenhang zwischen Produktvielfalt und Umsatz darstellt. (JPG)

        - X-Achse: ProductVariety (Produktvielfalt)
        - Y-Achse: MonthlySalesRevenue (Monatlicher Umsatz)
        - Farb-Codierung: StoreCategory (um branchenspezifische Unterschiede hervorzuheben)
        - Trendlinie: Fügt eine lineare Regressionslinie hinzu (OLS), um den Trend visuell zu unterstützen.
        """
        fig = px.scatter(
            df,
            x="ProductVariety",
            y="MonthlySalesRevenue",
            color="StoreCategory",
            trendline="ols",  # Trendlinie als lineare Regression (OLS)
            title="Product Variety vs Revenue",
            labels={
                "ProductVariety": "Product Variety",
                "MonthlySalesRevenue": "Revenue"
            },
            hover_data=["StoreID"]
        )
        return fig

    @staticmethod
    def create_scatter_productvariety_efficiency(df):
        """
        Erzeugt ein Streudiagramm mit Trendlinie, das den Zusammenhang zwischen
        der Produktvielfalt (ProductVariety) und der Mitarbeitereffizienz (EmployeeEfficiency) darstellt. (JPG)

        - X-Achse: ProductVariety (Anzahl der verschiedenen Produkte im Store)
        - Y-Achse: EmployeeEfficiency (Mitarbeitereffizienz, Skala 0–100)
        - Farb-Codierung: StoreCategory (zeigt branchenspezifische Unterschiede)
        - Trendlinie: Fügt eine lineare Regressionslinie (OLS) hinzu, die den allgemeinen Trend
          zwischen Produktvielfalt und Effizienz verdeutlicht.
        """
        fig = px.scatter(
            df,
            x="ProductVariety",
            y="EmployeeEfficiency",
            color="StoreCategory",
            trendline="ols",  # Fügt eine lineare Regressions-Trendlinie hinzu
            title="Product Variety vs Employee Efficiency",
            labels={
                "ProductVariety": "Product Variety (Anzahl der verschiedenen Produkte)",
                "EmployeeEfficiency": "Employee Efficiency (Skala 0–100)"
            },
            hover_data=["StoreID"]
        )
        return fig
