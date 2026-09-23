import math

from dash import Input, Output, State, callback, ctx, no_update

from backend import data_service as ds
from callbacks.figures import empty_figure, species_bar_figure

SLIDER_IDS = ["slider-" + col for col in ds.NUMERIC_COLS]
NO_DATA_MSG = 'Stlačte tlačidlo "Načítať dáta"'


def slider_outputs():
    # kazdy slider potrebuje 4 outputy, tak si ich vyskladam v cykle
    outputs = []
    for sid in SLIDER_IDS:
        outputs.append(Output(sid, "min"))
        outputs.append(Output(sid, "max"))
        outputs.append(Output(sid, "value"))
        outputs.append(Output(sid, "disabled"))
    return outputs


def slider_state(ranges):
    # ranges = None znamena stav pred nacitanim dat (slidery su vypnute)
    state = []
    for col in ds.NUMERIC_COLS:
        if ranges is None:
            state += [0, 1, [0, 1], True]
        else:
            lo, hi = ranges[col]
            state += [lo, hi, [lo, hi], False]
    return state


# 1. callback - nacitanie dat, pripadne vratenie sliderov na cely rozsah
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
def load_or_reset(load_clicks, reset_clicks, url):
    if ctx.triggered_id == "reset-button":
        if not ds.has_data():
            return no_update
        # data uz mam nacitane, len posuniem slidery naspat na min a max
        return no_update, no_update, False, *slider_state(ds.get_ranges())

    url = (url or "").strip()
    if not url:
        url = ds.IRIS_URL

    try:
        df = ds.load_iris_data(url)
    except ValueError as e:
        # slidery sa vratia do vychodzieho stavu, cim sa spusti druhy callback
        # a ten povypina panel aj graf
        return "načítanie zlyhalo - %s" % e, "-", True, *slider_state(None)

    return "dáta načítané", str(len(df)), False, *slider_state(ds.get_ranges())


# 2. callback - slidery filtruju data pre panel, graf aj tabulku
@callback(
    Output("filtered-count", "children"),
    Output("filtered-pct", "children"),
    Output("species-graph", "figure"),
    Output("table", "data"),
    Output("table", "page_current"),
    *[Output("range-" + col, "children") for col in ds.NUMERIC_COLS],
    *[Input(sid, "value") for sid in SLIDER_IDS],
    prevent_initial_call=True,
)
def apply_filters(*values):
    if not ds.has_data():
        return "-", "-", empty_figure(NO_DATA_MSG), [], 0, "-", "-", "-", "-"

    ranges = dict(zip(ds.NUMERIC_COLS, values))
    filtered = ds.filter_data(ranges)
    total = len(ds.get_data())

    fig = species_bar_figure(ds.species_counts(filtered))
    pct = "%.1f %%" % (100 * len(filtered) / total)
    texts = ["%.1f - %.1f" % (lo, hi) for lo, hi in values]

    return str(len(filtered)), pct, fig, filtered.to_dict("records"), 0, *texts


# 3. callback - cislo aktualnej strany v tabulke
@callback(
    Output("page-info", "children"),
    Input("table", "page_current"),
    Input("table", "data"),
    State("table", "page_size"),
)
def show_page_info(page_current, rows, page_size):
    if not rows:
        return "-"
    pages = math.ceil(len(rows) / page_size)
    return "%d/%d" % ((page_current or 0) + 1, pages)
