from dash import html
import dash_bootstrap_components as dbc

def create_card(title, value, description, icon):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title"),
            html.H3(value, className="card-value"),
            html.P(description, className="card-description"),
            html.I(icon, className="card-icon")
        ]),
        className="mb-3"
    )

def cards_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(create_card("Sales", "$10,567", "Yesterday: +10.57%", "bi bi-cart"), width=4),
            dbc.Col(create_card("Revenue", "$43,594", "Last month: -2%", "bi bi-wallet"), width=4),
            dbc.Col(create_card("Customers", "345k", "Last month: +22%", "bi bi-people"), width=4)
        ])
    ], fluid=True)
