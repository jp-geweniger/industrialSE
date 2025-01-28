import dash
from dash import dcc, html, Input, Output
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class SQLiteConnector:
    def __init__(self, db_path):
        self.db_path = db_path

    def fetch_data(self, query):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

class Dashboard:
    def __init__(self, db_path):
        self.db_connector = SQLiteConnector(db_path)
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1("Store Performance Dashboard"),

            # Overview Section
            html.H2("Overview"),
            html.Div(id="overview-section"),

            # Key Influencers Section
            html.H2("Key Influencers"),
            dcc.Graph(id="feature-importance"),
            dcc.Graph(id="correlation-heatmap"),

            # Performance Insights Section
            html.H2("Performance Insights"),
            dcc.Graph(id="scatter-footfall-revenue"),
            dcc.Graph(id="scatter-marketing-revenue"),
            dcc.Graph(id="scatter-competitor-revenue"),
            dcc.Graph(id="box-plot-category"),

            # Regional Comparison Section
            html.H2("Regional Comparison"),
            dcc.Graph(id="map-visualization"),
            dcc.Graph(id="grouped-bar-chart"),

            # Store Operations Section
            html.H2("Store Operations"),
            dcc.Graph(id="bubble-chart-operations"),
            dcc.Graph(id="histogram-efficiency"),

            # Recommendations Section
            html.H2("Recommendations"),
            html.Div(id="recommendations-section")
        ])

    def setup_callbacks(self):
        @self.app.callback(
            [Output("overview-section", "children"),
             Output("feature-importance", "figure"),
             Output("correlation-heatmap", "figure"),
             Output("scatter-footfall-revenue", "figure"),
             Output("scatter-marketing-revenue", "figure"),
             Output("scatter-competitor-revenue", "figure"),
             Output("box-plot-category", "figure"),
             Output("map-visualization", "figure"),
             Output("grouped-bar-chart", "figure"),
             Output("bubble-chart-operations", "figure"),
             Output("histogram-efficiency", "figure"),
             Output("recommendations-section", "children")],
            Input("feature-importance", "id")  # Dummy input to trigger callback
        )
        def update_dashboard(_):
            # Fetch all data
            query = "SELECT * FROM StoreData"
            df = self.db_connector.fetch_data(query)

            # Overview Section
            total_revenue = df["MonthlySalesRevenue"].sum()
            avg_footfall = df["CustomerFootfall"].mean()
            total_marketing_spend = df["MarketingSpend"].sum()
            total_promotions = df["PromotionsCount"].sum()

            overview = html.Ul([
                html.Li(f"Total Monthly Sales Revenue: ${total_revenue:,.2f}"),
                html.Li(f"Average Customer Footfall: {avg_footfall:,.0f}"),
                html.Li(f"Total Marketing Spend: ${total_marketing_spend:,.2f}"),
                html.Li(f"Total Promotions: {total_promotions}")
            ])

            # Key Influencers Section
            numeric_df = df.select_dtypes(include=["number"])
            correlation_matrix = numeric_df.corr()
            heatmap_fig = px.imshow(correlation_matrix, text_auto=True, title="Correlation Heatmap")

            # Placeholder for feature importance (requires ML model implementation)
            feature_importance_fig = go.Figure()
            feature_importance_fig.update_layout(title="Feature Importance (Placeholder)")

            # Performance Insights Section
            scatter_footfall_fig = px.scatter(df, x="CustomerFootfall", y="MonthlySalesRevenue",
                                              title="Customer Footfall vs Revenue",
                                              labels={"CustomerFootfall": "Customer Footfall", "MonthlySalesRevenue": "Revenue"},
                                              hover_data=["StoreID"])

            scatter_marketing_fig = px.scatter(df, x="MarketingSpend", y="MonthlySalesRevenue",
                                               title="Marketing Spend vs Revenue",
                                               labels={"MarketingSpend": "Marketing Spend", "MonthlySalesRevenue": "Revenue"},
                                               hover_data=["StoreID"])

            scatter_competitor_fig = px.scatter(df, x="CompetitorDistance", y="MonthlySalesRevenue",
                                                title="Competitor Distance vs Revenue",
                                                labels={"CompetitorDistance": "Competitor Distance", "MonthlySalesRevenue": "Revenue"},
                                                hover_data=["StoreID"])

            box_plot_category_fig = px.box(df, x="StoreCategory", y="MonthlySalesRevenue",
                                           title="Revenue by Store Category",
                                           labels={"StoreCategory": "Store Category", "MonthlySalesRevenue": "Revenue"},
                                           hover_data=["StoreID"])

            # Regional Comparison Section
            map_fig = px.scatter_geo(df, locations="StoreLocation",
                                      color="MonthlySalesRevenue",
                                      title="Revenue by Location",
                                      labels={"MonthlySalesRevenue": "Revenue", "StoreLocation": "Location"},
                                      hover_data=["StoreID"])

            grouped_bar_fig = px.bar(df, x="StoreLocation", y="MonthlySalesRevenue", color="StoreCategory",
                                     title="Revenue by Location and Category",
                                     labels={"MonthlySalesRevenue": "Revenue", "StoreLocation": "Location"},
                                     hover_data=["StoreID"])

            # Store Operations Section
            bubble_chart_fig = px.scatter(df, x="StoreSize", y="MonthlySalesRevenue",
                                           size="EmployeeEfficiency", color="StoreCategory",
                                           title="Store Size, Efficiency, and Revenue",
                                           labels={"StoreSize": "Store Size", "MonthlySalesRevenue": "Revenue", "EmployeeEfficiency": "Efficiency"},
                                           hover_data=["StoreID"])

            histogram_fig = px.histogram(df, x="EmployeeEfficiency",
                                         title="Employee Efficiency Distribution",
                                         labels={"EmployeeEfficiency": "Efficiency"},
                                         hover_data=["StoreID"])

            # Recommendations Section
            recommendations = html.Ul([
                html.Li("Increase marketing spend for locations with high footfall but low revenue."),
                html.Li("Focus promotional activities on top-performing categories."),
                html.Li("Optimize employee efficiency in underperforming stores.")
            ])

            return (overview, feature_importance_fig, heatmap_fig, scatter_footfall_fig,
                    scatter_marketing_fig, scatter_competitor_fig, box_plot_category_fig,
                    map_fig, grouped_bar_fig, bubble_chart_fig, histogram_fig, recommendations)

    def run(self):
        self.app.run_server(debug=True)

if __name__ == "__main__":
    dashboard = Dashboard("Database.db")
    dashboard.run()
