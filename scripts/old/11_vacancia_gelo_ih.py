"""Cria uma vacancia molecular no gelo Ih aproximado.

O script remove uma molecula H2O da supercelula gerada na etapa 10. A molecula
removida e escolhida como a mais proxima do centro geometrico da supercelula,
criando uma vacancia em uma regiao interna do cristal didatico.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/11_vacancia_gelo_ih.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase.io import read, write


INPUT_CIF = Path("structures/supercelula_gelo_ih_3x3x2.cif")
STRUCTURES_DIR = Path("structures")
FIGURES_DIR = Path("figures")

OUTPUT_XYZ = STRUCTURES_DIR / "gelo_ih_vacancia.xyz"
OUTPUT_CIF = STRUCTURES_DIR / "gelo_ih_vacancia.cif"
OUTPUT_HTML = FIGURES_DIR / "gelo_ih_vacancia_interativa.html"


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


def molecule_indices(atoms):
    """Retorna grupos de indices assumindo ordem O, H, H para cada molecula."""
    groups = []

    for oxygen_index in range(0, len(atoms), 3):
        group = [oxygen_index, oxygen_index + 1, oxygen_index + 2]
        symbols = [atoms[index].symbol for index in group]

        if symbols != ["O", "H", "H"]:
            raise ValueError(
                "A estrutura nao esta na ordem molecular esperada O, H, H."
            )

        groups.append(group)

    return groups


def choose_central_molecule(atoms):
    """Escolhe a molecula cujo oxigenio esta mais proximo do centro da celula."""
    positions = atoms.get_positions()
    center = 0.5 * np.sum(np.array(atoms.cell), axis=0)

    best_group = None
    best_distance = None

    for group in molecule_indices(atoms):
        oxygen_position = positions[group[0]]
        distance = np.linalg.norm(oxygen_position - center)

        if best_distance is None or distance < best_distance:
            best_group = group
            best_distance = distance

    return best_group, center, best_distance



    defective = atoms.copy()
    del defective[group]
    return defective

def remove_molecule(atoms, group):
    """Remove uma molecula H2O da estrutura."""
    defective = atoms.copy()
    del defective[group]
    return defective

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
    """Desenha ligacoes O-H assumindo a ordem O, H, H."""
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
    """Adiciona atomos restantes, coloridos por elemento."""
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


def add_vacancy_marker(fig, removed_positions):
    """Marca a posicao da molecula removida."""
    vacancy_center = removed_positions.mean(axis=0)

    fig.add_trace(
        go.Scatter3d(
            x=[vacancy_center[0]],
            y=[vacancy_center[1]],
            z=[vacancy_center[2]],
            mode="markers+text",
            marker=dict(
                size=12,
                color="gold",
                symbol="diamond",
                line=dict(color="black", width=2),
            ),
            text=["vacancia"],
            textposition="top center",
            name="Vacancia",
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=removed_positions[:, 0],
            y=removed_positions[:, 1],
            z=removed_positions[:, 2],
            mode="markers",
            marker=dict(
                size=[7, 5, 5],
                color=["rgba(255,0,0,0.25)", "rgba(255,255,255,0.25)", "rgba(255,255,255,0.25)"],
                line=dict(color="black", width=1),
            ),
            name="Molecula removida",
            hoverinfo="skip",
        )
    )


def create_interactive_view(defective, removed_positions):
    """Gera HTML interativo destacando a vacancia."""
    fig = go.Figure()
    add_cell_edges(fig, defective.cell)
    add_bonds(fig, defective)
    add_atoms(fig, defective)
    add_vacancy_marker(fig, removed_positions)

    fig.update_layout(
        title="Vacancia molecular no gelo Ih aproximado",
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
    """Cria uma vacancia molecular e salva os resultados."""
    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_CIF}\n"
            "Execute primeiro: python scripts/10_supercelula_gelo_ih.py"
        )

    STRUCTURES_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    atoms = read(INPUT_CIF)
    group, center, distance = choose_central_molecule(atoms)
    removed_positions = atoms.get_positions()[group]
    defective = remove_molecule(atoms, group)

    write(OUTPUT_XYZ, defective)
    write(OUTPUT_CIF, defective)
    create_interactive_view(defective, removed_positions)

    original_symbols = atoms.get_chemical_symbols()
    defective_symbols = defective.get_chemical_symbols()

    print("=== Vacancia molecular no gelo Ih aproximado ===")
    print(f"Arquivo de entrada: {INPUT_CIF}")
    print(f"Atomos antes: {len(atoms)}")
    print(f"Atomos depois: {len(defective)}")
    print(f"Oxigenios antes: {original_symbols.count('O')}")
    print(f"Oxigenios depois: {defective_symbols.count('O')}")
    print(f"Hidrogenios antes: {original_symbols.count('H')}")
    print(f"Hidrogenios depois: {defective_symbols.count('H')}")
    print(f"Molecula removida, indices originais: {group}")
    print(f"Centro da supercelula: {center}")
    print(f"Distancia da molecula removida ao centro: {distance:.4f} Angstrom")
    print(f"PBC: {defective.pbc}")
    print("\nArquivos gerados:")
    print(f"- {OUTPUT_XYZ}")
    print(f"- {OUTPUT_CIF}")
    print(f"- {OUTPUT_HTML}")


if __name__ == "__main__":
    main()