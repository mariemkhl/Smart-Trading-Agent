from dash import html, dcc, dash_table, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ALL
import plotly.graph_objs as go
import pandas as pd
import dash
import time

# Tickers and names
tickers = ["ASSMA", "AST", "ATL", "CITY", "BH", "ICF", "LNDOR", "SAH", "SIAM", "SMG", "SOMOC", "SOTE", "STAR", "STPIL", "TJL", "TLNET", "OBCI", "UMED", "WIFAK"]
names = ['AB Inc.', 'BH Corporation', 'BIAT Inc.', 'BNA Corporation', 'BS Corporation',
         'BT Corporation', 'BTEI Inc.', 'STB Corporation', 'UBCI Corporation', 'UIB Inc.',
         'WIFAK Inc.', 'AETEC Corporation', 'OTH Inc.', 'SERVI Inc.', 'SIAM Corporation',
         'SITS Inc.', 'SOKNA Inc.', 'SOTE Corporation', 'STVR Inc.', 'TLNET Corporation']
tickers_and_names = list(zip(tickers, names))

viz_types = ["Time Series", "Candlestick", "Histogram"]
feature_types = ["Price", "Open", "High", "Low", "Vol."]

# Retrieve historical stock data from a CSV file
def retrieve_stock_data(ticker: str) -> pd.DataFrame:
    file_path = f"C:/Users/marie/Desktop/deploy/Hermez/data/cotation/{ticker}-Historical-Data.csv"
    return pd.read_csv(file_path)

# Retrieve normalized data
normalized_data = pd.read_csv('C:/Users/marie/Downloads/dataF (1).csv')

# Calculate averages and volatility per "Valeur"
def calculate_averages_and_volatility(csv_file='C:/Users/marie/Downloads/dataF (1).csv'):
    df = pd.read_csv(csv_file)
    if "Change %" in df.columns and "Adjusted_Close" in df.columns and "ROI" in df.columns and "Valeur" in df.columns and "Volatility" in df.columns:
        change_averages = df.groupby("Valeur")["Change %"].mean() * 100
        adjusted_close_averages = df.groupby("Valeur")["Adjusted_Close"].mean()
        roi_averages = df.groupby("Valeur")["ROI"].mean() * 100
        volatility_averages = df.groupby("Valeur")["Volatility"].mean() * 100
        return change_averages.round(2).to_dict(), adjusted_close_averages.round(2).to_dict(), roi_averages.round(2).to_dict(), volatility_averages.round(2).to_dict()
    else:
        raise ValueError("'Change %', 'Adjusted_Close', 'ROI', 'Volatility', or 'Valeur' column not found in the CSV file")

# Get averages and volatility data per "Valeur"
valeur_change_percent_averages, valeur_adjusted_close_averages, valeur_roi_averages, valeur_volatility_averages = calculate_averages_and_volatility()
valeur_options = [{"label": key, "value": key} for key in valeur_change_percent_averages.keys()]

# Create a multi-feature plot for the historical data
def create_multi_feature_plot(hist_df: pd.DataFrame, feature: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_df['Date'], y=hist_df[feature], mode='lines', name=feature))
    fig.update_layout(title='Stock Features Over Time', xaxis_title='Date', yaxis_title=feature,
                      margin={"t": 0, "l": 0, "r": 0, "b": 0}, height=300, width=550)
    return fig

# Create a candlestick plot for the historical data
def create_candlestick_plot(hist_df: pd.DataFrame):
    return go.Figure(data=[go.Candlestick(x=hist_df['Date'], open=hist_df['Open'],
                                          high=hist_df['High'], low=hist_df['Low'],
                                          close=hist_df['Price'], name='Candlestick')]).update_layout(
        title='Stock Candlestick Over Time', xaxis_title='Date', yaxis_title='Price',
        margin={"t": 0, "l": 0, "r": 0, "b": 0}, height=300, width=550)

# Create a histogram plot for the historical data
def create_histogram_plot(hist_df: pd.DataFrame, feature: str):
    return go.Figure(go.Histogram(x=hist_df[feature], nbinsx=20, name='Histogram')).update_layout(
        title=f'{feature} Distribution', xaxis_title=feature, yaxis_title='Frequency',
        margin={"t": 0, "l": 0, "r": 0, "b": 0}, height=300, width=550)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define CSS for blinking columns directly within the app
