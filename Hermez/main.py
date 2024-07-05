import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group


# Import layouts and functions from pages
from pages.dashboard import dashboard_layout, setup_dashboard_callbacks
from pages.tunindex import tunindex_layout
from pages.live_pricing import live_pricing_layout
from pages.hermez_market_watch import hermez_market_watch_layout, setup_callbacks
from pages.sectoral_indices import sectoral_index_layout
from pages.actions import actions_layout, setup_actions_callbacks
from pages.indicators import indicators_layout
from pages.settings import settings_layout
from pages.help import help_layout
from pages.sign_in import sign_in_layout, setup_sign_in_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/custom.css"])
app.title = "Stock Dashboard"
app.config.suppress_callback_exceptions = True

# Sidebar layout
sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src="/assets/Steve_Jobs_Headshot_2010-CROP_(cropped_2).jpg", className="profile-pic", alt="Profile Picture"),
                html.P("ASSET MANAGER", className="small"),
            ],
            className="text-center"
        ),
        html.Div([
            html.Div("MAIN", className="small sidebar-title"),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/dashboard", className="nav-link text-white", active='exact'),
                    dbc.NavLink("TUNINDEX", href="/tunindex", className="nav-link text-white", active='exact'),
                    dbc.NavLink("Live Pricing", href="/live-pricing", className="nav-link text-white", active='exact')
                ],
                vertical=True,
                pills=True,
                className="nav nav-pills flex-column mb-auto"
            ),
            html.Div("Stock Exchange", className="small sidebar-title"),
            dbc.Nav(
                [
                    dbc.NavLink("Hermez Market Watch", href="/hermez-market-watch", className="nav-link text-white", active='exact'),
                    dbc.NavLink("Sectoral Indices", href="/sectoral-indices", className="nav-link text-white", active='exact'),
                    dbc.NavLink("Actions", href="/actions", className="nav-link text-white", active='exact'),
                    dbc.NavLink("Portfolio", href="/Portfolio", className="nav-link text-white", active='exact'),
                ],
                vertical=True,
                pills=True,
                className="nav nav-pills flex-column mb-auto"
            ),
            html.Div("WordCloud", className="small sidebar-title"),
            dbc.Nav(
                [
                    dbc.NavLink("WordCloud", href="/WordCloud", className="nav-link text-white", active='exact'),
                ],
                vertical=True,
                pills=True,
                className="nav nav-pills flex-column mb-auto"
            )
        ], className="sidebar-nav"),
        html.Div([
            html.A("Logout Account", href="/logout", className="nav-link text-danger")
        ], className="footer")
    ],
    className="sidebar"
)

# Layout setup
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # This element tracks the current URL
    html.Div(id='page-layout')
])

# Callback to update the layout dynamically
@app.callback(
    Output('page-layout', 'children'),
    [Input('url', 'pathname')]
)
def display_layout(pathname):
    if pathname == '/sign-in' or pathname == '/logout':
        return sign_in_layout
    else:
        return html.Div([
            sidebar,
            html.Div(id='page-content', className="main-content")
        ])



# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/dashboard':
        return dashboard_layout()
    elif pathname == '/tunindex':
        return tunindex_layout()
    elif pathname == '/live-pricing':
        return live_pricing_layout()
    elif pathname == '/hermez-market-watch':
        return hermez_market_watch_layout
    elif pathname == '/sectoral-indices':
        return sectoral_index_layout()
    elif pathname == '/actions':
        return actions_layout()
    elif pathname == '/Portfolio':
        return indicators_layout()
    elif pathname == '/WordCloud':
        return settings_layout()
    elif pathname == '/help':
        return help_layout()
    elif pathname == '/logout' or pathname == '/sign-in':
        return sign_in_layout
    else:
        return sign_in_layout  # Default to sign in layout

# Setup callbacks for the individual pages
setup_dashboard_callbacks(app)
setup_callbacks(app)
setup_sign_in_callbacks(app)
setup_actions_callbacks(app)  # Setup the actions page callbacks

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
