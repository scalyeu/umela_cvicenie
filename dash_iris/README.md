# Iris Data Explorer (Plotly Dash)

Interaktívny dashboard pre Iris dataset. Po stlačení tlačidla **Načítať dáta**
sa dataset stiahne z internetu, štyri RangeSlidery filtrujú dáta podľa
číselných vlastností kvetov a výsledok sa zobrazí v informačnom paneli,
stĺpcovom grafe a tabuľke.

## Inštalácia a spustenie

```bash
pip install -r requirements.txt
python app.py
```

Aplikácia beží na <http://127.0.0.1:8050>.

## Štruktúra projektu

```
dash_iris/
|-- app.py                     # vytvorenie aplikácie, Dash Pages, Bootstrap téma
|-- requirements.txt
|-- README.md
|-- assets/
|   `-- styles.css             # drobné vizuálne úpravy
|-- pages/
|   `-- home.py                # rozloženie hlavnej stránky
|-- backend/
|   `-- data_service.py        # načítanie, kontrola a filtrovanie datasetu
`-- callbacks/
    |-- iris_callbacks.py      # callbacky (načítanie, filtrovanie, stránkovanie)
    `-- figures.py             # tvorba grafov
```

## Callbacky

| # | Callback | Input | State | Output |
|---|----------|-------|-------|--------|
| 1 | `load_or_reset` | tlačidlo *Načítať dáta*, tlačidlo *Obnoviť filtre* | CSV URL | stav, celkový počet, min/max/value/disabled sliderov |
| 2 | `apply_filters` | hodnoty 4 sliderov | – | vyfiltrovaný počet, podiel, graf, dáta tabuľky, aktuálne rozsahy |
| 3 | `show_page_info` | strana a dáta tabuľky | veľkosť strany | text „Zobrazená strana x/y“ |

Dataset sa načíta až po kliknutí (nie pri štarte). Načítaný DataFrame drží
modul `backend/data_service.py`; `dcc.Store` sa nepoužíva.

## Rozšírenia

- vlastná CSV URL s kontrolou požadovaných stĺpcov (chybná URL zobrazí správu),
- tlačidlo *Obnoviť filtre* (vráti slidery na celý rozsah).
