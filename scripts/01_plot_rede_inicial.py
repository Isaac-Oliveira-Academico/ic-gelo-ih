from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
DATA = ROOT / "data"

FIGURES.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)


def water_molecule(origin):
    """Return approximate O, H, H coordinates for one water molecule."""
    origin = np.array(origin, dtype=float)

    # Geometria aproximada: O-H ~0.96 A, angulo H-O-H ~104.5 graus.
    oh = 0.96
    angle = np.deg2rad(104.5 / 2)

    oxygen = origin
    h1 = origin + np.array([oh * np.sin(angle), oh * np.cos(angle), 0.0])
    h2 = origin + np.array([-oh * np.sin(angle), oh * np.cos(angle), 0.0])

    return oxygen, h1, h2


def build_hexagonal_network(nx=4, ny=4, spacing=3.0):
    atoms = []
    bonds = []

    for i in range(nx):
        for j in range(ny):
            x = spacing * (i + 0.5 * (j % 2))
            y = spacing * np.sqrt(3) * j / 2
            z = 0.35 * ((i + j) % 2)

            start = len(atoms)
            oxygen, h1, h2 = water_molecule((x, y, z))

            atoms.extend([
                ("O", oxygen),
                ("H", h1),
                ("H", h2),
            ])

            bonds.extend([
                (start, start + 1),
                (start, start + 2),
            ])

    return atoms, bonds


def save_xyz(atoms, path):
    with path.open("w", encoding="utf-8") as f:
        f.write(f"{len(atoms)}\n")
        f.write("Rede inicial simplificada para estudo computacional do gelo Ih\n")
        for symbol, coord in atoms:
            x, y, z = coord
            f.write(f"{symbol} {x:.6f} {y:.6f} {z:.6f}\n")


def plot_network(atoms, bonds, path):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    colors = {"O": "#d62828", "H": "#f4f4f4"}
    edges = {"O": "#7a1111", "H": "#777777"}
    sizes = {"O": 90, "H": 35}

    for symbol in ["O", "H"]:
        coords = np.array([coord for atom_symbol, coord in atoms if atom_symbol == symbol])
        ax.scatter(
            coords[:, 0],
            coords[:, 1],
            coords[:, 2],
            s=sizes[symbol],
            c=colors[symbol],
            edgecolors=edges[symbol],
            linewidths=0.8,
            label=symbol,
        )

    for a, b in bonds:
        p1 = atoms[a][1]
        p2 = atoms[b][1]
        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            color="#555555",
            linewidth=1.0,
            alpha=0.8,
        )

    ax.set_title("Rede molecular inicial inspirada no gelo Ih")
    ax.set_xlabel("x (A)")
    ax.set_ylabel("y (A)")
    ax.set_zlabel("z (A)")
    ax.legend()

    ax.view_init(elev=25, azim=35)
    ax.set_box_aspect((1.3, 1.0, 0.35))

    plt.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    atoms, bonds = build_hexagonal_network()

    xyz_path = DATA / "rede_gelo_inicial.xyz"
    figure_path = FIGURES / "rede_gelo_inicial.png"

    save_xyz(atoms, xyz_path)
    plot_network(atoms, bonds, figure_path)

    print(f"Arquivo XYZ salvo em: {xyz_path}")
    print(f"Figura salva em: {figure_path}")
    print("Observacao: estrutura simplificada, ainda nao e um modelo cristalografico rigoroso do gelo Ih.")


if __name__ == "__main__":
    main()