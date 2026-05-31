"""Exporta a estrutura inicial para diferentes formatos atomicos.

Este script le o arquivo XYZ inicial e gera copias em formatos usados por
programas diferentes: XYZ, PDB e CIF.

Observacao importante:
    A estrutura inicial ainda nao e uma celula unitaria fisica do gelo Ih.
    Para escrever CIF, criamos uma caixa cartesiana auxiliar em torno dos
    atomos. Essa caixa ajuda na interoperabilidade, mas ainda nao representa
    uma celula cristalografica rigorosa.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/03_exportar_formatos.py
"""

from pathlib import Path

import numpy as np
from ase.io import read, write


INPUT_XYZ = Path("data/rede_gelo_inicial.xyz")
OUTPUT_DIR = Path("structures")
VACUUM_PADDING = 4.0


def structure_has_cell(atoms):
    """Verifica se a estrutura possui uma celula com volume diferente de zero."""
    return atoms.cell.volume > 0.0


def add_auxiliary_box(atoms, padding=VACUUM_PADDING):
    """Cria uma caixa auxiliar ao redor dos atomos para exportacao em CIF/PDB."""
    atoms = atoms.copy()
    positions = atoms.get_positions()

    min_position = positions.min(axis=0)
    max_position = positions.max(axis=0)
    span = max_position - min_position
    cell_lengths = span + 2.0 * padding

    atoms.translate(-min_position + padding)
    atoms.set_cell(np.diag(cell_lengths))
    atoms.set_pbc(False)

    return atoms


def main():
    """Le a estrutura inicial e exporta os arquivos de saida."""
    if not INPUT_XYZ.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_XYZ}\n"
            "Execute este script a partir da raiz do repositorio."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)

    atoms = read(INPUT_XYZ)

    if structure_has_cell(atoms):
        export_atoms = atoms
        box_message = "A estrutura ja possui celula definida."
    else:
        export_atoms = add_auxiliary_box(atoms)
        box_message = "Foi criada uma caixa auxiliar para exportacao."

    xyz_output = OUTPUT_DIR / "rede_gelo_inicial.xyz"
    pdb_output = OUTPUT_DIR / "rede_gelo_inicial.pdb"
    cif_output = OUTPUT_DIR / "rede_gelo_inicial.cif"

    write(xyz_output, atoms)
    write(pdb_output, export_atoms)
    write(cif_output, export_atoms)

    print("=== Exportacao de formatos com ASE ===")
    print(f"Arquivo de entrada: {INPUT_XYZ}")
    print(f"Numero de atomos: {len(atoms)}")
    print(box_message)
    print("\nArquivos gerados:")
    print(f"- {xyz_output}")
    print(f"- {pdb_output}")
    print(f"- {cif_output}")
    print("\nCelula usada nos formatos com caixa:")
    print(export_atoms.cell)
    print(f"PBC: {export_atoms.pbc}")


if __name__ == "__main__":
    main()