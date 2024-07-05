import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage

# Initialize the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def indicators_layout():
    np.random.seed(42)
    assets = [f'Asset {i+1}' for i in range(20)]
    hrp_weights = np.random.dirichlet(np.ones(len(assets)), size=1)[0]  # Random weights summing to 1
    total_investment = 100000  # Total investment amount

    # Simulate correlation matrix for dendrogram
    corr_matrix = pd.DataFrame(np.random.rand(len(assets), len(assets)), columns=assets, index=assets)
    corr_matrix = corr_matrix.apply(lambda x: (x + x.T)/2)  # Make it symmetric
    distance_matrix = np.sqrt(0.5 * (1 - corr_matrix))  # Convert correlation to distance

    # Calculate investment amounts based on HRP weights
    investments = hrp_weights * total_investment
    linkage_matrix = linkage(distance_matrix, 'ward')

    # Dendrogram plot
    dendro_fig = go.Figure()
    dendro = dendrogram(linkage_matrix, labels=assets, orientation='left', no_plot=True)
    for i, d in enumerate(dendro['dcoord']):
        x = d
        y = dendro['icoord'][i]
        dendro_fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='blue', width=2)))

    dendro_fig.update_layout(title="HRP Dendrogram (Hierarchical Clustering of Assets)",
                             title_x=0.5,  # Centering the title
                             xaxis_title="Distance",
                             yaxis_title="Assets",
                             plot_bgcolor='white',
                             height=500,  # Increased height for better visibility
                             margin={"t": 60, "l": 40, "r": 40, "b": 100})

    # Investment distribution bar chart
    investment_fig = go.Figure(
        data=[go.Bar(x=assets, y=investments,
                     marker={'color': investments, 'colorscale': 'Viridis'},
                     name='Investments')],
        layout=go.Layout(
            title=' Investment Distribution Across Assets Based on HRP Weights',
            title_x=0.5,  # Centering the title
            xaxis={'title': 'Assets'},
            yaxis={'title': 'Amount Invested (TND)'},
            plot_bgcolor='white',
            height=500,  # Increased height for better visibility
            margin={"t": 60, "l": 40, "r": 40, "b": 140})
    )

    # Define the layout for this part of the application
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Hierarchical Risk Parity Investment Simulation", className="text-center mb-4"), width=12),
                dbc.Col(dcc.Graph(figure=dendro_fig, id='dendrogram-plot'), width=6),
                dbc.Col(dcc.Graph(figure=investment_fig, id='investment-bar-chart'), width=6)
            ]),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H3("Invested Amount:", className="text-center"),
                    html.P("TND 100,000", className="lead text-center")
                ], className="shadow p-3 mb-5 bg-white rounded")),
                dbc.Col(html.Div([
                    html.H3("Investment Strategy", className="text-center"),
                    html.P("Investments are distributed across assets based on Hierarchical Risk Parity (HRP) weights. HRP aims to create a portfolio that balances risk across all included assets, dynamically adjusting to market conditions and inter-asset correlations.", className="lead text-center")
                ], className="shadow p-3 mb-5 bg-white rounded"))
            ])
        ])
    ])

# Set the layout of the app to be the Hermez Market Watch layout
app.layout = indicators_layout()

if __name__ == '_main_':
    app.run_server(debug=True)
