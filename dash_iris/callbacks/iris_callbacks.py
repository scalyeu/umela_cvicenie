"""Callbacky dashboardu.

1. load_or_reset  – tlačidlo „Načítať dáta“ (a „Obnoviť filtre“) → načítanie
                    datasetu v backende, stav, celkový počet, rozsahy sliderov.
2. apply_filters  – 4 slidery → vyfiltrovaný DataFrame → počty, graf, tabuľka.
3. show_page_info – stránkovanie tabuľky → text „Zobrazená strana x/y“.
"""

import math

from dash import Input, Output, State, callback, ctx, no_update

from backend import data_service as ds
from callbacks.figures import empty_figure, species_bar_figure

SLIDER_IDS = [f"slider-{col}" for col in ds.NUMERIC_COLS]
EMPTY_GRAPH_MESSAGE = "Stlačte tlačidlo „Načítať dáta“"


def slider_outputs():
    """Output-y (min, max, value, disabled) pre všetky štyri slidery."""
    outputs = []
    for slider_id in SLIDER_IDS:
        outputs += [
            Output(slider_id, "min"),
            Output(slider_id, "max"),
            Output(slider_id, "value"),
            Output(slider_id, "disabled"),
        ]
    return outputs


def slider_state(ranges):
    """Hodnoty pre slider_outputs(). ranges=None → stav pred načítaním."""
    state = []
    for col in ds.NUMERIC_COLS:
        if ranges is None:
            state += [0, 1, [0, 1], True]
        else:
            lo, hi = ranges[col]
            state += [lo, hi, [lo, hi], False]
    return state


# --------------------------------------------------------------------------
# Callback 1 – načítanie dát (a obnovenie filtrov na celý rozsah)
# --------------------------------------------------------------------------
@callback(
    Output("load-status", "children"),
    Output("total-count", "children"),
    Output("reset-button", "disabled"),
    *slider_outputs(),
    Input("load-button", "n_clicks"),
    Input("reset-button", "n_clicks"),
    State("url-input", "value"),
    prevent_initial_call=True,
    running=[(Output("load-button", "disabled"), True, False)],
)
def load_or_reset(_load_clicks, _reset_clicks, url):
    if ctx.triggered_id == "reset-button":
        # Iba vráti slidery na celý rozsah datasetu; dáta sa nenačítavajú znova
        if not ds.has_data():
            return no_update
        return no_update, no_update, False, *slider_state(ds.get_ranges())

    try:
        df = ds.load_iris_data((url or "").strip() or ds.IRIS_URL)
    except ValueError as error:
        # Vrátime stav pred načítaním; zmena hodnôt sliderov spustí
        # filtrovací callback, ktorý zobrazí prázdny stav
        return f"načítanie zlyhalo – {error}", "–", True, *slider_state(None)

    return "dáta načítané", str(len(df)), False, *slider_state(ds.get_ranges())


# --------------------------------------------------------------------------
# Callback 2 – filtrovanie: slidery → panel, graf, tabuľka
# --------------------------------------------------------------------------
@callback(
    Output("filtered-count", "children"),
    Output("filtered-pct", "children"),
    Output("species-graph", "figure"),
    Output("table", "data"),
    Output("table", "page_current"),
    *[Output(f"range-{col}", "children") for col in ds.NUMERIC_COLS],
    *[Input(slider_id, "value") for slider_id in SLIDER_IDS],
    prevent_initial_call=True,
)
def apply_filters(*slider_values):
    if not ds.has_data():
        return "–", "–", empty_figure(EMPTY_GRAPH_MESSAGE), [], 0, *(["–"] * 4)

    ranges = dict(zip(ds.NUMERIC_COLS, slider_values))
    filtered = ds.filter_data(ranges)  # jeden DataFrame pre panel, graf aj tabuľku
    total = len(ds.get_data())

    figure = species_bar_figure(ds.species_counts(filtered))
    range_texts = [f"{lo:.1f} – {hi:.1f}" for lo, hi in slider_values]
    percent = f"{100 * len(filtered) / total:.1f} %"

    return (str(len(filtered)), percent, figure, filtered.to_dict("records"), 0,
            *range_texts)


# --------------------------------------------------------------------------
# Callback 3 – stránkovanie tabuľky → „Zobrazená strana x/y“
# --------------------------------------------------------------------------
@callback(
    Output("page-info", "children"),
    Input("table", "page_current"),
    Input("table", "data"),
    State("table", "page_size"),
)
def show_page_info(page_current, rows, page_size):
    if not rows:
        return "–"
    pages = math.ceil(len(rows) / page_size)
    return f"{(page_current or 0) + 1}/{pages}"
