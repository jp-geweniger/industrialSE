import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierung

class StoreOperationsTab:

    # 🔹 Einheitliche Farben für jede StoreCategory
    category_colors = {
        "Electronic": "#1f77b4",  # Blau
        "Grocery": "#2ca02c",     # Grün
        "Clothing": "#d62728"     # Rot
    }

    @staticmethod
    def create_bubble_chart_operations(df):
        """Erzeugt das Blasendiagramm für Filialgröße, Effizienz und Umsatz."""
        return px.scatter(
            df, x="StoreSize", y="MonthlySalesRevenue",
            size="EmployeeEfficiency", color="StoreCategory",
            color_discrete_map=StoreOperationsTab.category_colors,  # 🔹 Feste Farben
            title="Store Size, Efficiency, and Revenue",
            labels={"StoreSize": "Store Size", "MonthlySalesRevenue": "Revenue", "EmployeeEfficiency": "Efficiency"},
            hover_data=["StoreID"]
        )

    @staticmethod
    def create_histogram_efficiency(df):
        """Erzeugt das Histogramm für die Verteilung der Mitarbeitereffizienz."""
        return px.histogram(
            df, x="EmployeeEfficiency",
            title="Employee Efficiency Distribution",
            labels={"EmployeeEfficiency": "Efficiency"},
            hover_data=["StoreID"]
        )

    @staticmethod
    def create_scatter_productvariety_revenue(df):
        """Erzeugt ein Streudiagramm für Produktvielfalt vs. Umsatz mit festen Farben."""
        fig = px.scatter(
            df, x="ProductVariety", y="MonthlySalesRevenue",
            color="StoreCategory",
            color_discrete_map=StoreOperationsTab.category_colors,  # 🔹 Feste Farben
            trendline="ols",
            title="Product Variety vs Revenue",
            labels={"ProductVariety": "Product Variety", "MonthlySalesRevenue": "Revenue"},
            hover_data=["StoreID"]
        )
        return fig

    @staticmethod
    def create_scatter_productvariety_efficiency(df):
        """Erzeugt ein Streudiagramm für Produktvielfalt vs. Mitarbeitereffizienz mit festen Farben."""
        fig = px.scatter(
            df, x="ProductVariety", y="EmployeeEfficiency",
            color="StoreCategory",
            color_discrete_map=StoreOperationsTab.category_colors,  # 🔹 Feste Farben
            trendline="ols",
            title="Product Variety vs Employee Efficiency",
            labels={"ProductVariety": "Product Variety (Anzahl der verschiedenen Produkte)",
                    "EmployeeEfficiency": "Employee Efficiency (Skala 0–100)"},
            hover_data=["StoreID"]
        )
        return fig
