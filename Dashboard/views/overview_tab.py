from dash import html, dcc
import plotly.express as px

class OverviewTab:
    @staticmethod
    def create_overview_section(df):
        """Erzeugt eine visuell ansprechende Übersicht über wichtige Kennzahlen, Rankings und ein Kuchendiagramm. (JPG und JE)"""

        # Wichtige Kennzahlen berechnen
        total_revenue = df["MonthlySalesRevenue"].sum()
        avg_footfall = df["CustomerFootfall"].mean()
        total_marketing_spend = df["MarketingSpend"].sum()
        total_promotions = df["PromotionsCount"].sum()

        # Übersichtliche Darstellung der Kennzahlen
        metrics = [
            {"label": "Total Monthly Sales Revenue", "value": f"${total_revenue:,.2f}", "icon": "💰"},
            {"label": "Average Customer Footfall", "value": f"{avg_footfall:,.0f}", "icon": "🚶‍♂️"},
            {"label": "Total Marketing Spend", "value": f"${total_marketing_spend:,.2f}", "icon": "📣"},
            {"label": "Total Promotions", "value": f"{total_promotions}", "icon": "🎉"}
        ]

        # Top 5 und Flop 5 Stores nach Umsatz berechnen
        top_5_stores = df.nlargest(5, "MonthlySalesRevenue")[
            ["StoreID", "MonthlySalesRevenue", "StoreCategory", "StoreLocation"]
        ].reset_index(drop=True)
        flop_5_stores = df.nsmallest(5, "MonthlySalesRevenue")[
            ["StoreID", "MonthlySalesRevenue", "StoreCategory", "StoreLocation"]
        ].reset_index(drop=True)

        # Städte Ranking nach Umsatz
        city_ranking = df.groupby("StoreLocation")["MonthlySalesRevenue"].sum().sort_values(ascending=False).reset_index()

        # Kategorie Ranking nach Umsatz
        category_ranking = df.groupby("StoreCategory")["MonthlySalesRevenue"].sum().sort_values(ascending=False).reset_index()

        # Anzahl der Stores pro Kategorie (Daten für das Kuchendiagramm)
        stores_per_category = df.groupby("StoreCategory").size().reset_index(name="StoreCount")

        # Kuchendiagramm erstellen
        pie_chart = dcc.Graph(
            figure=px.pie(
                stores_per_category,
                names="StoreCategory",
                values="StoreCount",
                title="Stores per Category",
                hole=0.4
            ).update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                showlegend=True,
                title_x=0.5
            ),
            style={"height": "300px"}
        )

        # HTML Darstellung der Top 5 Stores
        top_5_list = html.Div(
            [
                html.H4("🏅 Top 5 Stores by Revenue"),
                html.Ol(
                    [
                        html.Li(
                            html.Div(
                                [
                                    html.Span("🏆", style={"margin-right": "10px", "font-size": "20px"}),
                                    html.Span(f"Store {row['StoreID']}", style={"font-weight": "bold", "margin-right": "10px"}),
                                    html.Span(f"({row['StoreCategory']}, {row['StoreLocation']})", style={"color": "#555"}),
                                    html.Span(f"${row['MonthlySalesRevenue']:,.2f}", style={"color": "#4CAF50", "margin-left": "10px"})
                                ],
                                style={"display": "flex", "align-items": "center", "margin-bottom": "5px"}
                            )
                        )
                        for i, row in top_5_stores.iterrows()
                    ],
                    style={"padding-left": "20px"}
                )
            ],
            style={
                "background-color": "#e8f5e9",
                "border-radius": "8px",
                "padding": "15px",
                "margin-bottom": "20px",
                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            }
        )

        # HTML Darstellung der Flop 5 Stores
        flop_5_list = html.Div(
            [
                html.H4("📉 Flop 5 Stores by Revenue"),
                html.Ol(
                    [
                        html.Li(
                            html.Div(
                                [
                                    html.Span("❌", style={"margin-right": "10px", "font-size": "20px"}),
                                    html.Span(f"Store {row['StoreID']}", style={"font-weight": "bold", "margin-right": "10px"}),
                                    html.Span(f"({row['StoreCategory']}, {row['StoreLocation']})", style={"color": "#555"}),
                                    html.Span(f"${row['MonthlySalesRevenue']:,.2f}", style={"color": "#e53935", "margin-left": "10px"})
                                ],
                                style={"display": "flex", "align-items": "center", "margin-bottom": "5px"}
                            )
                        )
                        for i, row in flop_5_stores.iterrows()
                    ],
                    style={"padding-left": "20px"}
                )
            ],
            style={
                "background-color": "#ffebee",
                "border-radius": "8px",
                "padding": "15px",
                "margin-bottom": "40px",  # Abstand zum nächsten Element
                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            }
        )

        # HTML Darstellung des Städte-Rankings
        city_ranking_list = html.Div(
            [
                html.H4("🏙️ City Ranking by Revenue"),
                html.Ol(
                    [
                        html.Li(
                            html.Div(
                                [
                                    html.Span("📍", style={"margin-right": "10px", "font-size": "20px"}),
                                    html.Span(f"{row['StoreLocation']}", style={"font-weight": "bold", "margin-right": "10px"}),
                                    html.Span(f"${row['MonthlySalesRevenue']:,.2f}", style={"color": "#4CAF50", "margin-left": "10px"})
                                ],
                                style={"display": "flex", "align-items": "center", "margin-bottom": "5px"}
                            )
                        )
                        for _, row in city_ranking.iterrows()
                    ],
                    style={"padding-left": "20px"}
                )
            ],
            style={
                "background-color": "#e3f2fd",
                "border-radius": "8px",
                "padding": "15px",
                "margin-bottom": "20px",
                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            }
        )

        # HTML Darstellung des Kategorie-Rankings
        category_ranking_list = html.Div(
            [
                html.H4("📦 Category Ranking by Revenue"),
                html.Ol(
                    [
                        html.Li(
                            html.Div(
                                [
                                    html.Span("📊", style={"margin-right": "10px", "font-size": "20px"}),
                                    html.Span(f"{row['StoreCategory']}", style={"font-weight": "bold", "margin-right": "10px"}),
                                    html.Span(f"${row['MonthlySalesRevenue']:,.2f}", style={"color": "#4CAF50", "margin-left": "10px"})
                                ],
                                style={"display": "flex", "align-items": "center", "margin-bottom": "5px"}
                            )
                        )
                        for _, row in category_ranking.iterrows()
                    ],
                    style={"padding-left": "20px"}
                )
            ],
            style={
                "background-color": "#fff3e0",
                "border-radius": "8px",
                "padding": "15px",
                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            }
        )

        # Gesamte Sektion erstellen
        return html.Div(
            [
                html.H3("Key Metrics Overview"),
                html.Div(
                    [
                        html.Div(
                            html.Ul(
                                [
                                    html.Li(
                                        html.Div(
                                            [
                                                html.Span(metric["icon"], style={"margin-right": "10px", "font-size": "20px"}),
                                                html.Span(metric["label"], style={"font-weight": "bold", "margin-right": "5px"}),
                                                html.Span(metric["value"], style={"color": "#4CAF50"})
                                            ],
                                            style={
                                                "display": "flex",
                                                "align-items": "center",
                                                "margin-bottom": "10px",
                                                "font-size": "16px"
                                            }
                                        )
                                    )
                                    for metric in metrics
                                ],
                                style={"list-style-type": "none", "padding": "0"}
                            ),
                            style={"flex": "1"}
                        ),
                        html.Div(
                            pie_chart,
                            style={"flex": "1", "padding-left": "20px"}
                        )
                    ],
                    style={"display": "flex", "align-items": "center", "margin-bottom": "40px"}
                ),
                top_5_list,
                flop_5_list,
                city_ranking_list,
                category_ranking_list
            ],
            style={
                "background-color": "#f9f9f9",
                "border": "1px solid #ddd",
                "border-radius": "8px",
                "padding": "20px",
                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
            }
        )
