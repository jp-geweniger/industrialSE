import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierung

class CustomerInsightsTab:
    """View für Kundenbezogene Einblicke. (JPG und JE)"""

    @staticmethod
    def create_scatter_footfall_revenue(df):
        """
        Erzeugt das Streudiagramm für Customer Footfall vs. Monthly Sales Revenue. (JE und JPG)
        - X-Achse: CustomerFootfall
        - Y-Achse: MonthlySalesRevenue
        - Farb-Codierung: StoreCategory
        - Trendline: Lineare Regression (OLS)
        Wie funktioniert die lineare Regression hier?

        1. Durch den Parameter trendline="ols" signalisiert Plotly Express,
           dass eine lineare Regression (Ordinary Least Squares, OLS) berechnet werden soll.

        2. Plotly Express extrahiert die X- und Y-Daten (hier CustomerFootfall und MonthlySalesRevenue)
           aus dem DataFrame.

        3. Intern wird das statsmodels-Paket verwendet, um ein OLS-Modell zu erstellen.
           Dabei wird ein Modell in der Form:

              y = m * x + b

           aufgebaut, wobei:
             - y die abhängige Variable (MonthlySalesRevenue) darstellt,
             - x die unabhängige Variable (CustomerFootfall) ist,
             - m den Steigungskoeffizienten und
             - b den y-Achsenabschnitt darstellt.

        4. Das OLS-Verfahren berechnet m und b so, dass die Summe der quadrierten Abweichungen
           (Residuen) zwischen den vorhergesagten und den tatsächlichen y-Werten minimiert wird.

        5. Die resultierende Regressionslinie wird dann automatisch in das Streudiagramm eingefügt,
           sodass man visuell den Einfluss des Customer Footfall auf den Umsatz erkennen kann.

        Hinweis: Für die Nutzung der Option trendline="ols" muss das Paket statsmodels installiert sein.
        """
        fig = px.scatter(
            df,
            x="CustomerFootfall",
            y="MonthlySalesRevenue",
            color="StoreCategory",  # Farb-Codierung nach StoreCategory: Unterscheidet die Datenpunkte anhand ihrer Kategorie. (JPG)
            trendline="ols",        # Fügt eine Trendline mittels linearer Regression (OLS) hinzu. (JPG)
            title="Customer Footfall vs Revenue",
            labels={
                "CustomerFootfall": "Customer Footfall",
                "MonthlySalesRevenue": "Revenue"
            },
            hover_data=["StoreID"]
        )
        return fig