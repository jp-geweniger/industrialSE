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

        # Generiere Empfehlungen basierend auf den Durchschnittswerten
        recommendations = []
        for col in avg_values.index:
            if col in store_data.columns:
                store_value = store_data[col].values[0]  # Wert des ausgewählten Stores
                avg_value = avg_values[col]  # Durchschnittswert aller anderen Stores

                if store_value < avg_value:
                    recommendations.append(html.P(f"🔻 {col}: Wert {store_value:.2f} liegt unter dem Durchschnitt ({avg_value:.2f}). Verbesserungspotenzial!"))
                else:
                    recommendations.append(html.P(f"✅ {col}: Wert {store_value:.2f} ist überdurchschnittlich."))

        # Falls keine Empfehlungen notwendig sind
        if not recommendations:
            recommendations.append(html.P("✅ Der Store ist in allen Bereichen überdurchschnittlich!"))

        return html.Div([
            html.H2("Empfehlungen"),
            dropdown,
            html.Div(recommendations)
        ])
