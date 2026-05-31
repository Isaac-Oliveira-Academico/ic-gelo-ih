"""Gera uma visualizacao 3D interativa da celula hexagonal.

Este script evita depender de janela grafica remota no G7Node. Em vez disso,
ele cria um arquivo HTML interativo que pode ser aberto no navegador. Assim e
possivel rotacionar, aplicar zoom e inspecionar a celula com o mouse.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/05_visualizar_celula_hexagonal.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase.io import read


INPUT_CIF = Path("structures/celula_hexagonal_simples.cif")
FIGURES_DIR = Path("figures")
OUTPUT_HTML = FIGURES_DIR / "celula_hexagonal_interativa.html"


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


def add_cell_edges(fig, cell):
    """Adiciona as arestas da celula ao grafico."""
    for start, end in get_cell_edges(cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color="royalblue", width=6),
                showlegend=False,
                hoverinfo="skip",
            )
        )


def add_lattice_vectors(fig, cell):
    """Adiciona vetores de rede como linhas destacadas."""
    origin = np.array([0.0, 0.0, 0.0])
    vectors = [
        (np.array(cell)[0], "a1"),
        (np.array(cell)[1], "a2"),
        (np.array(cell)[2], "a3"),
    ]

    for vector, label in vectors:
        fig.add_trace(
            go.Scatter3d(
                x=[origin[0], vector[0]],
                y=[origin[1], vector[1]],
                z=[origin[2], vector[2]],
                mode="lines+text",
                line=dict(color="black", width=8),
                text=["", label],
                textposition="top center",
                name=label,
            )
        )


"""Gera uma visualizacao 3D interativa da celula hexagonal.

Este script evita depender de janela grafica remota no G7Node. Em vez disso,
ele cria um arquivo HTML interativo que pode ser aberto no navegador. Assim e
possivel rotacionar, aplicar zoom e inspecionar a celula com o mouse.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/05_visualizar_celula_hexagonal.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase.io import read


INPUT_CIF = Path("structures/celula_hexagonal_simples.cif")
FIGURES_DIR = Path("figures")
OUTPUT_HTML = FIGURES_DIR / "celula_hexagonal_interativa.html"


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


def add_cell_edges(fig, cell):
    """Adiciona as arestas da celula ao grafico."""
    for start, end in get_cell_edges(cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color="royalblue", width=6),
                showlegend=False,
                hoverinfo="skip",
            )
        )


def add_lattice_vectors(fig, cell):
    """Adiciona vetores de rede como linhas destacadas."""
    origin = np.array([0.0, 0.0, 0.0])
    vectors = [
        (np.array(cell)[0], "a1"),
        (np.array(cell)[1], "a2"),
        (np.array(cell)[2], "a3"),
    ]

    for vector, label in vectors:
        fig.add_trace(
            go.Scatter3d(
                x=[origin[0], vector[0]],
                y=[origin[1], vector[1]],
                z=[origin[2], vector[2]],
                mode="lines+text",
                line=dict(color="black", width=8),
                text=["", label],
                textposition="top center",
                name=label,
            )
        )


def main():
    """Le a celula hexagonal e cria um HTML interativo."""
    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_CIF}\n"
            "Execute primeiro: python scripts/04_celula_hexagonal.py"
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
            mode="markers+text",
            marker=dict(size=8, color="red", line=dict(color="black", width=2)),
            text=[f"{symbol}{index}" for index, symbol in enumerate(symbols)],
            textposition="top center",
            name="Pontos da base",
        )
    )

    add_cell_edges(fig, atoms.cell)
    add_lattice_vectors(fig, atoms.cell)

    fig.update_layout(
        title="Celula hexagonal simples - visualizacao interativa",
        scene=dict(
            xaxis_title="x (Angstrom)",
            yaxis_title="y (Angstrom)",
            zaxis_title="z (Angstrom)",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=45),
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")

    print("=== Visualizacao interativa da celula hexagonal ===")
    print(f"Arquivo de entrada: {INPUT_CIF}")
    print(f"Arquivo HTML gerado: {OUTPUT_HTML}")
    print("\nAbra esse HTML no navegador para rotacionar e aplicar zoom com o mouse.")


if __name__ == "__main__":
    main()