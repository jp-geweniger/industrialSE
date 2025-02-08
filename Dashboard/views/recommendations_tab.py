from dash import dcc, html

class RecommendationsTab:

    @staticmethod
    def create_recommendations_section(df, selected_store):
        if df is None or df.empty:
            return html.P("Keine Daten verfügbar.")

        # Erstelle Dropdown-Optionen aus den Store-IDs
        store_options = [{"label": f"Store {store}", "value": store} for store in df["StoreID"].unique()]

        # Dropdown für Store-Auswahl (nur für diesen Tab)
        dropdown = dcc.Dropdown(
            id="store-dropdown",
            options=store_options,
            placeholder="Store auswählen...",
            value=selected_store if selected_store in df["StoreID"].values else None,
            clearable=False
        )

        # Falls kein Store ausgewählt wurde oder Store existiert nicht
        if selected_store is None or selected_store not in df["StoreID"].values:
            return html.Div([
                html.H2("Empfehlungen"),
                dropdown,
                html.P("Bitte einen gültigen Store auswählen.")
            ])

        # Daten des ausgewählten Stores abrufen
        store_data = df[df["StoreID"] == selected_store]

        # Falls keine Daten für den Store vorhanden sind (z.B. falls er gefiltert wurde)
        if store_data.empty:
            return html.Div([
                html.H2("Empfehlungen"),
                dropdown,
                html.P(f"❌ Fehler: Store {selected_store} existiert nicht in den Daten!"),
            ])

        # Filtere DataFrame, um den gewählten Store auszuschließen
        df_filtered = df[df["StoreID"] != selected_store]

        # Wähle nur numerische Spalten aus
        numeric_df = df_filtered.select_dtypes(include=["number"])

        # Berechne den Mittelwert nur für numerische Spalten
        avg_values = numeric_df.mean()

        # Generiere spezifische Empfehlungen
        recommendations = []

        # 🔥 Umsatzsteigerung
        if "MonthlySalesRevenue" in store_data.columns and "MonthlySalesRevenue" in avg_values:
            if store_data["MonthlySalesRevenue"].values[0] < avg_values["MonthlySalesRevenue"]:
                recommendations.append(html.P("📊 Erhöhe das Marketingbudget, um den Umsatz zu steigern."))

        # 🔥 Kundenfrequenz verbessern
        if "CustomerFootfall" in store_data.columns and "CustomerFootfall" in avg_values:
            if store_data["CustomerFootfall"].values[0] < avg_values["CustomerFootfall"]:
                recommendations.append(html.P("👥 Plane mehr Promotion-Events, um mehr Kunden anzulocken."))

        # 🔥 Werbeaktionen optimieren
        if "PromotionsCount" in store_data.columns and "PromotionsCount" in avg_values:
            if store_data["PromotionsCount"].values[0] < avg_values["PromotionsCount"]:
                recommendations.append(html.P("🎯 Nutze gezieltere Werbeaktionen zur Steigerung der Kundenfrequenz."))

        # 🔥 Mitarbeiterschulung verbessern
        if "EmployeeEfficiency" in store_data.columns and "EmployeeEfficiency" in avg_values:
            if store_data["EmployeeEfficiency"].values[0] < avg_values["EmployeeEfficiency"]:
                recommendations.append(html.P("📚 Optimiere die Mitarbeiterschulung, um die Effizienz zu erhöhen."))

        # Falls keine spezifischen Empfehlungen notwendig sind
        if not recommendations:
            recommendations.append(html.P("✅ Der Store ist in allen Bereichen überdurchschnittlich!"))

        return html.Div([
            html.H2("Empfehlungen"),
            dropdown,
            html.Div(recommendations)
        ])
