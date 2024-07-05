from dash import html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash
from numpy import polyfit, poly1d
import numpy as np

# Load the data
data = pd.read_csv('C:/Users/marie/Downloads/dataF (1).csv')

# Selecting columns to display in the DataTable
columns_to_display = ['Date', 'Valeur', 'Price', 'Open', 'High', 'Low', 'Change %', 'Volume', 
                      'Adjusted_Close', 'ROI', 'RSI']

def actions_layout():
    unique_stocks = data['Valeur'].unique()  # Unique stocks from the "Valeur" column
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader(
                            children=[
                                html.H5("Stock Actions", className="card-title"),
                                dcc.Dropdown(
                                    id='stock-dropdown',
                                    options=[{'label': stock, 'value': stock} for stock in unique_stocks],
                                    value=unique_stocks[0],  # Default value
                                    clearable=False,
                                    style={'margin-bottom': '40px', 'width': '150px'}
                                ),
                                dbc.Button("Show Plot", id="plot-button", color="primary", n_clicks=0),
                            ],
                            className="d-flex justify-content-between align-items-center"
                        ),
                        dbc.CardBody(
                            [
                                dash_table.DataTable(
                                    id='table',
                                    columns=[{"name": i, "id": i} for i in columns_to_display],
                                    data=data[columns_to_display].to_dict('records'),
                                    page_size=20,
                                    page_action='native',
                                    style_table={'overflowX': 'auto', 'border': '1px solid #ddd'},
                                    style_header={
                                        'backgroundColor': '#007BFF',
                                        'color': 'white',
                                        'fontWeight': 'bold',
                                        'textAlign': 'center'
                                    },
                                    style_data={
                                        'backgroundColor': '#FFFFFF',
                                        'color': '#333333',
                                        'border': '1px solid #ddd'
                                    },
                                    style_cell={'padding': '10px'},
                                    style_data_conditional=[
                                        {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'}
                                    ],
                                    style_as_list_view=True,
                                )
                            ],
                            className="table-responsive"
                        )
                    ],
                    className="card table-card"
                ),
                # Modal for displaying the plot
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Plot")),
                        dbc.ModalBody(dcc.Graph(id='plot-area')),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-plot-modal", className="ms-auto", n_clicks=0)
                        ),
                    ],
                    id="plot-modal",
                    is_open=False,
                    style={"width": "100%", "max-width": "none"}  # Custom width for the modal
                )
            ], xl=12, md=12)
        ])
    ], fluid=True)

import numpy as np

def setup_actions_callbacks(app):
    @app.callback(
        [Output('plot-area', 'figure'),
         Output('plot-modal', 'is_open')],
        [Input('plot-button', 'n_clicks'),
         Input('close-plot-modal', 'n_clicks')],
        [State('plot-modal', 'is_open'),
         State('stock-dropdown', 'value')]  # State to keep track of the selected stock
    )
    def toggle_modal(n_clicks_show, n_clicks_close, is_open, selected_stock):
        if n_clicks_show or n_clicks_close:
            if n_clicks_show > n_clicks_close:
                # Filter data for the selected stock
                filtered_data = data[data['Valeur'] == selected_stock]
                # Convert 'Date' to datetime if it isn't already
                filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
                fig = px.line(filtered_data, x='Date', y='Price', title=f'Price Over Time for {selected_stock}', template='plotly_dark')
                
                # Adding a linear forecast to extend to 2024
                # Convert 'Date' to numeric for polyfit
                filtered_data['DateNumeric'] = filtered_data['Date'].map(pd.Timestamp.toordinal)
                # Fit a first-degree polynomial (linear) to the data
                coeffs = polyfit(filtered_data['DateNumeric'], filtered_data['Price'], 1)
                p = poly1d(coeffs)

                # Create forecast values up to the end of 2024
                last_date = filtered_data['Date'].max()
                forecast_end_date = pd.Timestamp('2024-12-31')
                forecast_dates = pd.date_range(start=last_date, end=forecast_end_date, freq='D')
                forecast_dates_numeric = forecast_dates.map(pd.Timestamp.toordinal)
                forecast_y = p(forecast_dates_numeric)

                # Add the forecast points to the plot
                fig.add_scatter(x=forecast_dates, y=forecast_y, mode='markers', marker=dict(color='red'), name='Forecast')

                # Add horizontal lines at y=30 and y=70
                fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Y = 30", annotation_position="bottom right")
                fig.add_hline(y=70, line_dash="dash", line_color="blue", annotation_text="Y = 70", annotation_position="top right")

                fig.update_layout(autosize=True, width=480, height=400)  # Adjust size as needed
                return fig, True
        return dash.no_update, False

    return toggle_modal

