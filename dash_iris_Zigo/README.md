# Iris Data Explorer

Dashboard v Plotly Dash nad datasetom Iris. Po spustení sa dáta ešte nenačítajú, stiahnu sa až keď sa klikne na Načítať dáta. Potom sa dá filtrovať cez štyri slidery (sepal length, sepal width, petal length, petal width) a podľa toho sa mení počet záznamov, graf aj tabuľka.

## Spustenie

```
pip install -r requirements.txt
python app.py
```

Potom otvoriť http://127.0.0.1:8050

## Štruktúra

- app.py - hlavný súbor, vytvorí sa tu aplikácia a navbar
- pages/home.py - layout stránky
- backend/data_service.py - načítanie CSV a filtrovanie
- callbacks/iris_callbacks.py - callbacky
- callbacks/figures.py - graf
- assets/styles.css - css

## Callbacky

Sú tam 3 callbacky:

1. load_or_reset - spustí sa po kliknutí na Načítať dáta alebo Obnoviť filtre. Načíta dáta z URL a nastaví slidery na min a max hodnoty z dát. Ak sa CSV nepodarí načítať, vypíše chybu a slidery ostanú vypnuté.
2. apply_filters - spustí sa pri zmene sliderov, vyfiltruje dáta a aktualizuje počet, percentá, graf a tabuľku.
3. show_page_info - ukazuje, na ktorej strane tabuľky sa práve je.

Dáta sú uložené v premennej _df v data_service.py, dcc.Store som nepoužil.

## Navyše

Pridal som pole na zadanie vlastnej URL k CSV súboru (skontroluje sa, či má správne stĺpce) a tlačidlo Obnoviť filtre, ktoré vráti slidery na začiatok.
