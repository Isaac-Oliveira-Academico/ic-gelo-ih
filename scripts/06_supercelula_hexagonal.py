"""Gera uma supercelula a partir da celula hexagonal simples.

Uma supercelula e criada repetindo a celula unitaria nas direcoes dos vetores
de rede. Essa etapa mostra como uma estrutura pequena pode representar um
cristal maior mantendo a periodicidade.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/06_supercelula_hexagonal.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from ase.io import read, write


INPUT_CIF = Path("structures/celula_hexagonal_simples.cif")
STRUCTURES_DIR = Path("structures")
FIGURES_DIR = Path("figures")

REPETITIONS = (4, 4, 2)


def get_cell_edges(cell):
    """Retorna as arestas da celula para desenho em 3D."""
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


def set_axes_equal(ax):
    """Mantem proporcao igual nos eixos 3D."""
    limits = np.array(
        [
            ax.get_xlim3d(),
            ax.get_ylim3d(),
            ax.get_zlim3d(),
        ]
    )
    centers = limits.mean(axis=1)
    radius = 0.5 * max(limits[:, 1] - limits[:, 0])

    ax.set_xlim3d([centers[0] - radius, centers[0] + radius])
    ax.set_ylim3d([centers[1] - radius, centers[1] + radius])
    ax.set_zlim3d([centers[2] - radius, centers[2] + radius])


def plot_supercell(unit_cell, supercell, output_path):
    """Gera uma figura 3D da supercelula."""
    positions = supercell.get_positions()

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        s=45,
        color="#d62728",
        edgecolor="black",
        linewidth=0.5,
        label="Pontos repetidos",
    )

    for start, end in get_cell_edges(supercell.cell):
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            color="#1f77b4",
            linewidth=2.2,
        )

    for start, end in get_cell_edges(unit_cell.cell):
        ax.plot(
            [start[0], end[0]],
            [start[1], end[1]],
            [start[2], end[2]],
            color="black",
            linestyle="--",
            linewidth=1.4,
        )

    ax.set_title(f"Supercelula hexagonal {REPETITIONS[0]}x{REPETITIONS[1]}x{REPETITIONS[2]}")
    ax.set_xlabel("x (Angstrom)")
    ax.set_ylabel("y (Angstrom)")
    ax.set_zlabel("z (Angstrom)")
    ax.legend(loc="upper left")
    ax.view_init(elev=24, azim=35)
    set_axes_equal(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main():
    """Cria e salva uma supercelula hexagonal."""
    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_CIF}\n"
            "Execute primeiro: python scripts/04_celula_hexagonal.py"
        )

    STRUCTURES_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    unit_cell = read(INPUT_CIF)
    supercell = unit_cell.repeat(REPETITIONS)

    xyz_output = STRUCTURES_DIR / "supercelula_hexagonal_4x4x2.xyz"
    cif_output = STRUCTURES_DIR / "supercelula_hexagonal_4x4x2.cif"
    figure_output = FIGURES_DIR / "supercelula_hexagonal_4x4x2.png"

    write(xyz_output, supercell)
    write(cif_output, supercell)
    plot_supercell(unit_cell, supercell, figure_output)

    print("=== Supercelula hexagonal ===")
    print(f"Arquivo de entrada: {INPUT_CIF}")
    print(f"Repeticoes: {REPETITIONS}")
    print(f"Atomos na celula unitaria: {len(unit_cell)}")
    print(f"Atomos na supercelula: {len(supercell)}")
    print(f"PBC: {supercell.pbc}")
    print("\nCelula original:")
    print(unit_cell.cell)
    print("\nCelula da supercelula:")
    print(supercell.cell)
    print("\nArquivos gerados:")
    print(f"- {xyz_output}")
    print(f"- {cif_output}")
    print(f"- {figure_output}")


if __name__ == "__main__":
    main()