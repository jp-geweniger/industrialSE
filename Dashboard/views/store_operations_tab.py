import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierung
import plotly.graph_objects as go

class StoreOperationsTab:

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
                "ProductVariety": "Product Variety",
                "EmployeeEfficiency": "Employee Efficiency"
            },
            hover_data=["StoreID"]
        )
        return fig

    @staticmethod
    def create_bubble_chart_with_best_point(df):
        """
        Erzeugt einen Bubble Chart, der den Zusammenhang zwischen ProductVariety,
        MonthlySalesRevenue und EmployeeEfficiency zeigt. Zusätzlich wird für jede StoreCategory
        der Punkt markiert, an dem der kombinierte Score (MonthlySalesRevenue * EmployeeEfficiency)
        am höchsten ist.

        - X-Achse: ProductVariety (Anzahl der angebotenen Produkte)
        - Y-Achse: MonthlySalesRevenue (Umsatz)
        - Bubble Size: EmployeeEfficiency (Größe der Blase entspricht der Effizienz)
        - Farbkodierung: StoreCategory (zeigt Unterschiede zwischen Store-Typen)

        Für jede Kategorie wird der "Best Point" separat als Stern markiert.
        Beim Mousehover werden für den Best Point dieselben Informationen angezeigt wie bei den anderen Blasen.
        """
        # Erstellt den Basis-Bubble Chart mit Plotly Express
        fig = px.scatter(
            df,
            x="ProductVariety",
            y="MonthlySalesRevenue",
            size="EmployeeEfficiency",
            color="StoreCategory",
            title="Product Variety vs Revenue vs Employee Efficiency (Best Points per Category)",
            labels={
                "ProductVariety": "Product Variety",
                "MonthlySalesRevenue": "Monthly Sales Revenue",
                "EmployeeEfficiency": "Employee Efficiency"
            },
            hover_data=["StoreID", "EmployeeEfficiency", "StoreCategory"]
        )

        # Kopie des DataFrames und Berechnung eines Scores, um den besten Punkt je Kategorie zu bestimmen.
        df = df.copy()
        df["score"] = df["MonthlySalesRevenue"] * df["EmployeeEfficiency"]

        # Für jede Kategorie: Bestimmt den Punkt mit maximalem Score
        for cat in df["StoreCategory"].unique():
            df_cat = df[df["StoreCategory"] == cat]
            if not df_cat.empty:
                best_idx = df_cat["score"].idxmax()
                best_point = df_cat.loc[best_idx]

                # Erstellt den Hovertext, der die gleichen Informationen enthält wie bei den anderen Bubbles
                hover_text = (
                    f"StoreID: {best_point['StoreID']}<br>"
                    f"Product Variety: {best_point['ProductVariety']}<br>"
                    f"Monthly Sales Revenue: {best_point['MonthlySalesRevenue']}<br>"
                    f"Employee Efficiency: {best_point['EmployeeEfficiency']}<br>"
                    f"StoreCategory: {best_point['StoreCategory']}"
                )

                # Fügt den besten Punkt als zusätzlichen Trace hinzu
                fig.add_trace(
                    go.Scatter(
                        x=[best_point["ProductVariety"]],
                        y=[best_point["MonthlySalesRevenue"]],
                        mode="markers+text",
                        marker=dict(
                            size=best_point["EmployeeEfficiency"] * 0.5,
                            color="black",
                            symbol="star"
                        ),
                        text=[f"Best {best_point['StoreCategory']}"],
                        textposition="top center",
                        name=f"Best {best_point['StoreCategory']}",
                        hoverinfo="text",
                        hovertext=[hover_text]
                    )
                )

        return fig

    @staticmethod
    def create_bubble_chart_operations(df):
        """Erzeugt das Blasendiagramm für Filialgröße, Effizienz und Umsatz, inklusive Hervorhebung des Best Point je Kategorie. (JE)"""
        # Erstellt den Basis-Bubble Chart mit Plotly Express
        fig = px.scatter(
            df,
            x="StoreSize",
            y="MonthlySalesRevenue",
            size="EmployeeEfficiency",
            color="StoreCategory",
            title="Store Size, Efficiency, and Revenue",
            labels={
                "StoreSize": "Store Size",
                "MonthlySalesRevenue": "Revenue",
                "EmployeeEfficiency": "Efficiency"
            },
            hover_data=["StoreID", "EmployeeEfficiency", "StoreCategory"]
        )

        # Kopiert den DataFrame und berechne einen Score, um den besten Punkt je Kategorie zu ermitteln.
        # Hier wird als Score das Produkt aus MonthlySalesRevenue und EmployeeEfficiency verwendet.
        df_copy = df.copy()
        df_copy["score"] = df_copy["MonthlySalesRevenue"] * df_copy["EmployeeEfficiency"]

        # Für jede StoreCategory: Bestimme den Punkt mit dem höchsten Score
        for cat in df_copy["StoreCategory"].unique():
            df_cat = df_copy[df_copy["StoreCategory"] == cat]
            if not df_cat.empty:
                best_idx = df_cat["score"].idxmax()
                best_point = df_cat.loc[best_idx]

                # Erstellt den Hovertext, der dieselben Informationen enthält wie bei den übrigen Bubbles
                hover_text = (
                    f"StoreID: {best_point['StoreID']}<br>"
                    f"Store Size: {best_point['StoreSize']}<br>"
                    f"Revenue: {best_point['MonthlySalesRevenue']}<br>"
                    f"Efficiency: {best_point['EmployeeEfficiency']}<br>"
                    f"StoreCategory: {best_point['StoreCategory']}"
                )

                # Fügt den Best Point als zusätzlichen Trace hinzu
                fig.add_trace(
                    go.Scatter(
                        x=[best_point["StoreSize"]],
                        y=[best_point["MonthlySalesRevenue"]],
                        mode="markers+text",
                        marker=dict(
                            size=best_point["EmployeeEfficiency"] * 0.5,
                            color="black",
                            symbol="star"
                        ),
                        text=[f"Best {best_point['StoreCategory']}"],
                        textposition="top center",
                        name=f"Best {best_point['StoreCategory']}",
                        hoverinfo="text",
                        hovertext=[hover_text]
                    )
                )
        return fig

    @staticmethod
    def create_scatter_customerfootfall_efficiency(df):
        """
        Erzeugt ein Streudiagramm mit Trendlinie, das den Zusammenhang zwischen CustomerFootfall
        (Anzahl der Kundenbesuche) und EmployeeEfficiency (Mitarbeitereffizienz) untersucht. (JPG)

        - X-Achse: CustomerFootfall (Anzahl der Kundenbesuche)
        - Y-Achse: EmployeeEfficiency (Effizienz der Mitarbeiter, z. B. auf einer Skala von 0–100)
        - Farb-Codierung: StoreCategory (zeigt branchenspezifische Unterschiede)
        - Trendlinie: Fügt eine lineare Regression (OLS) hinzu, die den generellen Trend in der Beziehung veranschaulicht.
        """
        fig = px.scatter(
            df,
            x="CustomerFootfall",
            y="EmployeeEfficiency",
            color="StoreCategory",  # Unterscheidung der Datenpunkte nach StoreCategory
            trendline="ols",  # Trendlinie als lineare Regression (OLS)
            title="Customer Footfall vs Employee Efficiency",
            labels={
                "CustomerFootfall": "Customer Footfall",
                "EmployeeEfficiency": "Employee Efficiency"
            },
            hover_data=["StoreID"]
        )
        return fig

    @staticmethod
    def create_histogram_efficiency(df):
        """Erzeugt das Histogramm für die Verteilung der Mitarbeitereffizienz. (JE)"""
        return px.histogram(
            df, x="EmployeeEfficiency",
            title="Employee Efficiency Distribution",
            labels={"EmployeeEfficiency": "Efficiency"},
            hover_data=["StoreID"]
        )
