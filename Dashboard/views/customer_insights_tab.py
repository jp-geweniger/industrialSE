import plotly.express as px
from dash import html

class CustomerInsightsTab:
    @staticmethod
    def create_customer_heatmap(df):
       return px.density_heatmap(df, x="StoreLocation", y="StoreCategory",
                                 z="CustomerFootfall", histfunc="sum",
                                 title="Customer Footfall Heatmap",
                                labels={"StoreLocation": "Location", "StoreCategory": "Category"})
