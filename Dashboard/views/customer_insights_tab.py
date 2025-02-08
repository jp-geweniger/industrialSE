import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierung

class CustomerInsightsTab:
    """View für Kundenbezogene Einblicke. (JPG und JE)"""

    @staticmethod
    def create_barchart_category_footfall(df):
        """
        Erzeugt ein Balkendiagramm, das den durchschnittlichen CustomerFootfall
        (Kundenbesuche) pro StoreCategory darstellt. (JPG)

        - X-Achse: StoreCategory
        - Y-Achse: Durchschnittlicher CustomerFootfall

        Vorgehensweise:
        1. Gruppierung des DataFrames nach StoreCategory und Berechnung des Durchschnitts
           der CustomerFootfall für jede Kategorie.
        2. Darstellung der Ergebnisse in einem Balkendiagramm, um die durchschnittliche
           Kundenfrequenz je Kategorie anschaulich zu visualisieren.
        """
        # Gruppiere nach StoreCategory und berechne den Durchschnitt der CustomerFootfall
        df_grouped = df.groupby("StoreCategory", as_index=False)["CustomerFootfall"].mean()

        # Erstelle das Balkendiagramm
        fig = px.bar(
            df_grouped,
            x="StoreCategory",
            y="CustomerFootfall",
            title="Average Customer Footfall pro Kategorie",
            labels={
                "StoreCategory": "Store Category",
                "CustomerFootfall": "Average Customer Footfall"
            },
            hover_data=["CustomerFootfall"]
        )
        return fig

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

    @staticmethod
    def create_scatter_marketing_footfall(df):
        """
        Erzeugt ein Streudiagramm mit Trendlinie, das den Zusammenhang zwischen Marketing-Ausgaben
        (MarketingSpend, in Tausend $) und der Anzahl der Kunden im Monat (CustomerFootfall) darstellt. (JPG)

        - X-Achse: MarketingSpend (Marketing-Ausgaben in Tausend $)
        - Y-Achse: CustomerFootfall (Anzahl der Kunden im Monat)
        - Farb-Codierung: StoreCategory (zeigt, ob der Effekt je nach Store-Typ unterschiedlich ist)
        - Trendlinie: Fügt eine lineare Regression (OLS) hinzu, um den generellen Trend zu verdeutlichen.

        Die lineare Regression funktioniert hier ähnlich wie im vorherigen Beispiel.
        """
        fig = px.scatter(
            df,
            x="MarketingSpend",
            y="CustomerFootfall",
            color="StoreCategory",
            trendline="ols",  # Trendlinie mittels linearer Regression (OLS)
            title="Marketing Spend vs Customer Footfall",
            labels={
                "MarketingSpend": "Marketing Spend (in Tausend $)",
                "CustomerFootfall": "Customer Footfall (Anzahl der Kunden im Monat)"
            },
            hover_data=["StoreID"]
        )
        return fig

    @staticmethod
    def create_scatter_promotions_footfall(df):
        """
        Erzeugt ein Streudiagramm, das den Zusammenhang zwischen der Anzahl der Promotion-Events
        (PromotionsCount) und der Anzahl der Kunden (CustomerFootfall) visualisiert. (JPG)

        - X-Achse: PromotionsCount (Anzahl der Promotion-Events)
        - Y-Achse: CustomerFootfall (Anzahl der Kunden)
        - Farb-Codierung: StoreCategory (zeigt branchenspezifische Unterschiede)
        - Trendlinie: Lineare Regression (OLS) zur Verdeutlichung einer möglichen Korrelation

        Die lineare Regression funktioniert hier ähnlich wie im vorherigen Beispiel.
        """
        fig = px.scatter(
            df,
            x="PromotionsCount",
            y="CustomerFootfall",
            color="StoreCategory",  # Unterscheidung der Datenpunkte nach StoreCategory
            trendline="ols",  # Fügt eine lineare Regressionslinie (OLS) hinzu
            title="Promotions vs Customer Footfall",
            labels={
                "PromotionsCount": "Promotions Count (Anzahl der Promotion-Events)",
                "CustomerFootfall": "Customer Footfall (Anzahl der Kunden)"
            },
            hover_data=["StoreID"]
        )
        return fig

    @staticmethod
    def create_bar_chart_promotions_vs_footfall(df):
        """
        Erzeugt ein Balkendiagramm, das die durchschnittliche Kundenfrequenz (CustomerFootfall)
        für verschiedene Promotionsanzahlen (PromotionsCount) anzeigt. (JPG)

        Vorgehensweise:

        1. Gruppierung:
           - Der DataFrame wird nach der Anzahl der Promotion-Events (PromotionsCount) gruppiert.
           - Für jede Gruppe wird der Durchschnitt der CustomerFootfall berechnet.

        2. Visualisierung:
           - Die X-Achse zeigt die Promotionsanzahl.
           - Die Y-Achse stellt die durchschnittliche Kundenfrequenz dar.
        """
        # Gruppiere nach PromotionsCount und berechne den Durchschnitt der CustomerFootfall
        df_grouped = df.groupby("PromotionsCount", as_index=False)["CustomerFootfall"].mean()

        # Optional: Sortiere die Ergebnisse nach PromotionsCount, damit die X-Achse korrekt geordnet ist
        df_grouped = df_grouped.sort_values("PromotionsCount")

        # Erstelle ein Balkendiagramm mit Plotly Express
        fig = px.bar(
            df_grouped,
            x="PromotionsCount",
            y="CustomerFootfall",
            title="Durchschnittliche Kundenfrequenz pro Promotionsanzahl",
            labels={
                "PromotionsCount": "Promotionsanzahl",
                "CustomerFootfall": "Durchschnittliche Kundenfrequenz"
            }
        )
        return fig

    @staticmethod
    def create_scatter_productvariety_vs_footfall(df):
        """
        Erzeugt ein Streudiagramm mit Trendlinie, das den Zusammenhang zwischen Produktvielfalt
        (ProductVariety) und Kundenbesuchen (CustomerFootfall) darstellt. (JPG)

        - X-Achse: ProductVariety (Produktvielfalt)
        - Y-Achse: CustomerFootfall (Anzahl der Kundenbesuche)
        - Farb-Codierung: StoreCategory
        - Trendlinie: Fügt eine lineare Regression (OLS) hinzu

        Die lineare Regression funktioniert wie in den obigen Beispielen.
        """
        fig = px.scatter(
            df,
            x="ProductVariety",
            y="CustomerFootfall",
            color="StoreCategory",
            trendline="ols",  # Fügt die lineare Regressionslinie hinzu
            title="Product Variety vs Customer Footfall",
            labels={
                "ProductVariety": "Product Variety (Produktvielfalt)",
                "CustomerFootfall": "Customer Footfall (Kundenbesuche)"
            },
            hover_data=["StoreID"]
        )
        return fig