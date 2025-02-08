import plotly.graph_objects as go
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from scripts.sqlite_connector import SQLiteConnector


class VergleichsfunktionTab:
    """Tab for comparing two stores or regions across multiple metrics."""

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def fetch_store_data(self):
        """Fetch store data from the database."""
        query = "SELECT * FROM StoreData"
        df = self.db_connector.fetch_data(query)
        return df

    def create_comparison_section(self):
        """Creates the layout for store/region comparison."""
        df = self.fetch_store_data()
        if df.empty:
            return html.Div("Error: No data available in StoreData.")

        unique_locations = df["StoreLocation"].dropna().unique()
        dropdown_options = [{"label": loc, "value": loc} for loc in unique_locations]
        metrics = [col for col in df.columns if col not in ["StoreID", "StoreLocation", "StoreCategory"]]
        metric_options = [{"label": metric, "value": metric} for metric in metrics]

        return html.Div([
            html.H3("Compare Two Stores or Regions"),
            html.Label("Select First Store or Region:"),
            dcc.Dropdown(id="compare-first", options=dropdown_options, placeholder="Select first", searchable=True),
            html.Label("Select Second Store or Region:"),
            dcc.Dropdown(id="compare-second", options=dropdown_options, placeholder="Select second", searchable=True),
            html.Label("Select Metrics for Comparison:"),
            dcc.Dropdown(id="compare-metrics", options=metric_options, placeholder="Select metrics", multi=True),
            html.Button("Compare", id="compare-button", n_clicks=0),
            html.Div(id="comparison-output"),
            dcc.Graph(id="comparison-bar-chart"),
            dcc.Graph(id="comparison-pie-chart")
        ])

    def generate_comparison_metrics(self, df, first, second, metrics):
        """Generates comparison results between two selected stores or regions."""
        first_data = df[df["StoreLocation"] == first]
        second_data = df[df["StoreLocation"] == second]

        if first_data.empty or second_data.empty:
            return html.Div("Error: No data available for one or both of the selected stores or regions.")

        first_avg = first_data[metrics].mean()
        second_avg = second_data[metrics].mean()

        comparison_result = [
            html.Li(f"{metric}: Higher in {'first' if first_avg[metric] > second_avg[metric] else 'second'}")
            for metric in metrics
        ]
        return html.Ul(comparison_result)

    def create_comparison_bar_chart(self, df, first, second, metrics):
        """Creates a grouped bar chart for selected metrics."""
        first_data = df[df["StoreLocation"] == first]
        second_data = df[df["StoreLocation"] == second]

        if first_data.empty or second_data.empty:
            return go.Figure(layout={"title": "No data available"})

        first_avg = first_data[metrics].mean()
        second_avg = second_data[metrics].mean()

        fig = go.Figure()
        for metric in metrics:
            fig.add_trace(go.Bar(x=[first, second], y=[first_avg[metric], second_avg[metric]], name=metric))

        fig.update_layout(title="Metric Comparison", barmode="group")
        return fig

    def create_comparison_pie_chart(self, df, first, second):
        """Creates a pie chart comparing total revenue of the two selections."""
        first_data = df[df["StoreLocation"] == first]
        second_data = df[df["StoreLocation"] == second]

        if first_data.empty or second_data.empty:
            return go.Figure(layout={"title": "No data available"})

        revenue_first = first_data["MonthlySalesRevenue"].sum()
        revenue_second = second_data["MonthlySalesRevenue"].sum()

        fig = go.Figure(data=[go.Pie(labels=[first, second], values=[revenue_first, revenue_second], hole=0.4)])
        fig.update_layout(title="Revenue Distribution Between Selected Stores/Regions")
        return fig
