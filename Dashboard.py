import dash
from dash import dcc, html, Input, Output
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import math
import json
import os

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
        self.coordinates_cache = self.load_coordinates_cache()
        self.setup_layout()
        self.setup_callbacks()

    def load_coordinates_cache(self):
        """Lädt gecachte Koordinaten oder erstellt einen neuen Cache."""
        cache_file = 'coordinates_cache.json'
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_coordinates_cache(self):
        """Speichert die Koordinaten im Cache."""
        cache_file = 'coordinates_cache.json'
        with open(cache_file, 'w') as f:
            json.dump(self.coordinates_cache, f)

    def geocode_locations(self, df):
        """Geocodes city names to coordinates with caching and fallback values."""
        # Vorbereitete Fallback-Koordinaten für große Städte
        fallback_coordinates = {
            'Palo Alto': (37.4419, -122.1430),
            'Los Angeles': (34.0522, -118.2437),
            'Sacramento': (38.5816, -121.4944),
            'San Francisco': (37.7749, -122.4194),
        }

        # Initialisiere Geocoder nur wenn nötig
        geolocator = None
        geocode = None

        coordinates = {}
        for city in df['StoreLocation'].unique():
            # Prüfe zunächst den Cache
            if city in self.coordinates_cache:
                coordinates[city] = tuple(self.coordinates_cache[city])
                continue

            # Prüfe dann die Fallback-Werte
            city_key = next((k for k in fallback_coordinates.keys()
                           if k.lower() in city.lower()), None)
            if city_key:
                coordinates[city] = fallback_coordinates[city_key]
                self.coordinates_cache[city] = list(fallback_coordinates[city_key])
                continue

            # Wenn weder Cache noch Fallback verfügbar, versuche Geocoding
            if geolocator is None:
                geolocator = Nominatim(user_agent="my_dashboard")
                geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1,
                                    max_retries=3, error_wait_seconds=2.0)

            try:
                location = geocode(f"{city}, USA")
                if location:
                    coordinates[city] = (location.latitude, location.longitude)
                    self.coordinates_cache[city] = [location.latitude, location.longitude]
                    time.sleep(1)  # Zusätzliche Verzögerung
                else:
                    print(f"Could not find coordinates for {city}")
                    coordinates[city] = (None, None)
            except Exception as e:
                print(f"Error geocoding {city}: {e}")
                coordinates[city] = (None, None)

        # Speichere aktualisierte Koordinaten
        self.save_coordinates_cache()
        return coordinates

    @staticmethod
    def calculate_marker_position(base_lat, base_lon, index, total_categories, radius=0.05):
        """
        Berechnet verschobene Position für Marker in einem Kreis um den Basispunkt.
        """
        if total_categories == 1:
            return base_lat, base_lon

        # Berechne Position auf dem Kreis
        angle = (2 * math.pi * index) / total_categories

        # Berechne Versatz
        lat_offset = radius * math.sin(angle)
        lon_offset = radius * math.cos(angle)

        return base_lat + lat_offset, base_lon + lon_offset

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

            ## Anfang der Regional Comparison Section
            ## Erstellen einer Karte mit Store-Verteilung nach Kategorie und Umsatz
            # Get coordinates for all locations
            coordinates = self.geocode_locations(df)

            # Aggregieren der Daten pro Stadt und Kategorie
            city_category_stats = df.groupby(['StoreLocation', 'StoreCategory']).agg({
                'StoreID': 'count',  # Anzahl der Stores
                'MonthlySalesRevenue': 'mean'  # Durchschnittlicher Umsatz
            }).reset_index()

            # Dictionary für Kategorie-Symbole
            category_symbols = {
                'Clothing': 'circle',
                'Electronics': 'diamond',
                'Grocery': 'square',
            }

            # Erstellen der Figur
            map_fig = go.Figure()

            # Erstellen einer farblosen Legende für die Kategorien
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

            # Farbskala für den Umsatz
            colorscale = [[0, 'red'], [0.5, 'yellow'], [1.0, 'green']]

            # Standard Kreisgröße für alle Marker
            standard_size = 30

            # Anzahl der Kategorien
            categories = df['StoreCategory'].unique()

            # Dictionary zum Speichern der Kategorien pro Stadt
            city_categories = {}
            for _, row in city_category_stats.iterrows():
                if row['StoreLocation'] not in city_categories:
                    city_categories[row['StoreLocation']] = []
                city_categories[row['StoreLocation']].append(row['StoreCategory'])

            city_labels_lats = []
            city_labels_lons = []
            city_names = []

            for city in city_categories.keys():
                base_lat, base_lon = coordinates[city]
                if base_lat is not None and base_lon is not None:
                    city_labels_lats.append(base_lat)
                    city_labels_lons.append(base_lon)
                    city_names.append(city)

            # Füge Stadtlabels als separate Trace hinzu
            map_fig.add_trace(go.Scattergeo(
                lon=city_labels_lons,
                lat=city_labels_lats,
                text=city_names,
                mode='text',
                name='Städte',
                textfont=dict(
                    size=20,
                    color='black'
                ),
                textposition='top right',
                showlegend=False,
                hoverinfo='none'
            ))

            # Hinzufügen der Daten für jede Kategorie
            for category_idx, category in enumerate(categories):
                category_data = city_category_stats[city_category_stats['StoreCategory'] == category]

                # Get coordinates for this category's cities
                lats = []
                lons = []
                for city in category_data['StoreLocation']:
                    base_lat, base_lon = coordinates[city]
                    if base_lat is not None and base_lon is not None:
                        # Berechne verschobene Position basierend auf der Anzahl der Kategorien in dieser Stadt
                        city_cat_count = len(city_categories[city])
                        cat_idx_in_city = city_categories[city].index(category)
                        lat, lon = self.calculate_marker_position(
                            base_lat, base_lon,
                            cat_idx_in_city,
                            city_cat_count,
                            0.08
                        )
                        lats.append(lat)
                        lons.append(lon)
                    else:
                        lats.append(None)
                        lons.append(None)

                # Dynamische Skalierung der Legende
                # Berechnet die Min-, Maxwerte aus den Umsatzdaten
                min_revenue = city_category_stats['MonthlySalesRevenue'].min()
                max_revenue = city_category_stats['MonthlySalesRevenue'].max()

                # Setze den Farbskalenbereich
                cmin_value = min_revenue
                cmax_value = max_revenue

                # Marker für die Kategorien
                map_fig.add_trace(go.Scattergeo(
                    lon=lons,
                    lat=lats,
                    text=category_data.apply(
                        lambda x: f"Stadt: {x['StoreLocation']}<br>" +
                                  f"Kategorie: {x['StoreCategory']}<br>" +
                                  f"Anzahl Stores: {x['StoreID']}<br>" +
                                  f"Durchschn. Umsatz: ${x['MonthlySalesRevenue']:,.2f}",
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
                        color=category_data['MonthlySalesRevenue'],
                        colorscale=colorscale,
                        cmin=cmin_value,
                        cmax=cmax_value,
                        colorbar=dict(
                            title=f"Durchschn.<br>Monatsumsatz (k$)<br>",
                            tickformat=".0f",  # Format in Tausendern
                            tickvals=[cmin_value, (cmin_value + cmax_value) / 2, cmax_value],  # Dynamische Tick-Werte
                            ticks="outside"
                        ),
                        symbol=category_symbols.get(category, 'circle'),
                        line=dict(width=1, color='black')
                    ),
                    hoverinfo='text',
                    showlegend=False  # Keine Legende für die farbcodierten Marker
                ))

            # Layout-Konfiguration für die Karte
            map_fig.update_layout(
                title='Store-Verteilung nach Kategorie und Umsatz',
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
                    title='Store-Kategorien',
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                ),
                height=800
            )

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
