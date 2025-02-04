import dash  # Framework zum Erstellen von Webanwendungen
from dash import dcc, html, Input, Output, State  # Komponenten und Rückrufe für Dash-Anwendungen
import sqlite3  # SQLite-Datenbankverbindung und -operationen
import pandas as pd  # Datenmanipulation und -analyse
import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierungen
import plotly.graph_objects as go  # Detaillierte Schnittstelle zum Erstellen von Plotly-Visualisierungen
import math


class SQLiteConnector:
    def __init__(self, db_path):
        self.db_path = db_path

    def fetch_data(self, query):
        """Fetch data from the SQLite database."""
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

    """Beginn Funktionen für die Map (Jan-Philipp Geweniger(JPG))"""
    def get_coordinates(self, city):
        """ Gibt hardkodierte Koordinaten für Städte zurück """
        fallback_coordinates = {
            'Palo Alto': (37.4419, -122.1430),
            'Los Angeles': (34.0522, -118.2437),
            'Sacramento': (38.5816, -121.4944),
            'San Francisco': (37.7749, -122.4194),
        }
        return fallback_coordinates.get(city, (None, None))

    def get_all_coordinates(self, df):
        """ Fragt die hardkodierten Koordinaten ab """
        coordinates = {}
        for city in df['StoreLocation'].unique():
            coordinates[city] = self.get_coordinates(city)
        return coordinates
    # Ende Funktionen für die Map (JPG)

    @staticmethod
    def calculate_marker_position(base_lat, base_lon, index, total_categories, radius=0.15):
        """
        Berechnet verschobene Position für Marker in einem Kreis um den Basispunkt, damit sie nicht übereinander liegen.
        """
        if total_categories == 1:
            return base_lat, base_lon

        # Berechne Position auf dem Kreis
        angle = (2 * math.pi * index) / total_categories

        # Berechne Versatz
        lat_offset = radius * math.sin(angle)
        lon_offset = radius * math.cos(angle)

        return base_lat + lat_offset, base_lon + lon_offset

    """Ende Funktionen für die Map (JPG)"""

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
                ], id="btn-overview", n_clicks=0, style={"width": "100%", "height": "60px", "fontSize": "18px",
                                                         "margin": "5px 0", "display": "flex", "alignItems": "center",
                                                         "borderRadius": "12px", "backgroundColor": "#f0f0f0"}),

                html.Button([
                    html.Span(html.I(className="fas fa-key", style={"color": "#28a745"}), style={"width": "30px"}),
                    html.Span("Key Influencers", style={"flex": "1", "textAlign": "left"})
                ], id="btn-key-influencers", n_clicks=0, style={"width": "100%", "height": "60px", "fontSize": "18px",
                                                                "margin": "5px 0", "display": "flex",
                                                                "alignItems": "center",
                                                                "borderRadius": "12px", "backgroundColor": "#f0f0f0"}),

                html.Button([
                    html.Span(html.I(className="fas fa-balance-scale", style={"color": "#6f42c1"}),
                              style={"width": "30px"}),
                    html.Span("Vergleichsfunktion", style={"flex": "1", "textAlign": "left"})
                ], id="btn-vergleichsfunktion", n_clicks=0,
                    style={"width": "100%", "height": "60px", "fontSize": "18px",
                           "margin": "5px 0", "display": "flex", "alignItems": "center",
                           "borderRadius": "12px", "backgroundColor": "#f0f0f0"}),

                html.Button([
                    html.Span(html.I(className="fas fa-tachometer-alt", style={"color": "#007bff"}),
                              style={"width": "30px"}),
                    html.Span("Performance Insights", style={"flex": "1", "textAlign": "left"})
                ], id="btn-performance-insights", n_clicks=0,
                    style={"width": "100%", "height": "60px", "fontSize": "18px",
                           "margin": "5px 0", "display": "flex", "alignItems": "center",
                           "borderRadius": "12px", "backgroundColor": "#f0f0f0"}),

                html.Button([
                    html.Span(html.I(className="fas fa-user", style={"color": "#ffc107"}), style={"width": "30px"}),
                    html.Span("Customer Insights", style={"flex": "1", "textAlign": "left"})
                ], id="btn-customer-insights", n_clicks=0, style={"width": "100%", "height": "60px", "fontSize": "18px",
                                                                  "margin": "5px 0", "display": "flex",
                                                                  "alignItems": "center",
                                                                  "borderRadius": "12px",
                                                                  "backgroundColor": "#f0f0f0"}),

                html.Button([
                    html.Span(html.I(className="fas fa-map-marker-alt", style={"color": "#dc3545"}),
                              style={"width": "30px"}),
                    html.Span("Regional Comparison", style={"flex": "1", "textAlign": "left"})
                ], id="btn-regional-comparison", n_clicks=0,
                    style={"width": "100%", "height": "60px", "fontSize": "18px",
                           "margin": "5px 0", "display": "flex", "alignItems": "center",
                           "borderRadius": "12px", "backgroundColor": "#f0f0f0"}),

                html.Button([
                    html.Span(html.I(className="fas fa-store", style={"color": "#6610f2"}), style={"width": "30px"}),
                    html.Span("Store Operations", style={"flex": "1", "textAlign": "left"})
                ], id="btn-store-operations", n_clicks=0, style={"width": "100%", "height": "60px", "fontSize": "18px",
                                                                 "margin": "5px 0", "display": "flex",
                                                                 "alignItems": "center",
                                                                 "borderRadius": "12px", "backgroundColor": "#f0f0f0"}),

                html.Button([
                    html.Span(html.I(className="fas fa-lightbulb", style={"color": "#17a2b8"}),
                              style={"width": "30px"}),
                    html.Span("Recommendations", style={"flex": "1", "textAlign": "left"})
                ], id="btn-recommendations", n_clicks=0, style={"width": "100%", "height": "60px", "fontSize": "18px",
                                                                "margin": "5px 0", "display": "flex",
                                                                "alignItems": "center",
                                                                "borderRadius": "12px", "backgroundColor": "#f0f0f0"})
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

                html.Div([
                    html.H2("Vergleichsfunktion")
                ], id="page-vergleichsfunktion", style={"display": "none"}),

                html.Div([
                    html.H2("Performance Insights"),
                    dcc.Graph(id="scatter-footfall-revenue"),
                    dcc.Graph(id="scatter-marketing-revenue"),
                    dcc.Graph(id="scatter-competitor-revenue"),
                    dcc.Graph(id="box-plot-category")
                ], id="page-performance-insights", style={"display": "none"}),

                html.Div([
                    html.H2("Customer Insights")
                ], id="page-customer-insights", style={"display": "none"}),

                html.Div([
                    html.H2("Regional Comparison"),
                    dcc.Graph(id="map-visualization"),
                    dcc.Graph(id="grouped-bar-chart")
                ], id="page-regional-comparison", style={"display": "none"}),

                html.Div([
                    html.H2("Store Operations"),
                    dcc.Graph(id="bubble-chart-operations"),
                    dcc.Graph(id="histogram-efficiency")
                ], id="page-store-operations", style={"display": "none"}),

                html.Div([
                    html.H2("Recommendations"),
                    html.Div(id="recommendations-section")
                ], id="page-recommendations", style={"display": "none"}),
            ], id="page-content", style={"margin-left": "220px", "padding": "20px"})
        ])

    def setup_callbacks(self):
        """Setup the callbacks for the dashboard."""
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
            """Erzeugt das Dashboard im Gesamten."""
            df = self.db_connector.fetch_data("SELECT * FROM StoreData")
            overview = self.create_overview_section(df)
            feature_importance_fig = self.create_feature_importance_figure()
            heatmap_fig = self.create_correlation_heatmap(df)
            scatter_footfall_fig = self.create_scatter_footfall_revenue(df)
            scatter_marketing_fig = self.create_scatter_marketing_revenue(df)
            scatter_competitor_fig = self.create_scatter_competitor_revenue(df)
            box_plot_category_fig = self.create_box_plot_category(df)
            map_fig = self.create_map_visualization(df)
            grouped_bar_fig = self.create_grouped_bar_chart(df)
            bubble_chart_fig = self.create_bubble_chart_operations(df)
            histogram_fig = self.create_histogram_efficiency(df)
            recommendations = self.create_recommendations_section()

            return (overview, feature_importance_fig, heatmap_fig, scatter_footfall_fig,
                    scatter_marketing_fig, scatter_competitor_fig, box_plot_category_fig,
                    map_fig, grouped_bar_fig, bubble_chart_fig, histogram_fig, recommendations)

        """ Navigation und View-Handling basierend auf der URL (JPG) """

        #Callback, damit nur die aktive View, basierend auf der URL, angezeigt wird
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
            # Initialize all pages as hidden.
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

        # Callback zum Togglen der Sidebar mit dem Button
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

        # Callback zum Updaten der URL, je nachdem welcher Button geklickt wird
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
        # Navigierungsfunktion
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

    def create_overview_section(self, df):
        """Erzeugt Übersichts-Sektion."""
        total_revenue = df["MonthlySalesRevenue"].sum()
        avg_footfall = df["CustomerFootfall"].mean()
        total_marketing_spend = df["MarketingSpend"].sum()
        total_promotions = df["PromotionsCount"].sum()

        return html.Ul([
            html.Li(f"Total Monthly Sales Revenue: ${total_revenue:,.2f}"),
            html.Li(f"Average Customer Footfall: {avg_footfall:,.0f}"),
            html.Li(f"Total Marketing Spend: ${total_marketing_spend:,.2f}"),
            html.Li(f"Total Promotions: {total_promotions}")
        ])

    def create_feature_importance_figure(self):
        """Erzeugt Platzhalter."""
        fig = go.Figure()
        fig.update_layout(title="Feature Importance (Placeholder)")
        return fig

    def create_correlation_heatmap(self, df):
        """Erzeugt Korrelations-Heatmap"""
        numeric_df = df.select_dtypes(include=["number"])
        correlation_matrix = numeric_df.corr()
        return px.imshow(correlation_matrix, text_auto=True, title="Correlation Heatmap")

    def create_scatter_footfall_revenue(self, df):
        """Erzeugt das Streudiagramm für Footfall vs. Umsatz."""
        return px.scatter(df, x="CustomerFootfall", y="MonthlySalesRevenue",
                          title="Customer Footfall vs Revenue",
                          labels={"CustomerFootfall": "Customer Footfall", "MonthlySalesRevenue": "Revenue"},
                          hover_data=["StoreID"])

    def create_scatter_marketing_revenue(self, df):
        """Erzeugt das Streudiagramm für Marketingausgaben vs. Umsatz."""
        return px.scatter(df, x="MarketingSpend", y="MonthlySalesRevenue",
                          title="Marketing Spend vs Revenue",
                          labels={"MarketingSpend": "Marketing Spend", "MonthlySalesRevenue": "Revenue"},
                          hover_data=["StoreID"])

    def create_scatter_competitor_revenue(self, df):
        """Erzeugt das Streudiagramm für Wettbewerberentfernung vs. Umsatz."""
        return px.scatter(df, x="CompetitorDistance", y="MonthlySalesRevenue",
                          title="Competitor Distance vs Revenue",
                          labels={"CompetitorDistance": "Competitor Distance", "MonthlySalesRevenue": "Revenue"},
                          hover_data=["StoreID"])

    def create_box_plot_category(self, df):
        """Erzeugt das Boxplot-Diagramm für den Umsatz nach Geschäftskategorie."""
        return px.box(df, x="StoreCategory", y="MonthlySalesRevenue",
                      title="Revenue by Store Category",
                      labels={"StoreCategory": "Store Category", "MonthlySalesRevenue": "Revenue"},
                      hover_data=["StoreID"])

    """Beginn Kartenfunktionalität (JPG)"""
    def create_map_visualization(self, df):
        """Erzeugt die Kartenvisualisierung für die Filialverteilung nach Kategorie und Umsatz."""
        coordinates = self.get_all_coordinates(df)

        # Aggregieren der Daten pro Stadt und Kategorie
        city_category_stats = df.groupby(['StoreLocation', 'StoreCategory']).agg({
            'StoreID': 'count',
            'MonthlySalesRevenue': 'mean'
        }).reset_index()

        # Dictionary für Kategorie-Symbole
        category_symbols = {
            'Clothing': 'circle',
            'Electronics': 'diamond',
            'Grocery': 'square',
        }

        # Erstellen der Figur
        map_fig = go.Figure()
        self.add_category_legend(map_fig, category_symbols)
        self.add_city_labels(map_fig, coordinates, city_category_stats)
        self.add_category_markers(map_fig, df, coordinates, city_category_stats, category_symbols)

        map_fig.update_layout(
            title='Store Distribution by Category and Revenue',
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='rgb(243, 243, 243)',
                countrycolor='rgb(204, 204, 204)',
                showsubunits=True,
                subunitcolor='rgb(204, 204, 204)',
                center=dict(lat=36.7783, lon=-119.4179),  # Zentrierung auf Kalifornien
                fitbounds="locations",  # Karte automatisch auf Symbole anpassen
                resolution=50
            ),
            legend=dict(
                title='Store Categories',
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            height=800
        )
        return map_fig

    # Erstellen einer farblosen Legende für die Kategorien
    def add_category_legend(self, map_fig, category_symbols):
        """Add category legend to the map figure."""
        for category in category_symbols.keys():
            map_fig.add_trace(go.Scattergeo(
                lon=[None],  # Keine Marker auf der Karte
                lat=[None],
                mode='markers',
                name=category,  # Kategorienamen für die Legende
                marker=dict(
                    size=20,  # Größe der Legendenmarker
                    symbol=category_symbols[category],  # Plotly-Symbol
                    color='black',  # Farblose Darstellung in der Legende
                    line=dict(width=1, color='black')
                ),
                showlegend=True  # Nur für die Legende anzeigen
            ))

    def add_city_labels(self, map_fig, coordinates, city_category_stats):
        """Fügt Namen der Städte in Karte hinzu"""
        city_categories = self.get_city_categories(city_category_stats)
        city_labels_lats, city_labels_lons, city_names = self.get_city_label_positions(coordinates, city_categories)

        # Fügt Stadtlabels als separate Trace hinzu
        map_fig.add_trace(go.Scattergeo(
            lon=city_labels_lons,
            lat=city_labels_lats,
            text=city_names,
            mode='text',
            name='Cities',
            textfont=dict(
                size=20,
                color='black'
            ),
            textposition='top right',
            showlegend=False,
            hoverinfo='none'
        ))

    def get_city_categories(self, city_category_stats):
        """Get categories for each city. TODO: entfernen"""
        city_categories = {}
        for _, row in city_category_stats.iterrows():
            if row['StoreLocation'] not in city_categories:
                city_categories[row['StoreLocation']] = []
            city_categories[row['StoreLocation']].append(row['StoreCategory'])
        return city_categories

    def get_city_label_positions(self, coordinates, city_categories):
        """Get positions for city labels."""
        city_labels_lats = []
        city_labels_lons = []
        city_names = []

        for city in city_categories.keys():
            base_lat, base_lon = coordinates[city]
            if base_lat is not None and base_lon is not None:
                city_labels_lats.append(base_lat)
                city_labels_lons.append(base_lon)
                city_names.append(city)
        return city_labels_lats, city_labels_lons, city_names

    def add_category_markers(self, map_fig, df, coordinates, city_category_stats, category_symbols):
        """Fügt Kategorie-Marker hinzu."""
        # Farbskala für den Umsatz
        colorscale = [[0, 'red'], [0.5, 'yellow'], [1.0, 'green']]
        standard_size = 30
        categories = df['StoreCategory'].unique()
        city_categories = self.get_city_categories(city_category_stats)

        for category in categories:
            # Filtere die Daten für die aktuelle Kategorie
            category_data = city_category_stats[city_category_stats['StoreCategory'] == category]

            # Hole die Positionen der Marker für die aktuelle Kategorie
            lats, lons = self.get_category_marker_positions(category_data, coordinates, city_categories, category)

            # Bestimme den minimalen und maximalen Umsatz für die Farbskala
            min_revenue = city_category_stats['MonthlySalesRevenue'].min()
            max_revenue = city_category_stats['MonthlySalesRevenue'].max()

            # Füge eine neue Trace für die aktuelle Kategorie hinzu
            map_fig.add_trace(go.Scattergeo(
                lon=lons,  # Längengrade der Marker
                lat=lats,  # Breitengrade der Marker
                text=category_data.apply(
                    lambda x: f"City: {x['StoreLocation']}<br>" +
                              f"Category: {x['StoreCategory']}<br>" +
                              f"Store Count: {x['StoreID']}<br>" +
                              f"Avg. Revenue: ${x['MonthlySalesRevenue']:,.2f}",
                    axis=1
                ),
                mode='markers+text',
                name=category,
                textfont=dict(
                    size=10,
                    color='black'
                ),
                textposition='middle center',
                texttemplate=category_data['StoreID'].astype(str),
                marker=dict(
                    size=standard_size,
                    color=category_data['MonthlySalesRevenue'],  # Farbe basierend auf dem Umsatz
                    colorscale=colorscale,
                    cmin=min_revenue,
                    cmax=max_revenue,
                    colorbar=dict(
                        title="Avg. Monthly Revenue (k$)",
                        tickformat=".0f",  # Format der Ticks
                        tickvals=[min_revenue, (min_revenue + max_revenue) / 2, max_revenue],  # Tick-Werte
                        ticks="outside"  # Ticks außerhalb der Farbskala
                    ),
                    symbol=category_symbols.get(category, 'circle'),  # Symbol basierend auf der Kategorie
                    line=dict(width=1, color='black')
                ),
                hoverinfo='text',
                showlegend=False  # Legende nicht anzeigen, da diese separat gerendert wird.
            ))

    def get_category_marker_positions(self, category_data, coordinates, city_categories, category):
        """Holt Positionen für Kategorie-Marker"""
        lats = []  # Liste für Breitengrade der Marker
        lons = []  # Liste für Längengrade der Marker
        for city in category_data['StoreLocation']:
            base_lat, base_lon = coordinates[city]
            if base_lat is not None and base_lon is not None:
                city_cat_count = len(city_categories[city])  # Anzahl der Kategorien in der Stadt
                cat_idx_in_city = city_categories[city].index(category)  # Index der aktuellen Kategorie in der Stadt
                lat, lon = self.calculate_marker_position(
                    base_lat, base_lon,
                    cat_idx_in_city,
                    city_cat_count,
                    0.17  # Radius für die Verschiebung der Marker, damit sie nicht übereinander liegen
                )
                lats.append(lat)
                lons.append(lon)
            else:
                lats.append(None)
                lons.append(None)
        return lats, lons

    """Ende Kartenfunktionalität (JPG)"""

    def create_grouped_bar_chart(self, df):
        """Erzeugt das gruppierte Balkendiagramm für den Umsatz nach Standort und Kategorie. (JPG)"""
        return px.bar(df, x="StoreLocation", y="MonthlySalesRevenue", color="StoreCategory",
                      title="Revenue by Location and Category",
                      labels={"MonthlySalesRevenue": "Revenue", "StoreLocation": "Location"},
                      hover_data=["StoreID"])

    def create_bubble_chart_operations(self, df):
        """Erzeugt das Blasendiagramm für Filialgröße, Effizienz und Umsatz."""
        return px.scatter(df, x="StoreSize", y="MonthlySalesRevenue",
                          size="EmployeeEfficiency", color="StoreCategory",
                          title="Store Size, Efficiency, and Revenue",
                          labels={"StoreSize": "Store Size", "MonthlySalesRevenue": "Revenue", "EmployeeEfficiency": "Efficiency"},
                          hover_data=["StoreID"])

    def create_histogram_efficiency(self, df):
        """Erzeugt das Histogramm für die Verteilung der Mitarbeitereffizienz."""
        return px.histogram(df, x="EmployeeEfficiency",
                            title="Employee Efficiency Distribution",
                            labels={"EmployeeEfficiency": "Efficiency"},
                            hover_data=["StoreID"])

    def create_recommendations_section(self):
        """Erzeugt Empfehlungssektion."""
        return html.Ul([
            html.Li("Increase marketing spend for locations with high footfall but low revenue."),
            html.Li("Focus promotional activities on top-performing categories."),
            html.Li("Optimize employee efficiency in underperforming stores.")
        ])

    def run(self):
        """Startet den Dash-Server."""
        self.app.run_server(debug=True)


if __name__ == "__main__":
    dashboard = Dashboard("Database.db")
    dashboard.run()