app.css.append_css({
    "external_url": [
        {
            "href": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
            "rel": "stylesheet",
            "integrity": "sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm",
            "crossorigin": "anonymous"
        }
    ],
    "internal": """
    @keyframes blink-color {
        0%, 100% { background-color: #f9f9f9; }
        25% { background-color: #fcf3cf; }
        50% { background-color: #d5f5e3; }
        75% { background-color: #aed6f1; }
    }

    .data-table th {
        animation: blink-color 2s infinite;
    }

    .data-table td {
        animation: blink-color 2s infinite;
    }
    """
})

# Proceed with your app configuration and layout


# Create a table for the dashboard with a "Chart" button


def create_data_table(hist_df: pd.DataFrame):
    hist_df['Index'] = hist_df.index

    # Define color cycles for blinking effect
    color_cycle = ['#f9f9f9', '#fcf3cf', '#d5f5e3', '#aed6f1']
    current_time = int(time.time()) % len(color_cycle)  # Get current second to cycle colors

    return dash_table.DataTable(
        id='data-table',
        columns=[
            {"name": col, "id": col} for col in ['Date', 'Price', 'Change %', 'Low', 'High']
        ] + [{"name": "Chart", "id": "Index", "presentation": "markdown"}],
        data=[
            {
                'Date': row['Date'],
                'Price': row['Price'],
                'Change %': row['Change %'],
                'Low': row['Low'],
                'High': row['High'],
                'Index': f"[Show Chart](#/{row['Index']})"
            } for row in hist_df.tail(8).to_dict('records')
        ],
        page_size=10,
        style_table={'height': '270px', 'overflowY': 'auto', 'border': '2px solid #dcdcdc', 'width': '200%'},
        style_as_list_view=True,
        style_header={
            'backgroundColor': '#f8f8f8',
            'fontWeight': 'bold',
            'border': '1px solid #dcdcdc',
            'textAlign': 'center'
        },
        style_cell={
            'backgroundColor': '#fefefe',
            'color': '#333',
            'textAlign': 'left',
            'border': '1px solid #dcdcdc',
            'padding': '10px'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Chart'}, 'textAlign': 'center'}
        ],
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f9f9f9'},
            *({'if': {'column_id': col}, 'backgroundColor': color_cycle[current_time]} for col in ['Date', 'Price', 'Change %', 'Low', 'High'])
        ],
        markdown_options={"link_target": "_self"},
        row_selectable=False,
        editable=False,
        export_columns='visible',
        export_format='csv',
        export_headers='display'
    )


def create_card(title, value, description, icon, card_type=''):
    # Determine the card class based on the value and card type
    card_class = 'mb-3 card-value '
    if card_type == 'change' or card_type == 'roi':
        card_class += 'card-positive' if value >= 0 else 'card-negative'
    else:
        card_class += 'mb-3'

    return dbc.Card(dbc.CardBody([
        html.H5(title, className="card-title"), html.H3(f"{value}%", className="card-value" if value >= 0 else "card-value-negative"),
        html.P(description, className="card-description"), html.I(icon, className="card-icon")
    ]), className=card_class)


