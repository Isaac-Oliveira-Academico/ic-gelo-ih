"""Cria uma animacao de condicoes periodicas de contorno.

Este script mostra um ponto se movendo na direcao do vetor de rede a1. Quando
a coordenada fracionaria passa de 1.0, o ponto reaparece no lado equivalente da
celula. A visualizacao e salva como HTML interativo com botao de play.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/08b_animacao_pbc.py
"""

from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from ase.io import read


INPUT_CIF = Path("structures/celula_hexagonal_simples.cif")
FIGURES_DIR = Path("figures")
OUTPUT_HTML = FIGURES_DIR / "animacao_pbc.html"

FIXED_FRACTIONAL_Y = 0.35
FIXED_FRACTIONAL_Z = 0.50
START_FRACTIONAL_X = 0.75
END_FRACTIONAL_X = 1.25
N_FRAMES = 41


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


def fractional_to_cartesian(fractional_position, cell):
    """Converte coordenadas fracionarias em coordenadas cartesianas."""
    return np.array(fractional_position) @ np.array(cell)


def make_particle_trace(position, label, color):
    """Cria o marcador do ponto em uma posicao cartesiana."""
    return go.Scatter3d(
        x=[position[0]],
        y=[position[1]],
        z=[position[2]],
        mode="markers+text",
        marker=dict(size=10, color=color, line=dict(color="black", width=1)),
        text=[label],
        textposition="top center",
        name=label,
    )


def add_static_cell(fig, atoms):
    """Adiciona celula e pontos da base ao grafico."""
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()

    fig.add_trace(
        go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],
            mode="markers+text",
            marker=dict(size=6, color="red", line=dict(color="black", width=1)),
            text=[f"{symbol}{index}" for index, symbol in enumerate(symbols)],
            textposition="top center",
            name="Base da celula",
        )
    )

    first_edge = True
    for start, end in get_cell_edges(atoms.cell):
        fig.add_trace(
            go.Scatter3d(
                x=[start[0], end[0]],
                y=[start[1], end[1]],
                z=[start[2], end[2]],
                mode="lines",
                line=dict(color="royalblue", width=5),
                name="Celula" if first_edge else None,
                showlegend=first_edge,
                hoverinfo="skip",
            )
        )
        first_edge = False


def build_frames(cell):
    """Cria os quadros da animacao."""
    frames = []
    fractional_x_values = np.linspace(
        START_FRACTIONAL_X,
        END_FRACTIONAL_X,
        N_FRAMES,
    )

    for frame_index, fractional_x in enumerate(fractional_x_values):
        unwrapped_fractional = np.array(
            [fractional_x, FIXED_FRACTIONAL_Y, FIXED_FRACTIONAL_Z]
        )
        wrapped_fractional = unwrapped_fractional % 1.0

        unwrapped_cartesian = fractional_to_cartesian(unwrapped_fractional, cell)
        wrapped_cartesian = fractional_to_cartesian(wrapped_fractional, cell)

        frame = go.Frame(
            name=str(frame_index),
            data=[
                make_particle_trace(
                    unwrapped_cartesian,
                    "trajetoria sem PBC",
                    "orange",
                ),
                make_particle_trace(
                    wrapped_cartesian,
                    "posicao com PBC",
                    "limegreen",
                ),
            ],
            traces=[13, 14],
            layout=go.Layout(
                annotations=[
                    dict(
                        text=(
                            "Coordenada fracionaria em a1: "
                            f"{fractional_x:.2f} -> {wrapped_fractional[0]:.2f}"
                        ),
                        x=0.02,
                        y=0.95,
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=14),
                    )
                ]
            ),
        )
        frames.append(frame)

    return frames


def main():
    """Gera a animacao HTML de PBC."""
    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_CIF}\n"
            "Execute primeiro: python scripts/04_celula_hexagonal.py"
        )

    FIGURES_DIR.mkdir(exist_ok=True)

    atoms = read(INPUT_CIF)
    atoms.set_pbc(True)
    cell = atoms.cell

    initial_unwrapped_fractional = np.array(
        [START_FRACTIONAL_X, FIXED_FRACTIONAL_Y, FIXED_FRACTIONAL_Z]
    )
    initial_wrapped_fractional = initial_unwrapped_fractional % 1.0

    initial_unwrapped_cartesian = fractional_to_cartesian(
        initial_unwrapped_fractional,
        cell,
    )
    initial_wrapped_cartesian = fractional_to_cartesian(
        initial_wrapped_fractional,
        cell,
    )

    fig = go.Figure()
    add_static_cell(fig, atoms)

    fig.add_trace(
        make_particle_trace(
            initial_unwrapped_cartesian,
            "trajetoria sem PBC",
            "orange",
        )
    )
    fig.add_trace(
        make_particle_trace(
            initial_wrapped_cartesian,
            "posicao com PBC",
            "limegreen",
        )
    )

    fig.frames = build_frames(cell)

    fig.update_layout(
        title="Animacao de condicoes periodicas de contorno",
        scene=dict(
            xaxis_title="x (Angstrom)",
            yaxis_title="y (Angstrom)",
            zaxis_title="z (Angstrom)",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, b=0, t=45),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.02,
                y=0.02,
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=120, redraw=True),
                                fromcurrent=True,
                                transition=dict(duration=0),
                            ),
                        ],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=False),
                                mode="immediate",
                                transition=dict(duration=0),
                            ),
                        ],
                    ),
                ],
            )
        ],
        sliders=[
            dict(
                steps=[
                    dict(
                        method="animate",
                        args=[
                            [str(index)],
                            dict(
                                mode="immediate",
                                frame=dict(duration=0, redraw=True),
                                transition=dict(duration=0),
                            ),
                        ],
                        label=str(index),
                    )
                    for index in range(N_FRAMES)
                ],
                x=0.12,
                y=0.02,
                len=0.75,
            )
        ],
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")

    print("=== Animacao de PBC ===")
    print(f"Arquivo de entrada: {INPUT_CIF}")
    print(f"Arquivo HTML gerado: {OUTPUT_HTML}")
    print("A particula verde mostra a posicao com PBC.")
    print("A particula laranja mostra onde ela estaria sem aplicar PBC.")
    print("Quando s passa de 1.0, a posicao verde reaparece perto de 0.0.")


if __name__ == "__main__":
    main()
