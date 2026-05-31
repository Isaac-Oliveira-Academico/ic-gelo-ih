"""Gera um HTML final comparando gelo Ih aproximado com e sem vacancia.

Esta etapa fecha a primeira versao tecnica do projeto. O HTML gerado funciona
como uma figura interativa de apresentacao: compara a supercelula perfeita com
a estrutura contendo uma vacancia molecular.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/12b_html_final_vacancia.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ase.io import read


PERFECT_CIF = Path("structures/supercelula_gelo_ih_3x3x2.cif")
VACANCY_CIF = Path("structures/gelo_ih_vacancia.cif")
FIGURES_DIR = Path("figures")
OUTPUT_HTML = FIGURES_DIR / "relatorio_visual_vacancia_gelo_ih.html"


def get_cell_edges(cell):
    """Retorna as arestas da celula."""
    origin = np.array([0.0, 0.0, 0.0])
    a1, a2, a3 = np.array(cell)

    corners = [
        origin,
        a1,
        a2,
        a3,
        a1 + a2,
        a1 + a3,
        a2 + a3,
        a1 + a2 + a3,
    ]

    edge_indices = [
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (1, 5),
        (2, 4),
        (2, 6),
        (3, 5),
        (3, 6),
        (4, 7),
        (5, 7),
        (6, 7),
    ]

    return [(corners[i], corners[j]) for i, j in edge_indices]


def molecule_groups(atoms):
    """Agrupa atomos assumindo ordem O, H, H."""
    groups = []

    for oxygen_index in range(0, len(atoms), 3):
        group = [oxygen_index, oxygen_index + 1, oxygen_index + 2]
        if group[-1] < len(atoms):
            groups.append(group)

    return groups


def estimate_vacancy_position(perfect, vacancy):
    """Estima a posicao da vacancia comparando oxigenios antes e depois."""
    perfect_oxygen_positions = perfect.get_positions()[
        [index for index, atom in enumerate(perfect) if atom.symbol == "O"]
    ]
    vacancy_oxygen_positions = vacancy.get_positions()[
        [index for index, atom in enumerate(vacancy) if atom.symbol == "O"]
    ]

    best_position = perfect_oxygen_positions[0]
    best_distance = -1.0

    for candidate in perfect_oxygen_positions:
        distances = np.linalg.norm(vacancy_oxygen_positions - candidate, axis=1)
        nearest_distance = distances.min()

        if nearest_distance > best_distance:
            best_position = candidate
            best_distance = nearest_distance

    return best_position


def add_cell(fig, cell, col, name):
    """Adiciona a caixa da celula em uma coluna do subplot."""
    first_edge = True

    for start, end in get_cell_edges(cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color="royalblue", width=4),
                name=name if first_edge else None,
                showlegend=first_edge,
                hoverinfo="skip",
            ),
            row=1,
            col=col,
        )
        first_edge = False


def add_atoms(fig, atoms, col, suffix):
    """Adiciona atomos coloridos por elemento."""
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()

    styles = {
        "O": {"color": "red", "size": 4},
        "H": {"color": "white", "size": 2.5},
    }

    for element in ["O", "H"]:
        indices = [index for index, symbol in enumerate(symbols) if symbol == element]
        element_positions = positions[indices]
        style = styles[element]

        fig.add_trace(
            go.Scatter3d(
                x=element_positions[:, 0],
                y=element_positions[:, 1],
                z=element_positions[:, 2],
                mode="markers",
                marker=dict(
                    size=style["size"],
                    color=style["color"],
                    line=dict(color="black", width=0.4),
                ),
                text=[
                    f"{element}{index}<br>"
                    f"x={positions[index, 0]:.3f} A<br>"
                    f"y={positions[index, 1]:.3f} A<br>"
                    f"z={positions[index, 2]:.3f} A"
                    for index in indices
                ],
                hoverinfo="text",
                name=f"{element} {suffix}",
                showlegend=col == 1,
            ),
            row=1,
            col=col,
        )

def add_bonds(fig, atoms, col):
    """Desenha ligacoes O-H didaticas."""
    positions = atoms.get_positions()

    for group in molecule_groups(atoms):
        oxygen = positions[group[0]]

        for hydrogen_index in group[1:]:
            hydrogen = positions[hydrogen_index]
            fig.add_trace(
                go.Scatter3d(
                    x=[oxygen[0], hydrogen[0]],
                    y=[oxygen[1], hydrogen[1]],
                    z=[oxygen[2], hydrogen[2]],
                    mode="lines",
                    line=dict(color="gray", width=2),
                    showlegend=False,
                    hoverinfo="skip",
                ),
                row=1,
                col=col,
            )


def add_vacancy_marker(fig, position):
    """Marca a vacancia na estrutura defeituosa."""
    fig.add_trace(
        go.Scatter3d(
            x=[position[0]],
            y=[position[1]],
            z=[position[2]],
            mode="markers+text",
            marker=dict(
                size=10,
                color="gold",
                symbol="diamond",
                line=dict(color="black", width=2),
            ),
            text=["vacancia"],
            textposition="top center",
            name="Vacancia molecular",
        ),
        row=1,
        col=2,
    )


def main():
    """Gera o relatorio visual final da vacancia."""
    if not PERFECT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {PERFECT_CIF}\n"
            "Execute primeiro: python scripts/10_supercelula_gelo_ih.py"
        )

    if not VACANCY_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {VACANCY_CIF}\n"
            "Execute primeiro: python scripts/11_vacancia_gelo_ih.py"
        )

    FIGURES_DIR.mkdir(exist_ok=True)

    perfect = read(PERFECT_CIF)
    vacancy = read(VACANCY_CIF)
    vacancy_position = estimate_vacancy_position(perfect, vacancy)

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "scene"}, {"type": "scene"}]],
        subplot_titles=[
            "Supercelula sem defeito",
            "Supercelula com vacancia molecular",
        ],
    )

    add_cell(fig, perfect.cell, col=1, name="Celula")
    add_bonds(fig, perfect, col=1)
    add_atoms(fig, perfect, col=1, suffix="sem defeito")

    add_cell(fig, vacancy.cell, col=2, name="Celula com vacancia")
    add_bonds(fig, vacancy, col=2)
    add_atoms(fig, vacancy, col=2, suffix="com vacancia")
    add_vacancy_marker(fig, vacancy_position)

    perfect_molecules = perfect.get_chemical_symbols().count("O")
    vacancy_molecules = vacancy.get_chemical_symbols().count("O")

    fig.update_layout(
        title=(
            "Relatorio visual - vacancia no gelo Ih aproximado"
            f"<br><sup>Sem defeito: {len(perfect)} atomos, "
            f"{perfect_molecules} H2O | Com vacancia: {len(vacancy)} atomos, "
            f"{vacancy_molecules} H2O</sup>"
        ),
        margin=dict(l=0, r=0, b=0, t=80),
        scene=dict(
            xaxis_title="x (A)",
            yaxis_title="y (A)",
            zaxis_title="z (A)",
            aspectmode="data",
        ),
        scene2=dict(
            xaxis_title="x (A)",
            yaxis_title="y (A)",
            zaxis_title="z (A)",
            aspectmode="data",
        ),
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")

    print("=== Relatorio visual final da vacancia ===")
    print(f"Estrutura sem defeito: {PERFECT_CIF}")
    print(f"Estrutura com vacancia: {VACANCY_CIF}")
    print(f"HTML gerado: {OUTPUT_HTML}")
    print(f"Atomos sem defeito: {len(perfect)}")
    print(f"Atomos com vacancia: {len(vacancy)}")
    print(f"Moleculas removidas: {perfect_molecules - vacancy_molecules}")


if __name__ == "__main__":
    main()