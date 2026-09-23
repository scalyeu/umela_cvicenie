import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from backend.data_service import IRIS_URL, NUMERIC_COLS, REQUIRED_COLS
from callbacks.figures import empty_figure

dash.register_page(__name__, path="/", name="Dashboard", title="Iris Data Explorer")

SLIDER_LABELS = {
    "sepal_length": "Sepal Length",
    "sepal_width": "Sepal Width",
    "petal_length": "Petal Length",
    "petal_width": "Petal Width",
}


def info_row(label, value_id):
    return html.Div(
        [
            html.Span(label + ": ", className="text-muted"),
            html.Span("-", id=value_id, className="fw-bold"),
        ],
        className="info-row",
    )


def slider_block(col):
    return dbc.Col(
        [
            html.Div(
                [
                    html.Span(SLIDER_LABELS[col], className="fw-semibold"),
                    html.Span("-", id="range-" + col, className="text-muted small"),
                ],
                className="d-flex justify-content-between",
            ),
            # min/max 0-1 je len docasne, spravne hodnoty nastavi prvy callback
            dcc.RangeSlider(
                id="slider-" + col,
                min=0,
                max=1,
                step=0.1,
                value=[0, 1],
                disabled=True,
                allowCross=False,
                tooltip={"placement": "bottom"},
            ),
        ],
        md=6,
        className="mb-3",
    )


overview_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Prehľad dát", className="card-title"),
            info_row("Všetky záznamy", "total-count"),
            info_row("Vyfiltrované", "filtered-count"),
            info_row("Podiel z celku", "filtered-pct"),
            info_row("Zobrazená strana", "page-info"),
            html.Div(
                [
                    html.Span("Stav: ", className="text-muted"),
                    dcc.Loading(
                        html.Span("dáta nie sú načítané", id="load-status",
                                  className="fw-bold"),
                        type="dot",
                        parent_style={"display": "inline-block"},
                    ),
                ],
                className="info-row",
            ),
            html.Hr(),
            dbc.Label("Zdroj dát (CSV URL)", html_for="url-input", className="small"),
            dbc.Input(id="url-input", value=IRIS_URL, type="url", size="sm",
                      className="mb-2"),
            html.Div(
                [
                    dbc.Button("Načítať dáta", id="load-button", color="primary"),
                    dbc.Button("Obnoviť filtre", id="reset-button", color="secondary",
                               outline=True, disabled=True),
                ],
                className="d-flex gap-2 flex-wrap",
            ),
        ]
    ),
    className="h-100",
)

graph_card = dbc.Card(
    dbc.CardBody(
        dcc.Graph(
            id="species-graph",
            figure=empty_figure('Stlačte tlačidlo "Načítať dáta"'),
            config={"displayModeBar": False},
            style={"height": "340px"},
        )
    ),
    className="h-100",
)

filter_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Filtrovanie rozsahov", className="card-title"),
            html.P(
                "Riadok zostane vo výsledku, iba ak spĺňa všetky štyri rozsahy "
                "naraz (AND).",
                className="text-muted small",
            ),
            dbc.Row([slider_block(col) for col in NUMERIC_COLS]),
        ]
    )
)

table_card = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.H5("Vyfiltrované dáta", className="card-title mb-0"),
                    html.Span("10 záznamov na strane", className="text-muted small"),
                ],
                className="d-flex justify-content-between align-items-center mb-3",
            ),
            dash_table.DataTable(
                id="table",
                columns=[{"name": col, "id": col} for col in REQUIRED_COLS],
                data=[],
                page_size=10,
                page_action="native",
                page_current=0,
                sort_action="native",
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left", "padding": "6px 10px",
                            "fontFamily": "inherit"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f1f4f8"},
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "#fafbfc"}
                ],
            ),
            html.P("Tabuľka, počty aj graf zobrazujú výsledok rovnakého filtra.",
                   className="text-muted small mt-3 mb-0"),
        ]
    )
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(overview_card, md=4, className="mb-3"),
                dbc.Col(graph_card, md=8, className="mb-3"),
            ]
        ),
        dbc.Row(dbc.Col(filter_card, className="mb-3")),
        dbc.Row(dbc.Col(table_card, className="mb-3")),
    ]
)
