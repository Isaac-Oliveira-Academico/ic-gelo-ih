# src/compare_structures.py
"""
Módulo utilitário para comparar a estrutura *inicial* (CIF) com a
estrutura *relaxada* (dump LAMMPS) e gerar métricas de deslocamento.

Exporta:
    * read_initial_structure(cif_path) → ase.Atoms
    * read_relaxed_structure(dump_path) → ase.Atoms
    * compute_displacements(initial, relaxed) → dict com:
        - average   (float)  : deslocamento médio (Å)
        - maximum   (float)  : deslocamento máximo (Å)
        - per_atom  (list)   : [{index, symbol, dx, dy, dz, displacement}, …]
    * build_report(initial, relaxed) → dicionário pronto para JSON
"""

from pathlib import Path
from typing import Union, List, Dict

import json
import numpy as np
from ase import Atoms
from ase.io import read

# Função já existente que lê o dump LAMMPS → Atoms
from src.lammps_parser import read_lammps_dump


def read_initial_structure(cif_path: Union[str, Path]) -> Atoms:
    """
    Lê a estrutura de partida a partir de um arquivo CIF.

    Parameters
    ----------
    cif_path : str | Path
        Ex.: ``structures/supercelula_gelo_ih_3x3x2.cif``

    Returns
    -------
    ase.Atoms
    """
    return read(str(cif_path))


def read_relaxed_structure(dump_path: Union[str, Path]) -> Atoms:
    """
    Lê a estrutura relaxada a partir do dump LAMMPS gerado na etapa 14.3.

    Parameters
    ----------
    dump_path : str | Path
        Ex.: ``lammps/dump.relaxed``

    Returns
    -------
    ase.Atoms
    """
    return read_lammps_dump(dump_path)


def compute_displacements(initial: Atoms, relaxed: Atoms) -> Dict:
    """
    Calcula deslocamentos entre duas estruturas idênticas em número de átomos.

    Returns
    -------
    dict com as chaves:
        * average   – deslocamento médio (Å)
        * maximum   – deslocamento máximo (Å)
        * per_atom  – lista de dicionários:
            {
                "index":   int (1‑based index, como o visualizador usa),
                "symbol":  str,
                "dx":      float,
                "dy":      float,
                "dz":      float,
                "displacement": float   # módulo √(dx²+dy²+dz²)
            }
    """
    if initial.get_number_of_atoms() != relaxed.get_number_of_atoms():
        raise ValueError(
            "Número de átomos diferente entre as duas estruturas "
            f"({initial.get_number_of_atoms()} ≠ {relaxed.get_number_of_atoms()})"
        )

    # posições em Å
    pos_i = initial.get_positions()
    pos_r = relaxed.get_positions()

    # vetor deslocamento (Nx3)
    delta = pos_r - pos_i

    # módulo por átomo
    disp = np.linalg.norm(delta, axis=1)

    # média e máximo
    avg_disp = float(np.mean(disp))
    max_disp = float(np.max(disp))

    # lista detalhada por átomo (índice 1‑based para facilitar visualização)
    symbols = initial.get_chemical_symbols()
    per_atom: List[Dict] = []
    for i, (sym, dvec, dval) in enumerate(zip(symbols, delta, disp), start=1):
        per_atom.append(
            {
                "index": i,
                "symbol": sym,
                "dx": float(dvec[0]),
                "dy": float(dvec[1]),
                "dz": float(dvec[2]),
                "displacement": float(dval),
            }
        )

    return {
        "average_displacement": avg_disp,
        "maximum_displacement": max_disp,
        "per_atom": per_atom,
    }


def build_report(initial: Atoms, relaxed: Atoms) -> Dict:
    """
    Constrói um dicionário contendo:
        * metadados da estrutura inicial (número de átomos, fórmula)
        * metadados da estrutura relaxada (número de átomos, fórmula)
        * as métricas de deslocamento calculadas por ``compute_displacements``.
    Este dicionário pode ser serializado diretamente em JSON.
    """
    displacement_data = compute_displacements(initial, relaxed)

    report = {
        "initial": {
            "n_atoms": initial.get_number_of_atoms(),
            "formula": initial.get_chemical_formula(),
        },
        "relaxed": {
            "n_atoms": relaxed.get_number_of_atoms(),
            "formula": relaxed.get_chemical_formula(),
        },
        "displacement": displacement_data,
    }
    return report


def write_report(report: Dict, out_path: Union[str, Path]) -> None:
    """
    Grava o relatório em JSON (indentado para leitura humana).

    Parameters
    ----------
    report : dict
        Dicionário retornado por ``build_report``.
    out_path : str | Path
        Arquivo onde o JSON será salvo.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=2, ensure_ascii=False)