# Dashboard layout with cards, graphs, histogram, and table
def dashboard_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Change % ", className="card-title"),
                    dcc.Dropdown(
                        id='valeur-dropdown-change-percent',
                        options=valeur_options,
                        value=list(valeur_change_percent_averages.keys())[0]
                    ),
                    html.H2(id='valeur-change-percent', className="card-value"),
                    html.P("Select a stock", className="card-subtitle"),
                    html.I(className="bi bi-percent")
                ])
            ], className="mb-4"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Adjusted Close ", className="card-title"),
                    dcc.Dropdown(
                        id='valeur-dropdown-adjusted-close',
                        options=valeur_options,
                        value=list(valeur_adjusted_close_averages.keys())[0]
                    ),
                    html.H2(id='valeur-adjusted-close', className="card-value"),
                    html.P("Select a stock", className="card-subtitle"),
                    html.I(className="bi bi-currency-dollar")
                ])
            ], className="mb-4"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("ROI ", className="card-title"),
                    dcc.Dropdown(
                        id='valeur-dropdown-roi',
                        options=valeur_options,
                        value=list(valeur_roi_averages.keys())[0]
                    ),
                    html.H2(id='valeur-roi', className="card-value"),
                    html.P("Select a stock", className="card-subtitle"),
                    html.I(className="bi bi-graph-up-arrow")
                ])
            ], className="mb-4"), width=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Volatility ", className="card-title"),
                    dcc.Dropdown(
                        id='valeur-dropdown-volatility',
                        options=valeur_options,
                        value=list(valeur_volatility_averages.keys())[0]
                    ),
                    html.H2(id='valeur-volatility', className="card-value"),
                    html.P("Select a stock", className="card-subtitle"),
                    html.I(className="bi bi-bar-chart-line")
                ])
            ], className="mb-4"), width=3)
        ]),
        dbc.Row([
           dbc.Col([
    html.H2("Stock Dashboard", className="page-header"),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='ticker-dropdown',
                             options=[{'label': name, 'value': ticker} for ticker, name in tickers_and_names],
                             value='UMED', style={"width": "100%"}), width=4),
        dbc.Col(dcc.Dropdown(id='viz-type-dropdown',
                             options=[{'label': viz, 'value': viz} for viz in viz_types],
                             value='Time Series', style={"width": "100%"}), width=4),
        dbc.Col(dcc.Dropdown(id='feature-type-dropdown',
                             options=[{'label': feature, 'value': feature} for feature in feature_types],
                             value='Price', style={"width": "100%"}), width=4),
    ], className="mb-3"),  # Adjust className as necessary for spacing
    html.Br(), html.Br()
], width=10)
        ]),
        dbc.Row([
            dbc.Col([dcc.Graph(id='line-plot')], width=6),
            dbc.Col([dcc.Graph(id='average-histogram')], width=6)
        ]),
        dbc.Row([dbc.Col([html.Div(id='data-table-container')], width=6)])
    ], fluid=True)

# Callback function for the dashboard page
def setup_dashboard_callbacks(app):
    @app.callback(
        [Output('line-plot', 'figure'),
         Output('average-histogram', 'figure'),
         Output('data-table-container', 'children')],
        [Input('ticker-dropdown', 'value'),
         Input('viz-type-dropdown', 'value'),
         Input('feature-type-dropdown', 'value'),
         Input({'type': 'show-chart', 'index': ALL}, 'n_clicks')]
    )
    def update_dashboard(ticker: str, viz_type: str, feature_type: str, button_clicks):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        # Retrieve the historical data for the selected ticker
        hist_df = retrieve_stock_data(ticker)

        # Update the main graph
        if viz_type == "Time Series":
            main_graph = create_multi_feature_plot(hist_df, feature_type)
        else:
            main_graph = create_candlestick_plot(hist_df)

        # Update the histogram graph
        average_histogram = create_histogram_plot(hist_df, feature_type)

        # Update the data table
        data_table = create_data_table(hist_df)

        return main_graph, average_histogram, data_table

    @app.callback(
        Output('valeur-change-percent', 'children'),
        Input('valeur-dropdown-change-percent', 'value')
    )
    def update_valeur_change_percent(selected_valeur):
        change_percent = valeur_change_percent_averages.get(selected_valeur, 0)
        return f"{change_percent}%"

    @app.callback(
        Output('valeur-adjusted-close', 'children'),
        Input('valeur-dropdown-adjusted-close', 'value')
    )
    def update_valeur_adjusted_close(selected_valeur):
        adjusted_close = valeur_adjusted_close_averages.get(selected_valeur, 0)
        return f"{adjusted_close}TND"

    @app.callback(
        Output('valeur-roi', 'children'),
        Input('valeur-dropdown-roi', 'value')
    )
    def update_valeur_roi(selected_valeur):
        roi = valeur_roi_averages.get(selected_valeur, 0)
        return f"{roi}"

    @app.callback(
        Output('valeur-volatility', 'children'),
        Input('valeur-dropdown-volatility', 'value')
    )
    def update_valeur_volatility(selected_valeur):
        volatility = valeur_volatility_averages.get(selected_valeur, 0)
        return f"{volatility}"

if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = dashboard_layout()
    setup_dashboard_callbacks(app)
    app.run_server(debug=True)
