import plotly.graph_objects as go
from dash import dcc, html


# Comparison function (DM - Davronbek Mavlonov)
class VergleichsfunktionTab:
    """Tab for comparing two stores or regions across multiple metrics. (DM)"""

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

        # Separate regions and stores
        unique_locations = df["StoreLocation"].dropna().unique()
        unique_stores = df[["StoreID", "StoreLocation", "StoreCategory"]].drop_duplicates()

        # Prepare dropdowns
        location_options = [{"label": f"Region: {loc}", "value": loc} for loc in unique_locations]
        store_options = [{"label": f"Store {row['StoreID']} ({row['StoreLocation']}, {row['StoreCategory']})",
                          "value": row['StoreID']}
                         for _, row in unique_stores.iterrows()]

        # Merge stores and regions into the dropdown
        dropdown_options = store_options + location_options

        # Metrics dropdown
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

        # Check if the selection is a StoreID (number) or a Region (string)
        first_is_store = isinstance(first, int) or str(first).isdigit()
        second_is_store = isinstance(second, int) or str(second).isdigit()

        if first_is_store:
            first_data = df[df["StoreID"] == int(first)]  # Filter by StoreID
        else:
            first_data = df[df["StoreLocation"] == first]  # Filter by StoreLocation

        if second_is_store:
            second_data = df[df["StoreID"] == int(second)]  # Filter by StoreID
        else:
            second_data = df[df["StoreLocation"] == second]  # Filter by StoreLocation

        if first_data.empty or second_data.empty:
            return html.Div("Error: No data available for one or both of the selected stores or regions.")

        # Ensure all metrics exist in the DataFrame
        available_metrics = [m for m in metrics if m in df.columns]

        if not available_metrics:
            return html.Div("Error: No valid metrics selected.")

        # Compute the mean for comparison (handling missing values)
        first_avg = first_data[available_metrics].mean(skipna=True)
        second_avg = second_data[available_metrics].mean(skipna=True)

        # Generate comparison results
        first_category = (
            first_data["StoreCategory"].iloc[
                0] if first_is_store and "StoreCategory" in first_data.columns else "Multiple Categories"
        )
        second_category = (
            second_data["StoreCategory"].iloc[
                0] if second_is_store and "StoreCategory" in second_data.columns else "Multiple Categories"
        )

        comparison_result = [
            html.Li(
                f"{metric}: {first_avg[metric]:.2f} vs. {second_avg[metric]:.2f} → "
                f"{'Higher in First' if first_avg[metric] > second_avg[metric] else 'Higher in Second'} "
                f"({first_category} vs. {second_category})"
            )
            for metric in available_metrics
        ]

        return html.Ul(comparison_result)

    # bar chart
    def create_comparison_bar_chart(self, df, first, second, metrics):
        """Creates a grouped bar chart for selected metrics."""

        # Check if selection is a StoreID or Region
        first_is_store = isinstance(first, int) or str(first).isdigit()
        second_is_store = isinstance(second, int) or str(second).isdigit()

        if first_is_store:
            first_data = df[df["StoreID"] == int(first)]
            first_category = first_data["StoreCategory"].iloc[0] if "StoreCategory" in first_data.columns else "Unknown"
            first_label = f"Store {int(first)} ({first_data['StoreLocation'].iloc[0]}, {first_category})"
        else:
            first_data = df[df["StoreLocation"] == first]
            first_label = f"Region: {first}"

        if second_is_store:
            second_data = df[df["StoreID"] == int(second)]
            second_category = second_data["StoreCategory"].iloc[
                0] if "StoreCategory" in second_data.columns else "Unknown"
            second_label = f"Store {int(second)} ({second_data['StoreLocation'].iloc[0]}, {second_category})"
        else:
            second_data = df[df["StoreLocation"] == second]
            second_label = f"Region: {second}"

        if first_data.empty or second_data.empty:
            return go.Figure(layout={"title": "No data available"})

        # Ensure all selected metrics exist in the DataFrame
        available_metrics = [m for m in metrics if m in df.columns]

        if not available_metrics:
            return go.Figure(layout={"title": "No valid metrics selected"})

        first_avg = first_data[available_metrics].mean(skipna=True)
        second_avg = second_data[available_metrics].mean(skipna=True)

        # Create bar chart
        fig = go.Figure()
        for metric in available_metrics:
            fig.add_trace(go.Bar(x=[first_label, second_label], y=[first_avg[metric], second_avg[metric]], name=metric))

        fig.update_layout(
            title="Metric Comparison",
            barmode="group",
            xaxis_title="Store/Region",
            yaxis_title="Metric Value"
        )
        return fig

    # pie chart
    def create_comparison_pie_chart(self, df, first, second):
        """Creates a pie chart comparing total revenue of the two selections."""

        # Check if selection is a StoreID or Region
        first_is_store = isinstance(first, int) or str(first).isdigit()
        second_is_store = isinstance(second, int) or str(second).isdigit()

        if first_is_store:
            first_data = df[df["StoreID"] == int(first)]
        else:
            first_data = df[df["StoreLocation"] == first]

        if second_is_store:
            second_data = df[df["StoreID"] == int(second)]
        else:
            second_data = df[df["StoreLocation"] == second]

        if first_data.empty or second_data.empty:
            return go.Figure(layout={"title": "No data available"})

        # Ensure "MonthlySalesRevenue" exists
        if "MonthlySalesRevenue" not in df.columns:
            return go.Figure(layout={"title": "Revenue data not available"})

        revenue_first = first_data["MonthlySalesRevenue"].sum()
        revenue_second = second_data["MonthlySalesRevenue"].sum()

        # Generate labels including category
        if first_is_store:
            first_category = first_data["StoreCategory"].iloc[0] if "StoreCategory" in first_data.columns else "Unknown"
            first_label = f"Store {int(first)} ({first_data['StoreLocation'].iloc[0]}, {first_category})"
        else:
            first_label = f"Region: {first}"

        if second_is_store:
            second_category = second_data["StoreCategory"].iloc[
                0] if "StoreCategory" in second_data.columns else "Unknown"
            second_label = f"Store {int(second)} ({second_data['StoreLocation'].iloc[0]}, {second_category})"
        else:
            second_label = f"Region: {second}"

        # Jetzt erst die Umsatzdaten berechnen
        revenue_first, revenue_second = first_data["MonthlySalesRevenue"].sum(), second_data[
            "MonthlySalesRevenue"].sum()

        labels = [first_label, second_label]
        fig = go.Figure(data=[go.Pie(labels=labels, values=[revenue_first, revenue_second], hole=0.4)])
        fig.update_layout(title="Revenue Distribution Between Selected Stores/Regions")
        return fig
