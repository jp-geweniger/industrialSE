import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

data = pd.read_csv('C:\\Users\\jan\\Desktop\\WP Stores\\Store_CA Überarbeitet.csv', delimiter=';')


# Selecting relevant features for clustering
features = ["StoreSize", "CustomerFootfall", "EmployeeEfficiency", "MonthlySalesRevenue"]
clustering_data = data[features]

# Standardizing the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(clustering_data)

# Finding the optimal number of clusters using the Elbow Method
inertia = []
k_values = range(1, 11)

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# Choosing the optimal number of clusters (e.g., 3 based on the plot)
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(scaled_data)

# Adding cluster labels to the original dataset
data['Cluster'] = kmeans.labels_

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Store Clustering Dashboard"),
    dcc.Graph(id='cluster-scatter'),
    html.Label("Select Features for Visualization:"),
    dcc.Dropdown(
        id='x-feature',
        options=[{'label': feature, 'value': feature} for feature in features],
        value='StoreSize',
        clearable=False
    ),
    dcc.Dropdown(
        id='y-feature',
        options=[{'label': feature, 'value': feature} for feature in features],
        value='CustomerFootfall',
        clearable=False
    )
])

# Callback to update scatter plot
@app.callback(
    Output('cluster-scatter', 'figure'),
    Input('x-feature', 'value'),
    Input('y-feature', 'value')
)
def update_scatter(x_feature, y_feature):
    fig = px.scatter(
        data, 
        x=x_feature, 
        y=y_feature, 
        color='Cluster', 
        title=f"Clusters based on {x_feature} and {y_feature}", 
        hover_data=features
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
