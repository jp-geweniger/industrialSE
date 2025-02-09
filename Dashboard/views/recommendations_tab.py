from dash import dcc, html, Input, Output, dash

class RecommendationsTab:

    @staticmethod
    def create_recommendations_section(df, selected_store=None):
        """Erstellt das Layout für den Recommendations-Tab. (JE und JPG)"""
        if df is None or df.empty:
            return html.P("🚫 Keine Daten verfügbar.")

        # Store-Optionen für Dropdown erstellen
        store_options = [{"label": f"Store {store}", "value": store} for store in df["StoreID"].unique()]

        # Falls kein Store ausgewählt wurde, wähle den ersten Store als Standard
        if selected_store is None:
            selected_store = df["StoreID"].iloc[0]

        top_general_heading = html.H2(
            "Top General Recommendations to Increase Revenue",
            style={"textAlign": "center", "marginBottom": "30px"}
        )

        # Sektion: Top Dos und Top Don'ts (JPG)
        dos_donts_section = html.Div([
            html.Div([
                html.H3("✓ Top Dos", style={"textAlign": "center", "color": "#28a745", "marginBottom": "15px"}),
                html.Ul([
                    html.Li("✔️ Optimize product variety (see Store Operations)"),
                    html.Li("✔️ Re-Evaluate your marketing and promotion strategy"),
                    html.Li("✔️ Increase customer footfall"),
                    html.Li("✔️ Increase employee efficiency"),
                    html.Li("✔️ Increase store-size when possible"),
                ], style={"fontSize": "16px", "lineHeight": "1.5"})
            ], style={
                "width": "48%",
                "padding": "10px",
                "border": "2px solid #28a745",
                "borderRadius": "5px",
                "backgroundColor": "#e9f7ef",
                "marginBottom": "30px"
            }),
            html.Div([
                html.H3("✗ Top Don'ts", style={"textAlign": "center", "color": "#dc3545", "marginBottom": "15px"}),
                html.Ul([
                    html.Li("❌ Spend too much on marketing and promotions (unless you know for sure they are useful)"),
                    html.Li("❌ Fear a short distance to a competitor"),
                    html.Li("❌ Give up too early"),
                ], style={"fontSize": "16px", "lineHeight": "1.5"})
            ], style={
                "width": "48%",
                "padding": "10px",
                "border": "2px solid #dc3545",
                "borderRadius": "5px",
                "backgroundColor": "#f8d7da",
                "marginBottom": "30px"
            })
        ], style={
            "display": "flex",
            "justifyContent": "space-between",
            "marginBottom": "30px"
        })

        # Überschrift für den Bereich Individual Recommendations (über dem Dropdown)
        individual_heading = html.H3(
            "Individual Recommendations",
            style={"textAlign": "center", "fontSize": "24px", "marginBottom": "20px"}
        )

        # Layout zusammenstellen: Gesamtüberschrift, Dos/Don'ts, Individual Recommendations, Dropdown und Empfehlungen
        return html.Div([
            top_general_heading,
            dos_donts_section,
            individual_heading,
            dcc.Dropdown(
                id="store-dropdown",
                options=store_options,
                value=selected_store,  # Standardmäßig erster Store
                clearable=False,
                style={"marginBottom": "30px"}
            ),
            html.Div(id="recommendations-content", children=RecommendationsTab.generate_recommendations(df, selected_store))
        ])

    @staticmethod
    def register_callbacks(app, db_connector):
        """Registriert den Callback für das Dropdown-Menü. (JE)"""

        @app.callback(
            Output("recommendations-content", "children"),
            Input("store-dropdown", "value")
        )
        def update_recommendations(selected_store):
            """Aktualisiert die Empfehlungen basierend auf dem gewählten Store. (JE)"""
            if not selected_store:
                raise dash.exceptions.PreventUpdate  # Kein Update, wenn kein Store ausgewählt wurde

            df = db_connector.fetch_data("SELECT * FROM StoreData")
            if df.empty:
                return html.P("🚫 Keine Daten verfügbar.")

            return RecommendationsTab.generate_recommendations(df, selected_store)

    @staticmethod
    def generate_recommendations(df, selected_store):
        """Erstellt die Empfehlungen basierend auf dem ausgewählten Store. (JE)"""
        if df is None or df.empty:
            return html.P("🚫 Keine Daten verfügbar.")

        # Prüfe, ob der Store existiert
        if selected_store not in df["StoreID"].values:
            return html.P("🚫 Der ausgewählte Store existiert nicht in den Daten.")

        # Daten des ausgewählten Stores abrufen
        store_data = df.loc[df["StoreID"] == selected_store]

        # Filtere DataFrame, um den gewählten Store auszuschließen
        df_filtered = df.loc[df["StoreID"] != selected_store]

        # Berechne den Mittelwert aller numerischen Spalten
        avg_values = df_filtered.mean(numeric_only=True).dropna()

        # Generiere spezifische Empfehlungen
        recommendations = []

        def add_recommendation(column, threshold, message):
            if column in store_data.columns and column in avg_values:
                if store_data.iloc[0][column] < avg_values[column] * threshold:
                    recommendations.append(html.P(message))

        # 🔥 Umsatzsteigerung
        add_recommendation("MonthlySalesRevenue", 1, "📊 Erhöhe das Marketingbudget, um den Umsatz zu steigern.")

        # 🔥 Kundenfrequenz verbessern
        add_recommendation("CustomerFootfall", 1, "👥 Plane mehr Promotion-Events, um mehr Kunden anzulocken.")

        # 🔥 Werbeaktionen optimieren
        add_recommendation("PromotionsCount", 1, "🎯 Nutze gezieltere Werbeaktionen zur Steigerung der Kundenfrequenz.")

        # 🔥 Mitarbeiterschulung verbessern
        add_recommendation("EmployeeEfficiency", 1, "📚 Optimiere die Mitarbeiterschulung, um die Effizienz zu erhöhen.")

        # Falls keine spezifischen Empfehlungen notwendig sind
        if not recommendations:
            recommendations.append(html.P("✅ Der Store ist in allen Bereichen überdurchschnittlich!"))

        return html.Div(recommendations)