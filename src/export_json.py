"""Exporta dados cristalograficos como JSON estruturado para o visualizador web.

Esta etapa separa a logica de fisica computacional da logica de visualizacao.
O Python conhece fisica (ASE, coordenadas, defeitos). O HTML conhece tela.
O JSON e a ponte entre os dois.

Execucao:
    python scripts/export_json.py

Saida:
    figures/crystal_data.json
"""

from pathlib import Path
import json
import numpy as np
from ase.io import read


# ── Caminhos ──────────────────────────────────────────────────────────────────
PERFECT_CIF  = Path("structures/supercelula_gelo_ih_3x3x2.cif")
VACANCY_CIF  = Path("structures/gelo_ih_vacancia.cif")
FIGURES_DIR  = Path("figures")
OUTPUT_JSON  = FIGURES_DIR / "crystal_data.json"


# ── Geometria da celula ────────────────────────────────────────────────────────
def get_cell_edges(cell: np.ndarray) -> list[list]:
    """Retorna lista de segmentos [start, end] representando as 12 arestas da celula."""
    o  = np.zeros(3)
    a1, a2, a3 = cell

    corners = [
        o,           # 0
        a1,          # 1
        a2,          # 2
        a3,          # 3
        a1 + a2,     # 4
        a1 + a3,     # 5
        a2 + a3,     # 6
        a1+a2+a3,    # 7
    ]

    edges = [
        (0,1),(0,2),(0,3),
        (1,4),(1,5),
        (2,4),(2,6),
        (3,5),(3,6),
        (4,7),(5,7),(6,7),
    ]

    return [
        [corners[i].tolist(), corners[j].tolist()]
        for i, j in edges
    ]


# ── Ligacoes O-H ───────────────────────────────────────────────────────────────
def compute_bonds(atoms, cutoff_oh: float = 1.3) -> list[list]:
    """Retorna ligacoes O-H por distancia (mais robusto que assumir ordem fixa).

    Usa cutoff de 1.3 A para O-H — ligacao covalente tipica no gelo Ih e ~0.96 A,
    mas com alguma tolerancia para coordenadas aproximadas vindas de CIF.
    """
    positions = atoms.get_positions()
    symbols   = atoms.get_chemical_symbols()

    oxygen_indices   = [i for i, s in enumerate(symbols) if s == "O"]
    hydrogen_indices = [i for i, s in enumerate(symbols) if s == "H"]

    bonds = []
    for o_idx in oxygen_indices:
        o_pos = positions[o_idx]
        for h_idx in hydrogen_indices:
            h_pos = positions[h_idx]
            dist  = np.linalg.norm(o_pos - h_pos)
            if dist <= cutoff_oh:
                bonds.append([positions[o_idx].tolist(), positions[h_idx].tolist()])

    return bonds


# ── Deteccao da vacancia ───────────────────────────────────────────────────────
def estimate_vacancy_position(perfect, vacancy) -> list[float]:
    """Encontra o O da estrutura perfeita mais distante de qualquer O da estrutura
    com vacancia. Esse e o melhor candidato a posicao da vacancia.

    Nota: implementacao atual usa distancia euclidiana simples. Uma versao futura
    deve usar distancias minimas de imagem (mic=True no ASE) para ser correta
    proxima a bordas periodicas.
    """
    perfect_o  = perfect.get_positions()[
        [i for i, a in enumerate(perfect) if a.symbol == "O"]
    ]
    vacancy_o  = vacancy.get_positions()[
        [i for i, a in enumerate(vacancy) if a.symbol == "O"]
    ]

    best_pos  = perfect_o[0]
    best_dist = -1.0

    for candidate in perfect_o:
        dists = np.linalg.norm(vacancy_o - candidate, axis=1)
        nearest = dists.min()
        if nearest > best_dist:
            best_pos  = candidate
            best_dist = nearest

    return best_pos.tolist()


# ── Serializacao dos atomos ────────────────────────────────────────────────────
def serialize_atoms(atoms) -> list[dict]:
    """Converte estrutura ASE em lista de dicionarios serializaveis.

    Cada atomo e um dict com:
        index    : indice global na estrutura
        symbol   : "O" ou "H"
        x, y, z  : coordenadas cartesianas em Angstrom
    """
    positions = atoms.get_positions()
    symbols   = atoms.get_chemical_symbols()

    return [
        {
            "index":  int(i),
            "symbol": str(sym),
            "x":      float(positions[i, 0]),
            "y":      float(positions[i, 1]),
            "z":      float(positions[i, 2]),
        }
        for i, sym in enumerate(symbols)
    ]


# ── Metadados da estrutura ─────────────────────────────────────────────────────
def structure_metadata(atoms, label: str) -> dict:
    """Retorna dict de metadados da estrutura."""
    symbols = atoms.get_chemical_symbols()
    n_O = symbols.count("O")
    n_H = symbols.count("H")

    cell_lengths = np.linalg.norm(atoms.cell, axis=1).tolist()
    cell_angles  = []  # pode ser expandido futuramente

    return {
        "label":         label,
        "n_atoms":       int(len(atoms)),
        "n_molecules":   int(n_O),
        "n_oxygen":      int(n_O),
        "n_hydrogen":    int(n_H),
        "cell_lengths_angstrom": [round(x, 4) for x in cell_lengths],
        "formula":       atoms.get_chemical_formula(),
    }


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    if not PERFECT_CIF.exists():
        raise FileNotFoundError(f"CIF nao encontrado: {PERFECT_CIF}")
    if not VACANCY_CIF.exists():
        raise FileNotFoundError(f"CIF nao encontrado: {VACANCY_CIF}")

    FIGURES_DIR.mkdir(exist_ok=True)

    perfect = read(PERFECT_CIF)
    vacancy = read(VACANCY_CIF)

    vacancy_pos = estimate_vacancy_position(perfect, vacancy)

    data = {
        "version": "1.0",
        "description": "Gelo Ih — supercelula perfeita vs. com vacancia molecular",
        "generated_by": "export_json.py — IC Gelo Ih / UFCAT",

        "perfect": {
            "metadata": structure_metadata(perfect, "Supercelula sem defeito"),
            "cell_edges": get_cell_edges(np.array(perfect.cell)),
            "atoms": serialize_atoms(perfect),
            "bonds": compute_bonds(perfect),
        },

        "vacancy": {
            "metadata": structure_metadata(vacancy, "Supercelula com vacancia molecular"),
            "cell_edges": get_cell_edges(np.array(vacancy.cell)),
            "atoms": serialize_atoms(vacancy),
            "bonds": compute_bonds(vacancy),
            "vacancy_position": vacancy_pos,
        },
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("=== JSON exportado com sucesso ===")
    print(f"  Arquivo : {OUTPUT_JSON}")
    print(f"  Perfeita: {data['perfect']['metadata']['n_atoms']} atomos, "
          f"{data['perfect']['metadata']['n_molecules']} H2O")
    print(f"  Vacancia: {data['vacancy']['metadata']['n_atoms']} atomos, "
          f"{data['vacancy']['metadata']['n_molecules']} H2O")
    print(f"  Vacancia estimada em: {[round(x,3) for x in vacancy_pos]} A")


if __name__ == "__main__":
    main()