# Iris Data Explorer

Dashboard v Plotly Dash nad datasetom Iris. Dataset sa stiahne až po stlačení
tlačidla **Načítať dáta**, potom sa dá filtrovať štyrmi RangeSlidermi.
Výsledok filtra sa naraz prejaví v informačnom paneli, v stĺpcovom grafe
aj v tabuľke.

## Spustenie

```bash
pip install -r requirements.txt
python app.py
```

Aplikácia potom beží na http://127.0.0.1:8050

## Súbory

- `app.py` - vytvorenie Dash aplikácie, Bootstrap téma, navbar
- `pages/home.py` - rozloženie stránky (karty, slidery, tabuľka)
- `backend/data_service.py` - stiahnutie CSV, kontrola stĺpcov, filtrovanie
- `callbacks/iris_callbacks.py` - tri callbacky
- `callbacks/figures.py` - stĺpcový graf a prázdny graf
- `assets/styles.css` - pár CSS úprav

## Callbacky

**1. `load_or_reset`** - reaguje na obe tlačidlá. Input: `load-button`,
`reset-button`, State: CSV URL. Nastavuje stav, celkový počet záznamov
a min/max/value/disabled všetkých štyroch sliderov. Pri chybnej URL vypíše
hlášku a slidery ostanú vypnuté.

**2. `apply_filters`** - Input: hodnoty štyroch sliderov. Zavolá
`filter_data()` a z jedného výsledku naplní počet, podiel, graf aj tabuľku,
plus texty s aktuálnymi rozsahmi nad slidermi.

**3. `show_page_info`** - Input: `page_current` a dáta tabuľky,
State: `page_size`. Vypíše, na ktorej strane z koľkých sa práve je.

Dáta sú uložené v module `backend/data_service.py` v premennej `_df`,
`dcc.Store` som nepoužil.

## Čo som pridal navyše

- pole na vlastnú CSV URL (kontroluje sa, či súbor má potrebné stĺpce)
- tlačidlo *Obnoviť filtre*, ktoré vráti slidery na celý rozsah dát
