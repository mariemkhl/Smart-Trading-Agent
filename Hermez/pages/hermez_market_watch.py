from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import yfinance as yf

max_length = 50
times = deque(maxlen=max_length)
profits = deque(maxlen=max_length)

# Initialize with empty data
for _ in range(max_length):
    times.append("")
    profits.append(0)

# Function to create a color-coded scatter plot
def create_trace():
    changes = [profits[i] - profits[i - 1] if i > 0 else 0 for i in range(len(profits))]
    colors = ['green' if change >= 0 else 'red' for change in changes]

    trace = go.Scatter(
        x=list(times),
        y=list(profits),
        mode='lines+markers',
        line={'shape': 'spline'},
        marker={'color': colors, 'size': 8}
    )

    return trace

# Layout for Hermez Market Watch page
hermez_market_watch_layout = html.Div([
    html.H2("Hermez Market Watch"),
    html.Div(
        className="col-xl-12 col-md-12",
        children=[
            html.Div(
                className="card sale-card",
                style={'height': '400px','max-width': '1200px', 'margin': '0 auto'},
                children=[
                    html.Div(
                        className="card-header",
                        children=[
                            html.H5("Realtime Profit")
                        ]
                    ),
                    html.Div(
                        className="card-block text-center",
                        children=[
                            dcc.Graph(
                                id='realtime-profit',
                                config={'displayModeBar': False},
                                style={'height': '400px', 'width': '100%'}
                            ),
                            dcc.Interval(
                                id='realtime-profit-interval',
                                interval=500,  # Update every 2 seconds
                                n_intervals=0
                            )
                        ]
                    )
                ]
            )
        ]
    )
])

# Callback function to update the graph
def setup_callbacks(app):
    @app.callback(
        Output('realtime-profit', 'figure'),
        Input('realtime-profit-interval', 'n_intervals')
    )
    def update_graph(n):
        # Fetch the latest data (last 1 minute)
        stock_data = yf.Ticker("AAPL").history(period="1d", interval="1m")
        times.extend(stock_data.index.strftime('%H:%M'))
        profits.extend(stock_data['Close'].pct_change().fillna(0).mul(100).cumsum())

        trace = create_trace()

        layout = go.Layout(
            xaxis={'title': 'Time'},
            yaxis={'title': 'Profit (%)'},
            margin={'l': 40, 'r': 20, 't': 40, 'b': 30},
            hovermode='closest',
            plot_bgcolor='#f9f9f9'
        )

        return {'data': [trace], 'layout': layout}
