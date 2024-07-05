import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import random
from collections import deque
import os

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Set up initial data for the real-time graph
max_length = 50
times = deque(maxlen=max_length)
profits = deque(maxlen=max_length)

# Initialize data with some default values
for _ in range(50):
    times.append(_)
    profits.append(random.uniform(0, 100))

# Define sample news data as a static list of dictionaries
news_items = [
    {
        "headline": "Amen Bank 04/25/2024",
        "description": "Amen Bank - Information post General Meeting on 04/25/2024, The resolutions adopted by the Ordinary General Meeting of AMEN BANK, held on 04/25/2024.",
        "image_url": "C:\\Users\\marie\\Desktop\\deploy\\Hermez\\assets\\image2.jpg"
    },
    {
        "headline": "Assurances AMI SA (Over-the-Counter) - Quarterly Activity Indicators as of 03/31/2024",
        "description": "Assurances AMI publishes its activity indicators for the first quarter of 2024.",
        "image_url": "C:\\Users\\marie\\Desktop\\deploy\\Hermez\\assets\\image3.png"

    },
    {
        "headline": "SIMPAR - Ordinary General Meeting on 06/07/2024, Ladies and Gentlemen",
        "description": "Shareholders of the Real Estate and Participation Company 'SIMPAR' are requested to attend the Ordinary General Meeting to be held on Friday, June 07, 2024.",
        "image_url": "C:\\Users\\marie\\Desktop\\deploy\\Hermez\\assets\\images (1).jpg"
    }
]

def live_pricing_layout():
    news_cards = [html.Div([
        html.Img(src=app.get_asset_url(os.path.basename(item['image_url'])), style={'width': '150%', 'height': '200px'}),  # Adjust image source and size
        html.H4(item['headline']),
        html.P(item['description'], style={'text-align': 'justify'})  # Justify the text for better readability
    ], className="news-card", style={'flex': '1 0 21%', 'margin': '20px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'}) for item in news_items]  # Adjust flex properties for responsiveness and add shadows
    
    return html.Div(
        children=[
            html.Div(
                className="col-xl-12 col-md-12",
                children=[
                    html.Div(
                        className="card sale-card",
                        children=[
                            html.Div(
                                className="card-header",
                                children=[html.H5("Realtime Profit")]),
                            html.Div(
                                className="card-block text-center",
                                children=[
                                    dcc.Graph(
                                        id='realtime-profit',
                                        config={'displayModeBar': False},
                                        style={'height': '500px', 'width': '100%'}
                                    ),
                                    dcc.Interval(
                                        id='realtime-profit-interval',
                                        interval=5000,  # Update every 5 seconds
                                        n_intervals=0
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                className="col-xl-8 col-md-12 d-flex flex-wrap justify-content-start",  # Updated classes here for better flex control
                children=news_cards
            )
        ]
    )



# Update the graph based on the interval
@app.callback(
    Output('realtime-profit', 'figure'),
    Input('realtime-profit-interval', 'n_intervals')
)
def update_graph(n):
    # Append new values to the times and profits deque
    times.append(times[-1] + 1 if times else 0)
    profits.append(random.uniform(0, 100))

    trace = go.Scatter(
        x=list(times),
        y=list(profits),
        mode='lines+markers',
        name='Profit',
        line={'shape': 'spline'}
    )

    layout = go.Layout(
        xaxis={'title': 'Time'},
        yaxis={'title': 'Profit (%)'},
        margin={'l': 40, 'r': 20, 't': 40, 'b': 30},
        hovermode='closest',
        plot_bgcolor='#f9f9f9'
    )

    return {'data': [trace], 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
