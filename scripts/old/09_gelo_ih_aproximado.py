"""Gera uma estrutura aproximada e didatica do gelo Ih.

Este modelo coloca moleculas de agua em uma celula hexagonal simples. Ele nao
e uma estrutura cristalografica rigorosa do gelo Ih. O objetivo e conectar os
conceitos ja estudados: molecula H2O, celula hexagonal, coordenadas
fracionarias, periodicidade e visualizacao interativa.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/09_gelo_ih_aproximado.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase import Atoms
from ase.geometry import cellpar_to_cell
from ase.io import write


STRUCTURES_DIR = Path("structures")
FIGURES_DIR = Path("figures")

OUTPUT_XYZ = STRUCTURES_DIR / "gelo_ih_aproximado.xyz"
OUTPUT_CIF = STRUCTURES_DIR / "gelo_ih_aproximado.cif"
OUTPUT_HTML = FIGURES_DIR / "gelo_ih_aproximado_interativo.html"

A = 7.8
C = 7.3
ALPHA = 90.0
BETA = 90.0
GAMMA = 120.0

OH_DISTANCE = 0.96
HOH_ANGLE_DEGREES = 104.5


def water_geometry(orientation_angle_degrees=0.0):
    """Retorna deslocamentos O-H para uma molecula H2O no plano xy."""
    half_angle = np.radians(HOH_ANGLE_DEGREES / 2.0)
    orientation = np.radians(orientation_angle_degrees)

    h1 = OH_DISTANCE * np.array(
        [
            np.cos(orientation + half_angle),
            np.sin(orientation + half_angle),
            0.0,
        ]
    )
    h2 = OH_DISTANCE * np.array(
        [
            np.cos(orientation - half_angle),
            np.sin(orientation - half_angle),
            0.0,
        ]
    )

    return h1, h2


def fractional_to_cartesian(fractional_position, cell):
    """Converte coordenada fracionaria para coordenada cartesiana."""
    return np.array(fractional_position) @ np.array(cell)


def create_approximate_ice_ih():
    """Cria uma estrutura molecular aproximada inspirada no gelo Ih."""
    cell = cellpar_to_cell([A, A, C, ALPHA, BETA, GAMMA])

    oxygen_fractional_positions = [
        [0.00, 0.00, 0.00],
        [1.0 / 3.0, 2.0 / 3.0, 0.25],
        [2.0 / 3.0, 1.0 / 3.0, 0.50],
        [0.00, 0.00, 0.75],
    ]
    orientation_angles = [20.0, 110.0, 200.0, 290.0]

    symbols = []
    positions = []

    for oxygen_fractional, angle in zip(oxygen_fractional_positions, orientation_angles):
        oxygen_position = fractional_to_cartesian(oxygen_fractional, cell)
        h1_offset, h2_offset = water_geometry(angle)

        symbols.extend(["O", "H", "H"])
        positions.extend(
            [
                oxygen_position,
                oxygen_position + h1_offset,
                oxygen_position + h2_offset,
            ]
        )

    atoms = Atoms(symbols=symbols, positions=positions, cell=cell, pbc=True)
    atoms.wrap()

    return atoms


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
    """Adiciona a celula ao grafico interativo."""
    first_edge = True

    for start, end in get_cell_edges(cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color="royalblue", width=5),
                name="Celula hexagonal" if first_edge else None,
                showlegend=first_edge,
                hoverinfo="skip",
            )
        )
        first_edge = False


def add_water_bonds(fig, atoms):
    """Desenha ligacoes O-H dentro de cada molecula."""
    positions = atoms.get_positions()

    for oxygen_index in range(0, len(atoms), 3):
        oxygen = positions[oxygen_index]
        hydrogens = [positions[oxygen_index + 1], positions[oxygen_index + 2]]

        for hydrogen in hydrogens:
            fig.add_trace(
                go.Scatter3d(
                    x=[oxygen[0], hydrogen[0]],
                    y=[oxygen[1], hydrogen[1]],
                    z=[oxygen[2], hydrogen[2]],
                    mode="lines",
                    line=dict(color="gray", width=5),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )


def add_atoms(fig, atoms):
    """Adiciona atomos coloridos por elemento quimico."""
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()

    element_styles = {
        "O": {"color": "red", "size": 8},
        "H": {"color": "white", "size": 5},
    }

    for element in ["O", "H"]:
        indices = [index for index, symbol in enumerate(symbols) if symbol == element]
        element_positions = positions[indices]
        style = element_styles[element]

        fig.add_trace(
            go.Scatter3d(
                x=element_positions[:, 0],
                y=element_positions[:, 1],
                z=element_positions[:, 2],
                mode="markers+text",
                marker=dict(
                    size=style["size"],
                    color=style["color"],
                    line=dict(color="black", width=1),
                ),
                text=[f"{element}{index}" for index in indices],
                textposition="top center",
                name=element,
            )
        )


def create_interactive_view(atoms):
    """Cria visualizacao HTML interativa da estrutura aproximada."""
    fig = go.Figure()
    add_cell_edges(fig, atoms.cell)
    add_water_bonds(fig, atoms)
    add_atoms(fig, atoms)

    fig.update_layout(
        title="Gelo Ih aproximado - modelo didatico",
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
    """Gera estrutura, arquivos e visualizacao do gelo Ih aproximado."""
    STRUCTURES_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    atoms = create_approximate_ice_ih()
    write(OUTPUT_XYZ, atoms)
    write(OUTPUT_CIF, atoms)
    create_interactive_view(atoms)

    symbols = atoms.get_chemical_symbols()
    oxygen_count = symbols.count("O")
    hydrogen_count = symbols.count("H")

    print("=== Gelo Ih aproximado ===")
    print("Modelo didatico, ainda nao cristalografico rigoroso.")
    print(f"Parametros: a={A} Angstrom, c={C} Angstrom, gamma={GAMMA} graus")
    print(f"Numero total de atomos: {len(atoms)}")
    print(f"Oxigenios: {oxygen_count}")
    print(f"Hidrogenios: {hydrogen_count}")
    print(f"Moleculas H2O: {oxygen_count}")
    print(f"PBC: {atoms.pbc}")
    print("\nArquivos gerados:")
    print(f"- {OUTPUT_XYZ}")
    print(f"- {OUTPUT_CIF}")
    print(f"- {OUTPUT_HTML}")


if __name__ == "__main__":
    main()