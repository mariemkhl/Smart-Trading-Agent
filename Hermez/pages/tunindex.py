

from dash import html, dcc, dash_table
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import calendar
import numpy as np
import random

# Initialize your Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data from the provided CSV file
tunindex_file_path = r'C:\Users\marie\Desktop\PIDS\DATA\DATA\Data-2eme lot\market_data_indexes_data\Cleaned indexes jdod\TUNINDEX_1.csv'
tunindex_df = pd.read_csv(tunindex_file_path)
tunindex_df['Date'] = pd.to_datetime(tunindex_df['Date'])
tunindex_df['Year'] = tunindex_df['Date'].dt.year
tunindex_df['Month'] = tunindex_df['Date'].dt.month
tunindex_df['Month'] = tunindex_df['Date'].dt.month

# Group by Month and Year, then calculate the average ROI
monthly_avg_roi = tunindex_df.groupby(['Year', 'Month'])['ROI'].mean().reset_index()
# Group by Year, then calculate the average ROI
yearly_avg_roi = tunindex_df.groupby(['Year'])['ROI'].mean().reset_index()

# Create cards for each year's ROI
def create_yearly_roi_cards():
    return [
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.H4(f"Year: {row['Year']}", className="card-title"),
                html.H2(f"{row['ROI']:.2f}%", className="card-value"),
                html.P("Average ROI", className="card-text"),
            ]),
            className="mb-4", style={"width": "18rem"}
        )) for index, row in yearly_avg_roi.iterrows()
    ]


# Create time series plots for each year's monthly ROI
def create_monthly_roi_plots():
    cards = []
    all_rois = monthly_avg_roi['ROI'].tolist()  # Collect all past ROI values for sampling

    for year in sorted(monthly_avg_roi['Year'].unique()):
        year_data = monthly_avg_roi[monthly_avg_roi['Year'] == year]
        months = year_data['Month'].tolist()
        rois = year_data['ROI'].tolist()
        last_known_month = max(months) if months else None

        if year == 2024 and last_known_month and last_known_month < 12:
            # Forecasting beyond the last known month
            for month in range(last_known_month + 1, 13):
                months.append(month)
                sampled_roi = random.choice(all_rois)
                rois.append(sampled_roi)

        actual_trace = go.Scatter(
            x=[calendar.month_abbr[month] for month in months if month <= last_known_month],
            y=rois[:last_known_month],
            mode='lines+markers',
            marker=dict(color='navy'),
            name='Actual'
        )
        
        forecast_trace = go.Scatter(
            x=[calendar.month_abbr[month] for month in months if month > last_known_month],
            y=rois[last_known_month:],
            mode='lines+markers',
            marker=dict(color='red'),
            name='Forecast'
        )

        fig = go.Figure(data=[actual_trace, forecast_trace])
        fig.update_layout(
            title=f"ROI {year}",
            xaxis_title="Month",
            yaxis_title="Average ROI",
            margin={"l": 10, "r": 10, "t": 30, "b": 10},
            height=300
        )
        card = dbc.Card(
            dbc.CardBody([
                dcc.Graph(figure=fig)
            ]),
            className="mb-4", style={"width": "24rem"}
        )
        cards.append(dbc.Col(card, width=4))
    return cards
# Function to create the TUNINDEX layout
def tunindex_layout():
    monthly_roi_plots = create_monthly_roi_plots()
    yearly_cards = create_yearly_roi_cards()
    return dbc.Container([
        html.H1("TUNINDEX Yearly ROI Overview", className="page-header"),
        dbc.Row(yearly_cards),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=create_tunindex_plot(tunindex_df)),
                html.Hr(),
                html.H3("TUNINDEX Data Table", className="page-subheader"),
                create_tunindex_table(tunindex_df)
            ], width=12)
        ]),
        dbc.Row(monthly_roi_plots)  # This adds a new row with all monthly ROI plots
    ], fluid=True, style={"marginLeft": "20px", "paddingTop": "20px"})

 

# Function to create a table from a DataFrame
def create_tunindex_table(df: pd.DataFrame):
    return dash_table.DataTable(
        id='tunindex-table',
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left'}
    )
    
# Function to create a time-series plot for the TUNINDEX data
def create_tunindex_plot(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.update_layout(
        title='TUNINDEX Close Price Over Time',
        xaxis_title='Date',
        yaxis_title='Close Price',
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
        height=300,
        width=800
    )
    return fig    

# Set the app layout
app.layout = tunindex_layout()

if __name__ == '_main_':
    app.run_server(debug=True)
