# Nacitanie a filtrovanie datasetu. DataFrame si drzim priamo tu v module,
# dcc.Store som nepouzil. Nacitava sa az vtedy, ked sa zavola load_iris_data()
# z callbacku - pri importe sa nestahuje nic.

import pandas as pd

IRIS_URL = "https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv"

NUMERIC_COLS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
REQUIRED_COLS = NUMERIC_COLS + ["species"]
SPECIES = ["setosa", "versicolor", "virginica"]

_df = None


def load_iris_data(url=IRIS_URL):
    global _df

    # ak nacitanie zlyha, stare data uz nechcem mat v pamati
    _df = None

    try:
        df = pd.read_csv(url)
    except Exception as e:
        raise ValueError("CSV sa nepodarilo načítať (%s)" % e)

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError("v súbore chýbajú stĺpce: " + ", ".join(missing))

    df = df[REQUIRED_COLS].dropna()

    try:
        df[NUMERIC_COLS] = df[NUMERIC_COLS].apply(pd.to_numeric)
    except Exception:
        raise ValueError("číselné stĺpce obsahujú nečíselné hodnoty")

    if df.empty:
        raise ValueError("súbor neobsahuje žiadne záznamy")

    _df = df.reset_index(drop=True)
    return _df


def has_data():
    return _df is not None


def get_data():
    return _df


def get_ranges():
    # min a max beriem zo skutocnych dat, zaokruhlene na jedno desatinne miesto
    ranges = {}
    for col in NUMERIC_COLS:
        ranges[col] = (round(float(_df[col].min()), 1), round(float(_df[col].max()), 1))
    return ranges


def filter_data(ranges):
    # riadok prejde len ak vyhovuje vsetkym styrom rozsahom naraz (AND),
    # hranice su vratane
    mask = pd.Series(True, index=_df.index)
    for col, (lo, hi) in ranges.items():
        mask &= _df[col].between(lo, hi)
    return _df[mask]


def species_counts(df):
    counts = df["species"].value_counts()
    return {s: int(counts.get(s, 0)) for s in SPECIES}
