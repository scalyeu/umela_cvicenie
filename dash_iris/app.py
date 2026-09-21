"""Vstupný bod aplikácie Iris Data Explorer (Plotly Dash + Bootstrap)."""

import dash
import dash_bootstrap_components as dbc
from dash import html

import callbacks.iris_callbacks  # noqa: F401 – registrácia callbackov

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Iris Data Explorer",
)

navbar = dbc.Navbar(
    dbc.Container(
        [dbc.NavbarBrand("Iris Data Explorer", className="fw-bold"),
         html.Span("Dashboard", className="text-white-50")],
        fluid=True,
    ),
    color="primary", dark=True, className="mb-3",
)

app.layout = html.Div([navbar, dbc.Container(dash.page_container, fluid=True)])

if __name__ == "__main__":
    app.run(debug=True)
