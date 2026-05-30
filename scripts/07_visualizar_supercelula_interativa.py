"""Gera uma visualizacao 3D interativa da supercelula hexagonal.

O script le a supercelula criada na etapa anterior e produz um arquivo HTML
interativo. Esse arquivo pode ser aberto no navegador para rotacionar, aplicar
zoom e inspecionar o cristal didatico.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/07_visualizar_supercelula_interativa.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase.io import read


INPUT_CIF = Path("structures/supercelula_hexagonal_4x4x2.cif")
FIGURES_DIR = Path("figures")
OUTPUT_HTML = FIGURES_DIR / "supercelula_hexagonal_interativa.html"


def get_cell_edges(cell):
    """Retorna as arestas da celula para desenhar no Plotly."""
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


def add_cell_edges(fig, cell, name, color, width):
    """Adiciona as arestas de uma celula ao grafico."""
    first_edge = True

    for start, end in get_cell_edges(cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color=color, width=width),
                name=name if first_edge else None,
                showlegend=first_edge,
                hoverinfo="skip",
            )
        )
        first_edge = False


def add_lattice_vectors(fig, cell):
    """Adiciona os vetores da supercelula."""
    origin = np.array([0.0, 0.0, 0.0])
    vectors = [
        (np.array(cell)[0], "A1"),
        (np.array(cell)[1], "A2"),
        (np.array(cell)[2], "A3"),
    ]

    for vector, label in vectors:
        fig.add_trace(
            go.Scatter3d(
                x=[origin[0], vector[0]],
                y=[origin[1], vector[1]],
                z=[origin[2], vector[2]],
                mode="lines+text",
                line=dict(color="black", width=7),
                text=["", label],
                textposition="top center",
                name=label,
            )
        )


def main():
    """Le a supercelula e cria uma visualizacao HTML interativa."""
    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_CIF}\n"
            "Execute primeiro: python scripts/06_supercelula_hexagonal.py"
        )

    FIGURES_DIR.mkdir(exist_ok=True)

    atoms = read(INPUT_CIF)
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],
            mode="markers",
            marker=dict(
                size=5,
                color=positions[:, 2],
                colorscale="Viridis",
                line=dict(color="black", width=0.5),
                colorbar=dict(title="z (A)"),
            ),
            text=[
                f"{symbol}{index}<br>"
                f"x={position[0]:.3f} A<br>"
                f"y={position[1]:.3f} A<br>"
                f"z={position[2]:.3f} A"
                for index, (symbol, position) in enumerate(zip(symbols, positions))
            ],
            hoverinfo="text",
            name="Pontos repetidos",
        )
    )

    add_cell_edges(
        fig,
        atoms.cell,
        name="Caixa da supercelula",
        color="royalblue",
        width=5,
    )
    add_lattice_vectors(fig, atoms.cell)

    fig.update_layout(
        title="Supercelula hexagonal 4x4x2 - visualizacao interativa",
        scene=dict(
            xaxis_title="x (Angstrom)",
            yaxis_title="y (Angstrom)",
            zaxis_title="z (Angstrom)",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=45),
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")

    print("=== Visualizacao interativa da supercelula hexagonal ===")
    print(f"Arquivo de entrada: {INPUT_CIF}")
    print(f"Numero de atomos: {len(atoms)}")
    print(f"PBC: {atoms.pbc}")
    print(f"Arquivo HTML gerado: {OUTPUT_HTML}")
    print("\nAbra esse HTML no navegador para rotacionar e aplicar zoom com o mouse.")


if __name__ == "__main__":
    main()