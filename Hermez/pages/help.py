from dash import html
import dash_bootstrap_components as dbc

def help_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Help", className="page-header"),
                html.P("Help page.")
            ], width=12)
        ])
    ], fluid=True, className="page-content")
