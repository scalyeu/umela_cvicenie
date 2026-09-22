import plotly.graph_objects as go

from backend.data_service import SPECIES

BAR_COLOR = "#2c7fb8"


def _layout(fig):
    # spolocne nastavenie vzhladu pre oba grafy
    fig.update_layout(
        title="Počet vyfiltrovaných kvetov podľa druhu",
        xaxis_title="Druh (species)",
        yaxis_title="Počet záznamov",
        margin=dict(l=50, r=20, t=60, b=50),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
    )
    fig.update_xaxes(categoryorder="array", categoryarray=SPECIES, showgrid=False)
    fig.update_yaxes(gridcolor="#e9ecef", zeroline=False, rangemode="tozero")
    return fig


def species_bar_figure(counts):
    values = [counts.get(s, 0) for s in SPECIES]

    fig = go.Figure(
        go.Bar(
            x=SPECIES,
            y=values,
            text=values,
            textposition="outside",
            marker_color=BAR_COLOR,
            hovertemplate="%{x}: %{y} záznamov<extra></extra>",
        )
    )
    _layout(fig)

    # bez rezervy nad stlpcami sa cisla orezu, pri malych poctoch chcem
    # celociselnu os
    if max(values) > 0:
        top = max(values) * 1.2
    else:
        top = 5
    fig.update_yaxes(range=[0, top], dtick=1 if top <= 10 else None)

    if sum(values) == 0:
        fig.add_annotation(
            text="Žiadny záznam nevyhovuje zvoleným filtrom",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=15, color="#6c757d"),
        )
    return fig


def empty_figure(message):
    # graf pred nacitanim dat - prazdny, len s textom v strede
    fig = go.Figure()
    _layout(fig)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False, showgrid=False)
    fig.add_annotation(
        text=message, xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
        font=dict(size=15, color="#6c757d"),
    )
    return fig
