import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
# Importiert die Klasse LinearRegression, mit der ein lineares Regressionsmodell erstellt wird.
# Dieses Modell ermittelt den Zusammenhang zwischen den unabhängigen Variablen (Features)
# und der abhängigen Variable (Target) – zum Beispiel, um den Einfluss von MarketingSpend,
# CustomerFootfall und ProductVariety auf den Umsatz zu analysieren.

from sklearn.preprocessing import StandardScaler
# Importiert den StandardScaler, der verwendet wird, um die Merkmalswerte zu standardisieren.
# Die Standardisierung transformiert die Daten so, dass sie einen Mittelwert von 0 und eine
# Standardabweichung von 1 haben. Dies ist wichtig, damit die Koeffizienten des Regressionsmodells
# vergleichbar sind, insbesondere wenn die Features unterschiedliche Skalen haben.

class KeyInfluencersTab:

    @staticmethod
    def create_feature_importance_figure(df):
        """
        Berechnet die Feature Importance – also den Einfluss verschiedener Faktoren auf den Umsatz –
        mittels eines linearen Regressionsmodells. Es werden die Features 'MarketingSpend', 'CustomerFootfall'
        und 'ProductVariety' herangezogen. Die Features werden standardisiert, um vergleichbare Koeffizienten
        zu erhalten. Anschließend wird ein lineares Regressionsmodell trainiert und die absoluten Werte der
        Koeffizienten werden normalisiert, sodass die Summe 100% ergibt. (JPG)

        Vorgehensweise:
        1. Auswahl der relevanten Features (MarketingSpend, CustomerFootfall, ProductVariety)
           und des Zielwerts (MonthlySalesRevenue).
        2. Entfernen von Zeilen mit fehlenden Werten in diesen Spalten.
        3. Standardisierung der Features (z. B. mit StandardScaler), damit die Koeffizienten nicht
           durch unterschiedliche Messskalen verzerrt werden.
        4. Training eines linearen Regressionsmodells (z. B. mit LinearRegression).
        5. Berechnung der absoluten Koeffizientenwerte und Normalisierung dieser Werte auf 100%.
        6. Darstellung der Ergebnisse in einem Balkendiagramm.

        Hinweis: Diese Methode verwendet die Bibliotheken scikit-learn (sklearn) und plotly.
        """

        # Definiert die unabhängigen Variablen und das Ziel
        features = ["MarketingSpend", "CustomerFootfall", "ProductVariety", "StoreSize", "StoreAge", "EmployeeEfficiency", "CompetitorDistance", "PromotionsCount", "EconomicIndicator"]
        target = "MonthlySalesRevenue"

        # Entfernt Zeilen mit fehlenden Werten in den relevanten Spalten
        df_model = df.dropna(subset=features + [target])

        # Standardisiert die Features, um vergleichbare Koeffizienten zu erhalten
        scaler = StandardScaler()
        x = scaler.fit_transform(df_model[features])
        y = df_model[target].values

        # Trainiert das lineare Regressionsmodell
        model = LinearRegression()
        model.fit(x, y)

        # Extrahiert die Koeffizienten und berechnet deren absolute Werte
        coefs = model.coef_
        importances = np.abs(coefs)

        # Normalisiert die Importances, sodass ihre Summe 100% ergibt
        total = importances.sum()
        percentages = 100 * importances / total if total > 0 else importances

        # Erstellt einen DataFrame für die Visualisierung
        data = {
            "Feature": features,
            "Influence": percentages
        }
        df_importance = pd.DataFrame(data)

        # Erstellt das Balkendiagramm
        fig = px.bar(
            df_importance,
            x="Feature",
            y="Influence",
            title="Feature Importance – Einflussfaktoren auf den Umsatz",
            labels={"Feature": "Faktor", "Influence": "Einfluss (%)"},
            text="Influence"
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        return fig

    @staticmethod
    def create_correlation_heatmap(df):
        """Erzeugt eine optimierte Korrelations-Heatmap. (JE)"""
        numeric_df = df.select_dtypes(include=["number"])
        correlation_matrix = numeric_df.corr()

        fig = px.imshow(
            correlation_matrix,
            text_auto=".2f",
            title="Correlation Heatmap",
            color_continuous_scale=px.colors.diverging.RdBu_r,  # Besserer Kontrast
        )

        fig.update_layout(
            height=800,  # Größer gemacht
            width=1000,  # Breiter gemacht
            coloraxis_colorbar=dict(title="Korrelationswert"),
        )

        return fig

    @staticmethod
    def create_employee_efficiency_importance_figure(df):
        """
        Berechnet die Feature Importance – also den Einfluss verschiedener Faktoren auf die EmployeeEfficiency –

        Funktionsweise wie im oberen Beispiel (JPG)
        """
        # Definiere die unabhängigen Variablen (Features) und das Ziel (Target)
        features = ["CustomerFootfall", "ProductVariety", "StoreSize", "StoreAge"]
        target = "EmployeeEfficiency"

        # Entferne Zeilen mit fehlenden Werten in den relevanten Spalten
        df_model = df.dropna(subset=features + [target])

        # Standardisiere die Features, damit die Koeffizienten vergleichbar sind
        scaler = StandardScaler()
        X = scaler.fit_transform(df_model[features])
        y = df_model[target].values

        # Trainiere das lineare Regressionsmodell
        model = LinearRegression()
        model.fit(X, y)

        # Extrahiere die Koeffizienten und berechne deren absolute Werte
        coefs = model.coef_
        importances = np.abs(coefs)

        # Normalisiere die Importances, sodass ihre Summe 100% ergibt
        total = importances.sum()
        percentages = 100 * importances / total if total > 0 else importances

        # Erstelle einen DataFrame für die Visualisierung
        data = {
            "Feature": features,
            "Influence": percentages
        }
        df_importance = pd.DataFrame(data)

        # Erstelle das Balkendiagramm (Bar Chart) mit plotly.express
        fig = px.bar(
            df_importance,
            x="Feature",
            y="Influence",
            title="Feature Importance – Einflussfaktoren auf die Employee Efficiency",
            labels={"Feature": "Faktor", "Influence": "Einfluss (%)"},
            text="Influence"
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        return fig