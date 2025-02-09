import plotly.graph_objects as go  # Detaillierte Schnittstelle zum Erstellen von Plotly-Visualisierungen
import plotly.express as px  # Vereinfachte Schnittstelle zum Erstellen von Plotly-Visualisierung
import math


class RegionalComparisonTab:
    """ View für Regionale bzw. Standortvergleiche (JPG)"""

    @staticmethod
    def get_coordinates(city):
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

    @staticmethod
    def create_map_visualization(df):
        """Erzeugt die Kartenvisualisierung für die Filialverteilung nach Kategorie und Umsatz."""
        regional_comparison = RegionalComparisonTab()  # Instanz der Klasse erstellen

        coordinates = regional_comparison.get_all_coordinates(df)  # Koordinaten für Städte abfragen

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

        map_fig = go.Figure()
        RegionalComparisonTab.add_category_legend(map_fig, category_symbols)
        RegionalComparisonTab.add_city_labels(map_fig, coordinates, city_category_stats)
        RegionalComparisonTab.add_category_markers(map_fig, df, coordinates, city_category_stats, category_symbols)

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

    @staticmethod
    def add_category_legend(map_fig, category_symbols):
        """Separate Legende, um Farben nicht zu verfälschen."""
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

    @staticmethod
    def add_city_labels(map_fig, coordinates, city_category_stats):
        """Fügt Namen der Städte in Karte hinzu"""
        city_categories = RegionalComparisonTab.get_city_categories(city_category_stats)
        city_labels_lats, city_labels_lons, city_names = RegionalComparisonTab.get_city_label_positions(coordinates,
                                                                                                        city_categories)

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

    @staticmethod
    def get_city_categories(city_category_stats):
        """ Kategorien für jede Stadt abfragen """
        city_categories = {}
        for _, row in city_category_stats.iterrows():
            if row['StoreLocation'] not in city_categories:
                city_categories[row['StoreLocation']] = []
            city_categories[row['StoreLocation']].append(row['StoreCategory'])
        return city_categories

    @staticmethod
    def get_city_label_positions(coordinates, city_categories):
        """Holt Positionen für Stadtlabels"""
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

    @staticmethod
    def add_category_markers(map_fig, df, coordinates, city_category_stats, category_symbols):
        """Fügt Kategorie-Marker hinzu."""
        # Farbskala für den Umsatz
        colorscale = [[0, 'red'], [0.5, 'yellow'], [1.0, 'green']]
        standard_size = 30
        categories = df['StoreCategory'].unique()
        city_categories = RegionalComparisonTab.get_city_categories(city_category_stats)

        for category in categories:
            # Filtere die Daten für die aktuelle Kategorie
            category_data = city_category_stats[city_category_stats['StoreCategory'] == category]

            # Hole die Positionen der Marker für die aktuelle Kategorie
            lats, lons = RegionalComparisonTab.get_category_marker_positions(category_data, coordinates,
                                                                             city_categories, category)

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

    @staticmethod
    def get_category_marker_positions(category_data, coordinates, city_categories, category):
        """Holt Positionen für Kategorie-Marker"""
        lats = []  # Liste für Breitengrade der Marker
        lons = []  # Liste für Längengrade der Marker
        for city in category_data['StoreLocation']:
            base_lat, base_lon = coordinates[city]
            if base_lat is not None and base_lon is not None:
                city_cat_count = len(city_categories[city])  # Anzahl der Kategorien in der Stadt
                cat_idx_in_city = city_categories[city].index(category)  # Index der aktuellen Kategorie in der Stadt
                lat, lon = RegionalComparisonTab.calculate_marker_position(
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

    @staticmethod
    def create_grouped_bar_chart(df):
        """Erzeugt ein gruppiertes Balkendiagramm für Umsatz nach Stadt und Kategorie."""
        df_grouped = df.groupby(["StoreLocation", "StoreCategory"], as_index=False)["MonthlySalesRevenue"].mean()

        fig = px.bar(
            df_grouped,
            x="StoreLocation",
            y="MonthlySalesRevenue",
            color="StoreCategory",
            barmode="group",
            title="Average Monthly Sales Revenue by Store Location and Category",
            labels={"StoreLocation": "Store Location", "MonthlySalesRevenue": "Avg. Monthly Sales Revenue"},
            hover_data=["MonthlySalesRevenue"]
        )
        return fig

    @staticmethod
    def create_scatter_competitor_revenue(df):
        """
        Erzeugt ein Scatter-Plot für Competitor Distance vs. Revenue mit festen Farben.
        Dabei werden die Stores anhand ihrer StoreLocation farblich unterschieden. (JE und JPG)
        """
        fig = px.scatter(
            df,
            x="CompetitorDistance",
            y="MonthlySalesRevenue",
            color="StoreCategory",
            trendline="ols",
            title="Competitor Distance vs. Revenue",
            labels={"CompetitorDistance": "Competitor Distance", "MonthlySalesRevenue": "Monthly Sales Revenue"}
        )
        return fig

    @staticmethod
    def create_grouped_barchart_footfall(df):
        """Erzeugt ein gruppiertes Balkendiagramm für Kundenfrequenz nach Stadt und Kategorie."""
        df_grouped = df.groupby(["StoreLocation", "StoreCategory"], as_index=False)["CustomerFootfall"].mean()

        fig = px.bar(
            df_grouped,
            x="StoreLocation",
            y="CustomerFootfall",
            color="StoreCategory",
            barmode="group",
            title="Average Customer Footfall by Store Location and Category",
            labels={"StoreLocation": "Store Location", "CustomerFootfall": "Avg. Customer Footfall"},
            hover_data=["CustomerFootfall"]
        )
        return fig
