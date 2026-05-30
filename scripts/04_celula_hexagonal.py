"""Cria uma celula hexagonal simples usando ASE.

Esta etapa introduz a ideia de celula unitaria: um bloco geometrico definido
por tres vetores de rede. A celula criada aqui ainda nao representa o gelo Ih
real. Ela e um modelo didatico para estudar geometria hexagonal, coordenadas
fracionarias e exportacao de estruturas com celula.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/04_celula_hexagonal.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from ase import Atoms
from ase.geometry import cellpar_to_cell
from ase.io import write


STRUCTURES_DIR = Path("structures")
FIGURES_DIR = Path("figures")

A = 4.5
C = 7.3
ALPHA = 90.0
BETA = 90.0
GAMMA = 120.0


def create_hexagonal_cell():
    """Cria uma estrutura didatica com celula hexagonal."""
    cell = cellpar_to_cell([A, A, C, ALPHA, BETA, GAMMA])

    fractional_positions = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0 / 3.0, 2.0 / 3.0, 0.5],
        ]
    )

    atoms = Atoms(
        symbols=["O", "O"],
        scaled_positions=fractional_positions,
        cell=cell,
        pbc=True,
    )

    return atoms


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
    """Ajusta os eixos 3D para evitar deformacao visual da celula."""
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


def plot_hexagonal_cell(atoms, output_path):
    """Gera uma figura 3D da celula hexagonal."""
    positions = atoms.get_positions()
    cell = atoms.cell

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        s=140,
        color="#d62728",
        edgecolor="black",
        label="Pontos da base",
    )

    for start, end in get_cell_edges(cell):
        xs = [start[0], end[0]]
        ys = [start[1], end[1]]
        zs = [start[2], end[2]]
        ax.plot(xs, ys, zs, color="#1f77b4", linewidth=2.0)

    origin = np.array([0.0, 0.0, 0.0])
    a1, a2, a3 = np.array(cell)
    vectors = [(a1, "a1"), (a2, "a2"), (a3, "a3")]

    for vector, label in vectors:
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            vector[0],
            vector[1],
            vector[2],
            color="black",
            arrow_length_ratio=0.08,
            linewidth=2.0,
        )
        label_position = 1.08 * vector
        ax.text(
            label_position[0],
            label_position[1],
            label_position[2],
            label,
            fontsize=12,
            weight="bold",
        )

    ax.set_title("Celula hexagonal simples")
    ax.set_xlabel("x (Angstrom)")
    ax.set_ylabel("y (Angstrom)")
    ax.set_zlabel("z (Angstrom)")
    ax.view_init(elev=22, azim=35)
    ax.legend(loc="upper left")
    set_axes_equal(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main():
    """Cria, salva e visualiza uma celula hexagonal simples."""
    STRUCTURES_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    atoms = create_hexagonal_cell()

    xyz_output = STRUCTURES_DIR / "celula_hexagonal_simples.xyz"
    cif_output = STRUCTURES_DIR / "celula_hexagonal_simples.cif"
    figure_output = FIGURES_DIR / "celula_hexagonal_simples.png"

    write(xyz_output, atoms)
    write(cif_output, atoms)
    plot_hexagonal_cell(atoms, figure_output)

    print("=== Celula hexagonal simples ===")
    print(f"Parametros: a={A} Angstrom, c={C} Angstrom")
    print(f"Angulos: alpha={ALPHA}, beta={BETA}, gamma={GAMMA}")
    print(f"Numero de atomos da base: {len(atoms)}")
    print(f"PBC: {atoms.pbc}")
    print("\nVetores de rede:")
    print(atoms.cell)
    print("\nCoordenadas fracionarias:")
    print(atoms.get_scaled_positions())
    print("\nArquivos gerados:")
    print(f"- {xyz_output}")
    print(f"- {cif_output}")
    print(f"- {figure_output}")


if __name__ == "__main__":
    main()