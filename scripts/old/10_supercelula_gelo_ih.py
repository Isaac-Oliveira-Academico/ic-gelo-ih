"""Gera uma supercelula do modelo aproximado de gelo Ih.

Este script repete a celula molecular aproximada criada na etapa 09. O objetivo
e produzir um cristal molecular maior, adequado para visualizacao e para a
proxima etapa: introducao de uma vacancia.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/10_supercelula_gelo_ih.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase.io import read, write


INPUT_CIF = Path("structures/gelo_ih_aproximado.cif")
STRUCTURES_DIR = Path("structures")
FIGURES_DIR = Path("figures")

REPETITIONS = (3, 3, 2)

OUTPUT_XYZ = STRUCTURES_DIR / "supercelula_gelo_ih_3x3x2.xyz"
OUTPUT_CIF = STRUCTURES_DIR / "supercelula_gelo_ih_3x3x2.cif"
OUTPUT_HTML = FIGURES_DIR / "supercelula_gelo_ih_3x3x2_interativa.html"


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


def add_cell_edges(fig, cell):
    """Adiciona a caixa da supercelula ao grafico."""
    first_edge = True

    for start, end in get_cell_edges(cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color="royalblue", width=5),
                name="Supercelula" if first_edge else None,
                showlegend=first_edge,
                hoverinfo="skip",
            )
        )
        first_edge = False


def add_bonds(fig, atoms):
    """Desenha ligacoes O-H assumindo a ordem O, H, H para cada molecula."""
    positions = atoms.get_positions()

    for oxygen_index in range(0, len(atoms), 3):
        oxygen = positions[oxygen_index]

        for hydrogen_index in [oxygen_index + 1, oxygen_index + 2]:
            hydrogen = positions[hydrogen_index]
            fig.add_trace(
                go.Scatter3d(
                    x=[oxygen[0], hydrogen[0]],
                    y=[oxygen[1], hydrogen[1]],
                    z=[oxygen[2], hydrogen[2]],
                    mode="lines",
                    line=dict(color="gray", width=3),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )


def add_atoms(fig, atoms):
    """Adiciona atomos da supercelula, coloridos por elemento."""
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()

    styles = {
        "O": {"color": "red", "size": 5},
        "H": {"color": "white", "size": 3},
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
                    line=dict(color="black", width=0.5),
                ),
                text=[
                    f"{element}{index}<br>"
                    f"x={positions[index, 0]:.3f} A<br>"
                    f"y={positions[index, 1]:.3f} A<br>"
                    f"z={positions[index, 2]:.3f} A"
                    for index in indices
                ],
                hoverinfo="text",
                name=element,
            )
        )


def create_interactive_view(atoms):
    """Gera HTML interativo da supercelula."""
    fig = go.Figure()
    add_cell_edges(fig, atoms.cell)
    add_bonds(fig, atoms)
    add_atoms(fig, atoms)

    fig.update_layout(
        title="Supercelula do gelo Ih aproximado 3x3x2",
        scene=dict(
            xaxis_title="x (Angstrom)",
            yaxis_title="y (Angstrom)",
            zaxis_title="z (Angstrom)",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=45),
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")


def main():
    """Cria a supercelula do gelo Ih aproximado."""
    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_CIF}\n"
            "Execute primeiro: python scripts/09_gelo_ih_aproximado.py"
        )

    STRUCTURES_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    unit_cell = read(INPUT_CIF)
    supercell = unit_cell.repeat(REPETITIONS)

    write(OUTPUT_XYZ, supercell)
    write(OUTPUT_CIF, supercell)
    create_interactive_view(supercell)

    symbols = supercell.get_chemical_symbols()
    oxygen_count = symbols.count("O")
    hydrogen_count = symbols.count("H")

    print("=== Supercelula do gelo Ih aproximado ===")
    print(f"Arquivo de entrada: {INPUT_CIF}")
    print(f"Repeticoes: {REPETITIONS}")
    print(f"Atomos na celula aproximada: {len(unit_cell)}")
    print(f"Atomos na supercelula: {len(supercell)}")
    print(f"Oxigenios: {oxygen_count}")
    print(f"Hidrogenios: {hydrogen_count}")
    print(f"Moleculas H2O: {oxygen_count}")
    print(f"PBC: {supercell.pbc}")
    print("\nArquivos gerados:")
    print(f"- {OUTPUT_XYZ}")
    print(f"- {OUTPUT_CIF}")
    print(f"- {OUTPUT_HTML}")


if __name__ == "__main__":
    main()