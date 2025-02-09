import plotly.express as px

class PerformanceInsightsTab:


    @staticmethod
    def create_scatter_marketing_revenue(df):
        """
        Erzeugt ein verbessertes Streudiagramm für Marketingausgaben vs. Umsatz mit festen Farben für Kategorien.
        """

        # 🔹 Einheitliche Farben für jede StoreCategory
        category_colors = {
            "Electronic": "#1f77b4",  # Blau
            "Grocery": "#2ca02c",     # Grün
            "Clothing": "#d62728"     # Rot
        }

        fig = px.scatter(
            df,
            x="MarketingSpend",
            y="MonthlySalesRevenue",
            color="StoreCategory",  # Farb-Codierung nach StoreCategory
            size="CustomerFootfall",  # Größe der Punkte basierend auf Kundenfrequenz
            trendline="ols",
            log_x=True,  # Log-Skalierung für eine bessere Darstellung großer Werte
            title="Marketing Spend vs Revenue",
            labels={
                "MarketingSpend": "Marketing Spend (in Tausend $)",
                "MonthlySalesRevenue": "Revenue (Umsatz)"
            },
            hover_data=["StoreID", "CustomerFootfall", "PromotionsCount"],  # Zusätzliche Infos beim Hover
            color_discrete_map=category_colors  # 🔹 Einheitliche Farben für jede Kategorie
        )

        fig.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))  # Bessere Sichtbarkeit

        return fig

    @staticmethod
    def create_box_plot_category(df):
        """Erzeugt ein verbessertes Boxplot-Diagramm für den Umsatz nach Geschäftskategorie mit festen Farben."""

        # 🔹 Einheitliche Farben für jede StoreCategory
        category_colors = {
            "Electronic": "#1f77b4",  # Blau
            "Grocery": "#2ca02c",  # Grün
            "Clothing": "#d62728"  # Rot
        }

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
            color_discrete_map=category_colors  # 🔹 Einheitliche Farben für jede Kategorie
        )

        fig.update_layout(boxmode="overlay")  # Mehrere Boxplots überlagert anzeigen

        return fig