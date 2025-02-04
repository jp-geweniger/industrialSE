from dash import html

class RecommendationsTab:
    @staticmethod
    def create_recommendations_section():
        """Erzeugt Empfehlungssektion."""
        return html.Ul([
            html.Li("Increase marketing spend for locations with high footfall but low revenue."),
            html.Li("Focus promotional activities on top-performing categories."),
            html.Li("Optimize employee efficiency in underperforming stores.")
        ])