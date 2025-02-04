import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierung

class StoreOperationsTab:
    @staticmethod
    def create_bubble_chart_operations(df):
        """Erzeugt das Blasendiagramm für Filialgröße, Effizienz und Umsatz."""
        return px.scatter(df, x="StoreSize", y="MonthlySalesRevenue",
                          size="EmployeeEfficiency", color="StoreCategory",
                          title="Store Size, Efficiency, and Revenue",
                          labels={"StoreSize": "Store Size", "MonthlySalesRevenue": "Revenue", "EmployeeEfficiency": "Efficiency"},
                          hover_data=["StoreID"])

    @staticmethod
    def create_histogram_efficiency(df):
        """Erzeugt das Histogramm für die Verteilung der Mitarbeitereffizienz."""
        return px.histogram(df, x="EmployeeEfficiency",
                            title="Employee Efficiency Distribution",
                            labels={"EmployeeEfficiency": "Efficiency"},
                            hover_data=["StoreID"])