import dash  # Framework zum Erstellen von Webanwendungen
from dash import dcc, html, Input, Output, State  # Komponenten und Rückrufe für Dash-Anwendungen
import plotly.graph_objects as go
from views.vergleichsfunktion_tab import VergleichsfunktionTab
from scripts.sqlite_connector import SQLiteConnector
from views.overview_tab import OverviewTab
from views.key_influencers_tab import KeyInfluencersTab
from views.performance_insights_tab import PerformanceInsightsTab
from views.recommendations_tab import RecommendationsTab
from views.regional_comparison_tab import RegionalComparisonTab
from views.store_operations_tab import StoreOperationsTab
from views.customer_insights_tab import CustomerInsightsTab


class Dashboard:
    def __init__(self, db_path):
        self.db_connector = SQLiteConnector(db_path)
        self.vergleichsfunktion_tab = VergleichsfunktionTab(self.db_connector)
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        """ Setup Aufbau des Dashboards mit einer einklappbaren Navbar und separaten Views/Tabs. (JPG) """
        self.app.layout = html.Div([
            dcc.Location(id="url", refresh=False),

            # Laden von Font Awesome (für Icons)
            html.Link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ),

            # Runder Toggle Navbar Button
            html.Button(
                html.I(className="fas fa-bars", style={"color": "#007bff"}),  # Blaues toggle icon
                id="toggle-navbar",
                n_clicks=0,
                style={
                    "position": "fixed",
                    "top": "10px",
                    "left": "10px",
                    "zIndex": "1000",
                    "borderRadius": "50%",
                    "width": "50px",
                    "height": "50px",
                    "fontSize": "20px",
                    "backgroundColor": "#e0e0e0",  # Helleres grau
                    "border": "none",
                    "cursor": "pointer",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "boxShadow": "2px 2px 5px rgba(0, 0, 0, 0.2)"
                }
            ),
            # Sidebar mit den Navigationsbuttons (JPG)
            html.Div([
                html.Button([
                    html.Span(html.I(className="fas fa-home", style={"color": "#ff5733"}), style={"width": "30px"}),
                    html.Span("Homepage", style={"flex": "1", "textAlign": "left"})
                ], id="btn-overview", n_clicks=0, style={"width": "100%"}),

                html.Button([
                    html.Span(html.I(className="fas fa-key", style={"color": "#28a745"}), style={"width": "30px"}),
                    html.Span("Key Influencers", style={"flex": "1", "textAlign": "left"})
                ], id="btn-key-influencers", n_clicks=0, style={"width": "100%"}),

                html.Button([
                    html.Span(html.I(className="fas fa-balance-scale", style={"color": "#6f42c1"}),
                              style={"width": "30px"}),
                    html.Span("Vergleichsfunktion", style={"flex": "1", "textAlign": "left"})
                ], id="btn-vergleichsfunktion", n_clicks=0, style={"width": "100%"}),

                html.Button([
                    html.Span(html.I(className="fas fa-tachometer-alt", style={"color": "#007bff"}),
                              style={"width": "30px"}),
                    html.Span("Performance Insights", style={"flex": "1", "textAlign": "left"})
                ], id="btn-performance-insights", n_clicks=0, style={"width": "100%"}),

                html.Button([
                    html.Span(html.I(className="fas fa-user", style={"color": "#ffc107"}), style={"width": "30px"}),
                    html.Span("Customer Insights", style={"flex": "1", "textAlign": "left"})
                ], id="btn-customer-insights", n_clicks=0, style={"width": "100%"}),

                html.Button([
                    html.Span(html.I(className="fas fa-map-marker-alt", style={"color": "#dc3545"}),
                              style={"width": "30px"}),
                    html.Span("Regional Comparison", style={"flex": "1", "textAlign": "left"})
                ], id="btn-regional-comparison", n_clicks=0, style={"width": "100%"}),

                html.Button([
                    html.Span(html.I(className="fas fa-store", style={"color": "#6610f2"}), style={"width": "30px"}),
                    html.Span("Store Operations", style={"flex": "1", "textAlign": "left"})
                ], id="btn-store-operations", n_clicks=0, style={"width": "100%"}),

                html.Button([
                    html.Span(html.I(className="fas fa-lightbulb", style={"color": "#17a2b8"}),
                              style={"width": "30px"}),
                    html.Span("Recommendations", style={"flex": "1", "textAlign": "left"})
                ], id="btn-recommendations", n_clicks=0, style={"width": "100%"})
            ], id="sidebar", style={
                "width": "200px",
                "background-color": "#f8f9fa",
                "position": "fixed",
                "height": "100%",
                "overflow": "auto",
                "padding": "10px",
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center"
            }),
            # Konfiguration des Inhalts der Tabs/Views
            html.Div([
                html.Div([
                    html.H1("Store Performance Dashboard"),
                    html.H2("Overview"),
                    html.Div(id="overview-section")
                ], id="page-overview", style={"display": "none"}),

                html.Div([
                    html.H2("Key Influencers"),
                    dcc.Graph(id="feature-importance"),
                    dcc.Graph(id="correlation-heatmap")
                ], id="page-key-influencers", style={"display": "none"}),

                html.Div(self.vergleichsfunktion_tab.create_comparison_section(), id="page-vergleichsfunktion",
                         style={"display": "none"}),

                html.Div([
                    html.H2("Performance Insights"),
                    dcc.Graph(id="scatter-marketing-revenue"),
                    dcc.Graph(id="box-plot-category")
                ], id="page-performance-insights", style={"display": "none"}),

                html.Div([
                    html.H2("Customer Insights"),
                    dcc.Graph(id="barchart_category_footfall"),
                    dcc.Graph(id="scatter-footfall-revenue"),
                    dcc.Graph(id="scatter-productvariety-footfall"),
                    dcc.Graph(id="scatter-marketing-footfall"),
                    dcc.Graph(id="scatter-promotions-footfall"),
                    dcc.Graph(id="barchart-promotions-footfall"),
                ], id="page-customer-insights", style={"display": "none"}),

                html.Div([
                    html.H2("Regional Comparison"),
                    dcc.Graph(id="map-visualization"),
                    dcc.Graph(id="grouped-bar-chart"),
                    dcc.Graph(id="scatter-competitor-revenue"),
                    dcc.Graph(id="grouped-bar-chart-footfall"),
                ], id="page-regional-comparison", style={"display": "none"}),

                html.Div([
                    html.H2("Store Operations"),
                    dcc.Graph(id="scatter-productvariety-revenue"),
                    dcc.Graph(id="scatter-productvariety-efficiency"),
                    dcc.Graph(id="bubble-chart-operations"),
                    dcc.Graph(id="histogram-efficiency"),
                ], id="page-store-operations", style={"display": "none"}),

                html.Div([
                    html.H2("Recommendations"),
                    html.Div(id="recommendations-section")
                ], id="page-recommendations", style={"display": "none"}),
            ], id="page-content", style={"margin-left": "220px", "padding": "20px"})
        ])

    def setup_callbacks(self):
        """Setup der callbacks fürs Dashboard."""
        @self.app.callback(
            [Output("overview-section", "children"),
             Output("feature-importance", "figure"),
             Output("correlation-heatmap", "figure"),
             Output("barchart_category_footfall", "figure"),
             Output("scatter-footfall-revenue", "figure"),
             Output("scatter-productvariety-footfall", "figure"),
             Output("scatter-marketing-footfall", "figure"),
             Output("scatter-promotions-footfall", "figure"),
             Output("barchart-promotions-footfall", "figure"),
             Output("scatter-marketing-revenue", "figure"),
             Output("scatter-competitor-revenue", "figure"),
             Output("grouped-bar-chart-footfall", "figure"),
             Output("box-plot-category", "figure"),
             Output("map-visualization", "figure"),
             Output("grouped-bar-chart", "figure"),
             Output("scatter-productvariety-revenue", "figure"),
             Output("scatter-productvariety-efficiency", "figure"),
             Output("bubble-chart-operations", "figure"),
             Output("histogram-efficiency", "figure"),
             Output("recommendations-section", "children")],
            Input("feature-importance", "id")  # Dummy trigger
        )

        def update_dashboard(_):
            """Erzeugt das Dashboard im Gesamten."""
            df = self.db_connector.fetch_data("SELECT * FROM StoreData")

            # Funktionen/Diagramme des Overview-Tabs
            overview = OverviewTab.create_overview_section(df)

            # Funktionen/Diagramme des KeyInfluencers-Tabs
            feature_importance_fig = KeyInfluencersTab.create_feature_importance_figure(df)
            heatmap_fig = KeyInfluencersTab.create_correlation_heatmap(df)

            # Funktionen/Diagramme des PerformanceInsights-Tabs
            scatter_marketing_fig = PerformanceInsightsTab.create_scatter_marketing_revenue(df)
            box_plot_category_fig = PerformanceInsightsTab.create_box_plot_category(df)

            # Funktionen/Diagramme des CustomerInsights-Tabs
            barchart_category_footfall_fig = CustomerInsightsTab.create_barchart_category_footfall(df)
            scatter_footfall_fig = CustomerInsightsTab.create_scatter_footfall_revenue(df)
            scatter_productvariety_footfall_fig = CustomerInsightsTab.create_scatter_productvariety_vs_footfall(df)
            scatter_marketing_footfall_fig = CustomerInsightsTab.create_scatter_marketing_footfall(df)
            scatter_promotions_footfall_fig = CustomerInsightsTab.create_scatter_promotions_footfall(df)
            barchart_promotions_footfall_fig = CustomerInsightsTab.create_bar_chart_promotions_vs_footfall(df)

            # Funktionen/Diagramme des RegionalComparison-Tabs
            map_fig = RegionalComparisonTab.create_map_visualization(df)
            grouped_bar_fig = RegionalComparisonTab.create_grouped_bar_chart(df)
            scatter_competitor_fig = RegionalComparisonTab.create_scatter_competitor_revenue(df)
            grouped_barchart_footfall_fig = RegionalComparisonTab.create_grouped_barchart_footfall(df)

            # Funktionen/Diagramme des StoreOperations-Tabs
            scatter_productvariety_revenue_fig = StoreOperationsTab.create_scatter_productvariety_revenue(df)
            scatter_productvariety_efficiency_fig = StoreOperationsTab.create_scatter_productvariety_efficiency(df)
            bubble_chart_fig = StoreOperationsTab.create_bubble_chart_operations(df)
            histogram_fig = StoreOperationsTab.create_histogram_efficiency(df)

            # Funktionen/Diagramme des Recommendations-Tabs
            recommendations = RecommendationsTab.create_recommendations_section()

            return (overview, feature_importance_fig, heatmap_fig, barchart_category_footfall_fig, scatter_footfall_fig, scatter_productvariety_footfall_fig, scatter_marketing_footfall_fig, scatter_promotions_footfall_fig, barchart_promotions_footfall_fig,
                    scatter_marketing_fig, scatter_competitor_fig, grouped_barchart_footfall_fig , box_plot_category_fig,
                    map_fig, grouped_bar_fig, scatter_productvariety_revenue_fig, scatter_productvariety_efficiency_fig, bubble_chart_fig, histogram_fig, recommendations)

        #Setup der callbacks fürs Vergleichsfunktion in Dashboard. (DM)
        @self.app.callback(
            [Output("comparison-output", "children"),
             Output("comparison-bar-chart", "figure"),
             Output("comparison-pie-chart", "figure")],
            Input("compare-button", "n_clicks"),
            [State("compare-first", "value"),
             State("compare-second", "value"),
             State("compare-metrics", "value")]
        )
        def update_comparison(n_clicks, first, second, metrics):
            """Erzeugt Vergleichsmetriken und Diagramme...(DM)"""
            if not first or not second or not metrics:
                return "Please select two stores/regions and at least one metric.", go.Figure(), go.Figure()

            df = self.db_connector.fetch_data("SELECT * FROM StoreData")

            comparison_metrics = self.vergleichsfunktion_tab.generate_comparison_metrics(df, first, second, metrics)
            bar_chart = self.vergleichsfunktion_tab.create_comparison_bar_chart(df, first, second, metrics)
            pie_chart = self.vergleichsfunktion_tab.create_comparison_pie_chart(df, first, second)

            return comparison_metrics, bar_chart, pie_chart

        """ Navigation und View-Handling basierend auf der URL (JPG) """

        # Callback zur Hervorhebung des aktiven Tabs in der Sidebar (JPG)
        @self.app.callback(
            [Output("btn-overview", "style"),
             Output("btn-key-influencers", "style"),
             Output("btn-vergleichsfunktion", "style"),
             Output("btn-performance-insights", "style"),
             Output("btn-customer-insights", "style"),
             Output("btn-regional-comparison", "style"),
             Output("btn-store-operations", "style"),
             Output("btn-recommendations", "style")],
            Input("url", "pathname")
        )
        def update_active_tab(pathname):
            default_style = {
                "width": "100%", "height": "60px", "fontSize": "18px",
                "margin": "5px 0", "display": "flex", "alignItems": "center",
                "borderRadius": "12px", "backgroundColor": "#f0f0f0",
                "fontWeight": "normal", "color": "black"
            }
            active_style = default_style.copy()
            active_style["backgroundColor"] = "#007bff"  # Blaues Highlight
            active_style["color"] = "white"
            active_style["fontWeight"] = "bold"

            styles = [default_style] * 8
            if pathname in ["/overview", "/", None]:
                styles[0] = active_style
            elif pathname == "/key-influencers":
                styles[1] = active_style
            elif pathname == "/vergleichsfunktion":
                styles[2] = active_style
            elif pathname == "/performance-insights":
                styles[3] = active_style
            elif pathname == "/customer-insights":
                styles[4] = active_style
            elif pathname == "/regional-comparison":
                styles[5] = active_style
            elif pathname == "/store-operations":
                styles[6] = active_style
            elif pathname == "/recommendations":
                styles[7] = active_style

            return styles

        # Callback, damit nur die aktive View, basierend auf der URL, angezeigt wird (JPG)
        @self.app.callback(
            Output("page-overview", "style"),
            Output("page-key-influencers", "style"),
            Output("page-vergleichsfunktion", "style"),
            Output("page-performance-insights", "style"),
            Output("page-customer-insights", "style"),
            Output("page-regional-comparison", "style"),
            Output("page-store-operations", "style"),
            Output("page-recommendations", "style"),
            Input("url", "pathname")
        )
        def display_page(pathname):
            hidden = {"display": "none"}
            visible = {"display": "block"}
            # Initialisiere alle Views als versteckt.
            styles = [hidden] * 8
            if pathname in ["/overview", "/", None]:
                styles[0] = visible
            elif pathname == "/key-influencers":
                styles[1] = visible
            elif pathname == "/vergleichsfunktion":
                styles[2] = visible
            elif pathname == "/performance-insights":
                styles[3] = visible
            elif pathname == "/customer-insights":
                styles[4] = visible
            elif pathname == "/regional-comparison":
                styles[5] = visible
            elif pathname == "/store-operations":
                styles[6] = visible
            elif pathname == "/recommendations":
                styles[7] = visible
            else:
                styles[0] = visible  # default zur Homepage
            return styles

        # Callback zum Togglen der Sidebar mit dem Button (JPG)
        @self.app.callback(
            Output("sidebar", "style"),
            Output("page-content", "style"),
            Input("toggle-navbar", "n_clicks"),
            State("sidebar", "style"),
            State("page-content", "style")
        )
        def toggle_sidebar(n_clicks, current_sidebar_style, current_content_style):
            if n_clicks is None:
                raise dash.exceptions.PreventUpdate
            # Togglen der sidebar: wenn ungerade Anzahl an Klicks, Verstecken; wenn gerade Anzahl, Zeigen.
            if n_clicks % 2 == 1:
                new_sidebar_style = current_sidebar_style.copy() if current_sidebar_style else {}
                new_sidebar_style["display"] = "none"
                new_content_style = current_content_style.copy() if current_content_style else {}
                new_content_style["margin-left"] = "20px"
                return new_sidebar_style, new_content_style
            else:
                new_sidebar_style = current_sidebar_style.copy() if current_sidebar_style else {}
                new_sidebar_style["display"] = "flex"
                new_content_style = current_content_style.copy() if current_content_style else {}
                new_content_style["margin-left"] = "220px"
                return new_sidebar_style, new_content_style

        # Callback zum Updaten der URL, je nachdem welcher Button geklickt wird (JPG)
        @self.app.callback(
            Output("url", "pathname"),
            [Input("btn-overview", "n_clicks"),
             Input("btn-key-influencers", "n_clicks"),
             Input("btn-vergleichsfunktion", "n_clicks"),
             Input("btn-performance-insights", "n_clicks"),
             Input("btn-customer-insights", "n_clicks"),
             Input("btn-regional-comparison", "n_clicks"),
             Input("btn-store-operations", "n_clicks"),
             Input("btn-recommendations", "n_clicks")]
        )
        # Navigierungsfunktion (JPG)
        def navigate(n_overview, n_key_influencers, n_vergleich, n_perf, n_cust, n_reg, n_store, n_rec):
            ctx = dash.callback_context
            if not ctx.triggered:
                return "/overview"
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id == "btn-overview":
                return "/overview"
            elif button_id == "btn-key-influencers":
                return "/key-influencers"
            elif button_id == "btn-vergleichsfunktion":
                return "/vergleichsfunktion"
            elif button_id == "btn-performance-insights":
                return "/performance-insights"
            elif button_id == "btn-customer-insights":
                return "/customer-insights"
            elif button_id == "btn-regional-comparison":
                return "/regional-comparison"
            elif button_id == "btn-store-operations":
                return "/store-operations"
            elif button_id == "btn-recommendations":
                return "/recommendations"
            return "/overview"

    def run(self):
        """Startet den Dash-Server."""
        self.app.run_server(debug=True)


if __name__ == "__main__":
    dashboard = Dashboard("../Database.db")
    dashboard.run()
