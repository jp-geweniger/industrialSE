import plotly.graph_objects as go
import plotly.express as px

class KeyInfluencersTab:
    @staticmethod
    def create_feature_importance_figure():
        """Erzeugt Platzhalter."""
        fig = go.Figure()
        fig.update_layout(title="Feature Importance (Placeholder)")
        return fig

    @staticmethod
    def create_correlation_heatmap(df):
        """Erzeugt Korrelations-Heatmap"""
        numeric_df = df.select_dtypes(include=["number"])
        correlation_matrix = numeric_df.corr()
        return px.imshow(correlation_matrix, text_auto=True, title="Correlation Heatmap")