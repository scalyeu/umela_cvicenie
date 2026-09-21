"""Backend: načítanie, uchovanie a filtrovanie Iris datasetu.

Načítaný DataFrame je uložený v tomto module (bez dcc.Store).
Načíta sa až volaním load_iris_data() z callbacku, nikdy pri importe
ani pri štarte aplikácie.
"""

import pandas as pd

IRIS_URL = "https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv"

NUMERIC_COLS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
REQUIRED_COLS = NUMERIC_COLS + ["species"]
SPECIES = ["setosa", "versicolor", "virginica"]

_df = None  # načítaný dataset; None = dáta ešte nie sú načítané


def load_iris_data(url=IRIS_URL):
    """Načíta CSV z URL, skontroluje stĺpce a uloží DataFrame do backendu.

    Pri chybe vyhodí ValueError so zrozumiteľnou správou a dáta v backende
    zruší, aby bol stav aplikácie konzistentný.
    """
    global _df
    _df = None
    try:
        df = pd.read_csv(url)
    except Exception as error:
        raise ValueError(f"CSV sa nepodarilo načítať ({error})") from error

    missing = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing:
        raise ValueError(f"v súbore chýbajú stĺpce: {', '.join(missing)}")

    df = df[REQUIRED_COLS].dropna()
    try:
        df[NUMERIC_COLS] = df[NUMERIC_COLS].apply(pd.to_numeric)
    except Exception as error:
        raise ValueError("číselné stĺpce obsahujú nečíselné hodnoty") from error
    if df.empty:
        raise ValueError("súbor neobsahuje žiadne záznamy")

    _df = df.reset_index(drop=True)
    return _df


def has_data():
    """True, ak sú dáta načítané."""
    return _df is not None


def get_data():
    """Celý načítaný DataFrame (alebo None)."""
    return _df


def get_ranges():
    """{stĺpec: (min, max)} zo skutočných hodnôt datasetu, zaokrúhlené na 0.1."""
    return {
        col: (round(float(_df[col].min()), 1), round(float(_df[col].max()), 1))
        for col in NUMERIC_COLS
    }


def filter_data(ranges):
    """Vráti riadky, ktoré spĺňajú VŠETKY rozsahy naraz (logické AND).

    ranges: {stĺpec: [dolná, horná]} – hranice sú vrátane.
    """
    mask = pd.Series(True, index=_df.index)
    for col, (lo, hi) in ranges.items():
        mask &= _df[col].between(lo, hi)
    return _df[mask]


def species_counts(df):
    """Počty záznamov pre všetky tri druhy; chýbajúci druh dostane 0."""
    counts = df["species"].value_counts()
    return {species: int(counts.get(species, 0)) for species in SPECIES}
