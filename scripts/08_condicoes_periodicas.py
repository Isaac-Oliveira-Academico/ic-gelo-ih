"""Demonstra condicoes periodicas de contorno em uma celula hexagonal.

Em sistemas periodicos, um ponto que sai por uma face da celula reaparece pela
face oposta. Essa ideia e essencial para simular cristais usando uma caixa finita
como representacao de um material extenso.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/08_condicoes_periodicas.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase.io import read, write


INPUT_CIF = Path("structures/celula_hexagonal_simples.cif")
STRUCTURES_DIR = Path("structures")
FIGURES_DIR = Path("figures")
OUTPUT_CIF = STRUCTURES_DIR / "celula_hexagonal_pbc.cif"
OUTPUT_HTML = FIGURES_DIR / "condicoes_periodicas.html"


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


def add_cell_edges(fig, cell, color="royalblue"):
    """Adiciona a caixa da celula ao grafico."""
    first_edge = True

    for start, end in get_cell_edges(cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color=color, width=5),
                name="Celula periodica" if first_edge else None,
                showlegend=first_edge,
                hoverinfo="skip",
            )
        )
        first_edge = False


def add_periodic_images(fig, atoms):
    """Desenha copias periodicas dos pontos em celulas vizinhas."""
    base_positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()
    a1, a2, _ = np.array(atoms.cell)

    shifts = [
        np.array([0.0, 0.0, 0.0]),
        a1,
        -a1,
        a2,
        -a2,
        a1 + a2,
        -a1 - a2,
    ]

    for shift_index, shift in enumerate(shifts):
        shifted = base_positions + shift
        is_original = shift_index == 0

        fig.add_trace(
            go.Scatter3d(
                x=shifted[:, 0],
                y=shifted[:, 1],
                z=shifted[:, 2],
                mode="markers+text" if is_original else "markers",
                marker=dict(
                    size=8 if is_original else 5,
                    color="red" if is_original else "lightgray",
                    line=dict(color="black", width=1),
                    opacity=1.0 if is_original else 0.45,
                ),
                text=[
                    f"{symbol}{index}" for index, symbol in enumerate(symbols)
                ]
                if is_original
                else None,
                textposition="top center",
                name="Celula original" if is_original else "Imagens periodicas",
                showlegend=shift_index <= 1,
            )
        )


def add_boundary_example(fig, atoms):
    """Mostra um ponto atravessando uma fronteira periodica."""
    cell = np.array(atoms.cell)

    start_scaled = np.array([0.92, 0.28, 0.50])
    end_scaled_outside = np.array([1.12, 0.28, 0.50])
    wrapped_scaled = end_scaled_outside % 1.0

    start_cart = start_scaled @ cell
    end_cart = end_scaled_outside @ cell
    wrapped_cart = wrapped_scaled @ cell

    fig.add_trace(
        go.Scatter3d(
            x=[start_cart[0], end_cart[0]],
            y=[start_cart[1], end_cart[1]],
            z=[start_cart[2], end_cart[2]],
            mode="lines+markers",
            line=dict(color="orange", width=8),
            marker=dict(size=6, color="orange"),
            name="Saida pela fronteira",
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=[wrapped_cart[0]],
            y=[wrapped_cart[1]],
            z=[wrapped_cart[2]],
            mode="markers+text",
            marker=dict(size=9, color="limegreen", line=dict(color="black", width=1)),
            text=["reentrada"],
            textposition="top center",
            name="Reentrada periodica",
        )
    )

    return start_scaled, end_scaled_outside, wrapped_scaled


def main():
    """Cria a demonstracao de PBC e salva estrutura/visualizacao."""
    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_CIF}\n"
            "Execute primeiro: python scripts/04_celula_hexagonal.py"
        )

    STRUCTURES_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    atoms = read(INPUT_CIF)
    atoms.set_pbc(True)
    write(OUTPUT_CIF, atoms)

    fig = go.Figure()
    add_cell_edges(fig, atoms.cell)
    add_periodic_images(fig, atoms)
    start_scaled, end_scaled_outside, wrapped_scaled = add_boundary_example(fig, atoms)

    fig.update_layout(
        title="Condicoes periodicas de contorno - celula hexagonal",
        scene=dict(
            xaxis_title="x (Angstrom)",
            yaxis_title="y (Angstrom)",
            zaxis_title="z (Angstrom)",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=45),
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")

    print("=== Condicoes periodicas de contorno ===")
    print(f"Arquivo de entrada: {INPUT_CIF}")
    print(f"Arquivo CIF com PBC: {OUTPUT_CIF}")
    print(f"Arquivo HTML gerado: {OUTPUT_HTML}")
    print(f"PBC: {atoms.pbc}")
    print("\nExemplo em coordenadas fracionarias:")
    print(f"Posicao inicial: {start_scaled}")
    print(f"Posicao apos cruzar a fronteira: {end_scaled_outside}")
    print(f"Posicao equivalente dentro da celula: {wrapped_scaled}")
    print("\nInterpretacao: 1.12 na direcao a1 equivale a 0.12 dentro da celula.")


if __name__ == "__main__":
    main()