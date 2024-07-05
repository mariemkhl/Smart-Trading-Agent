
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import os
from datetime import timedelta
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

data_directory = r'C:\Users\marie\Desktop\PIDS\Value DATA\DATA\Data-2eme lot\market_data_indexes_data'  # Adjust this to your actual data directory
sector_files = os.listdir(data_directory)
sectors = [file.split('_')[0] for file in sector_files if file.endswith('.csv')]

def load_data(sector):
    file_path = os.path.join(data_directory, f"{sector}_pi_ds_esprit.csv")
    try:
        sector_data = pd.read_csv(file_path)
        sector_data['Date'] = pd.to_datetime(sector_data['Date'])
        return sector_data
    except Exception as e:
        print(f"Failed to load data for {sector}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def create_time_series_plot(sector_data, sector):
    if sector_data.empty:
        return go.Figure()

    # Historical data plot
    fig = go.Figure(data=[
        go.Scatter(x=sector_data['Date'], y=sector_data['Close'], mode='lines+markers', name='Historical')
    ])

    # Create a fake forecast with random fluctuations
    if not sector_data.empty:
        last_date = sector_data['Date'].iloc[-1]
        last_value = sector_data['Close'].iloc[-1]
        forecast_dates = [last_date + timedelta(days=i) for i in range(1, 31)]  # 30 days of fake forecast
        forecast_values = [last_value]
        
        for i in range(1, 30):
            # Random fluctuation between -2% and +2%
            change_percent = random.uniform(-0.02, 0.02)
            new_value = forecast_values[-1] * (1 + change_percent)
            forecast_values.append(new_value)

        fig.add_trace(go.Scatter(x=forecast_dates, y=forecast_values, mode='lines+markers', name='Forecast', line=dict(color='red')))

    fig.update_layout(title=f'Time Series Plot for {sector} - Close Prices with Forecast',
                      xaxis_title='Date', yaxis_title='Close Price')
    return fig

def sectoral_index_layout():
    cards = []
    for sector in sectors:
        sector_data = load_data(sector)
        fig = create_time_series_plot(sector_data, sector)
        card = dbc.Card(
            dbc.CardBody([
                html.H5(f"{sector}", className="card-title"),
                dcc.Graph(figure=fig),
                html.P(f"Data for {sector} with forecast", className="card-text")
            ]),
            className="mb-4"
        )
        cards.append(dbc.Col(card, width=6))  # Adjust the width as necessary

    return html.Div([
        dbc.Row(cards)
    ])

app.layout = sectoral_index_layout

if __name__ == '_main_':
    app.run_server(debug=True)