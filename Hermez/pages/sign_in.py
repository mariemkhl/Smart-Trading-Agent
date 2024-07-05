from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Layout for the sign-in page
sign_in_layout = html.Section(
    className="h-100 gradient-form",
    style={"background-color": "#f2f2f2"},
    children=[
        html.Div(
            className="container py-5 h-100",
            children=[
                html.Div(
                    className="row d-flex justify-content-center align-items-center h-100",
                    children=[
                        html.Div(
                            className="col-xl-10",
                            children=[
                                html.Div(
                                    className="card rounded-3 text-black",
                                    children=[
                                        html.Div(
                                            className="row g-0",
                                            children=[
                                                html.Div(
                                                    className="col-lg-6",
                                                    children=[
                                                        html.Div(
                                                            className="card-body p-md-5 mx-md-1",
                                                            children=[
                                                                html.Div(
                                                                    className="text-center",
                                                                    children=[
                                                                        html.Img(
                                                                            src="/assets/profile-pic.jpg",
                                                                            style={"width": "185px"},
                                                                            alt="logo"
                                                                        ),
                                                                        html.H4(
                                                                            "We are HERMEZ",
                                                                            className="mt-1 mb-5 pb-1"
                                                                        ),
                                                                    ]
                                                                ),
                                                                html.P("Please login to your account"),
                                                                html.Div(
                                                                    className="form-outline mb-4",
                                                                    children=[
                                                                        dcc.Input(
                                                                            id="username",
                                                                            type="text",
                                                                            placeholder="Phone number or email address",
                                                                            className="form-control",
                                                                            style={"border": "1px solid #ff9800"}
                                                                        ),
                                                                        html.Label(
                                                                            "Username",
                                                                            className="form-label",
                                                                            htmlFor="username",
                                                                            style={"color": "#ff9800"}
                                                                        )
                                                                    ]
                                                                ),
                                                                html.Div(
                                                                    className="form-outline mb-4",
                                                                    children=[
                                                                        dcc.Input(
                                                                            id="password",
                                                                            type="password",
                                                                            className="form-control",
                                                                            style={"border": "1px solid #ff9800"}
                                                                        ),
                                                                        html.Label(
                                                                            "Password",
                                                                            className="form-label",
                                                                            htmlFor="password",
                                                                            style={"color": "#ff9800"}
                                                                        )
                                                                    ]
                                                                ),
                                                                html.Div(
                                                                    className="text-center pt-1 mb-5 pb-1",
                                                                    children=[
                                                                        dbc.Button(
                                                                            "Log in",
                                                                            id="sign-in-button",
                                                                            color="warning",
                                                                            className="btn-block fa-lg gradient-custom-2 mb-3"
                                                                        ),
                                                                        html.A(
                                                                            "Forgot password?",
                                                                            className="text-muted",
                                                                            href="#!"
                                                                        )
                                                                    ]
                                                                ),
                                                                html.Div(
                                                                    id="sign-in-message",
                                                                    className="text-danger mb-4"
                                                                ),
                                                                html.Div(
                                                                    className="d-flex align-items-center justify-content-center pb-4",
                                                                    children=[
                                                                        html.P(
                                                                            "Don't have an account?",
                                                                            className="mb-0 me-2"
                                                                        ),
                                                                        dbc.Button(
                                                                            "Create new",
                                                                            outline=True,
                                                                            color="warning"
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.Div(
                                                    className="col-lg-6 d-flex align-items-center",
                                                    style={
                                                        "background": "linear-gradient(-45deg, #ff9800, #ff5722, #ff7043, #ffab40)",
                                                        "color": "white"
                                                    },
                                                    children=[
                                                        html.Div(
                                                            className="text-white px-3 py-4 p-md-5 mx-md-4",
                                                            children=[
                                                                html.H4("We are more than just a company", className="mb-4"),
                                                                html.P(
                                                                    "HERMEZ is the power of trading. Join us and experience the most advanced trading platform, "
                                                                    "designed to empower you with the tools and insights needed to succeed. "
                                                                    "We are committed to providing unparalleled service and support, ensuring you have the best trading experience possible.",
                                                                    className="small mb-0"
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback to validate sign-in
def setup_sign_in_callbacks(app):
    @app.callback(
        [Output("sign-in-message", "children"), Output("url", "pathname")],
        [Input("sign-in-button", "n_clicks")],
        [State("username", "value"), State("password", "value")]
    )
    def validate_sign_in(n_clicks, username, password):
        if n_clicks and username == "admin" and password == "password":
            return "", "/dashboard"
        else:
            if n_clicks:
                return "Invalid credentials", "/sign-in"
            return "", "/sign-in"
