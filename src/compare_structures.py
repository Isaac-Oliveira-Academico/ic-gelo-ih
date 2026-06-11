# src/compare_structures.py
"""
Módulo utilitário para comparar a estrutura *inicial* (CIF) com a
estrutura *relaxada* (dump LAMMPS) e gerar métricas de deslocamento.

Exporta (mantidos para compatibilidade com V13/V14.4):
    * read_initial_structure(cif_path) → ase.Atoms
    * read_relaxed_structure(dump_path) → ase.Atoms
    * compute_displacements(initial, relaxed) → dict com:
        - average   (float)  : deslocamento médio (Å)
        - maximum   (float)  : deslocamento máximo (Å)
        - per_atom  (list)   : [{index, symbol, dx, dy, dz, displacement}, …]
    * build_report(initial, relaxed) → dicionário pronto para JSON

Novidade V14.5.1:
    * compare_with_displacements(initial, relaxed) → dict contendo:
        - displacements (lista de vetores [dx,dy,dz] por átomo)
        - total_displacement (soma das normas)
        - top10 (lista dos 10 maiores deslocamentos com índice, símbolo e valor)
"""

from pathlib import Path
from typing import Union, List, Dict

import json
import numpy as np
from ase import Atoms
from ase.io import read

# Função já existente que lê o dump LAMMPS → Atoms
from src.lammps_parser import read_lammps_dump


# ----------------------------------------------------------------------
# Funções de leitura (mantidas)
# ----------------------------------------------------------------------
def read_initial_structure(cif_path: Union[str, Path]) -> Atoms:
    """Lê a estrutura de partida a partir de um arquivo CIF."""
    return read(str(cif_path))


def read_relaxed_structure(dump_path: Union[str, Path]) -> Atoms:
    """Lê a estrutura relaxada a partir do dump LAMMPS."""
    return read_lammps_dump(dump_path)


# ----------------------------------------------------------------------
# Cálculo de deslocamentos (já existente – mantido)
# ----------------------------------------------------------------------
def compute_displacements(initial: Atoms, relaxed: Atoms) -> Dict:
    """Calcula deslocamentos entre duas estruturas idênticas em número de átomos."""
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

    # lista detalhada por átomo (índice 1‑based)
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


# ----------------------------------------------------------------------
# Relatório JSON (mantido)
# ----------------------------------------------------------------------
def build_report(initial: Atoms, relaxed: Atoms) -> Dict:
    """Constrói um dicionário contendo metadados e métricas de deslocamento."""
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
    """Grava o relatório em JSON (indentado para leitura humana)."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=2, ensure_ascii=False)


# ----------------------------------------------------------------------
# NOVA FUNÇÃO – V14.5.1
# ----------------------------------------------------------------------
def compare_with_displacements(initial: Atoms, relaxed: Atoms) -> Dict:
    """
    V14.5.1 – Backend de comparação estrutural.

    Calcula, para cada átomo, o vetor de deslocamento entre a estrutura
    inicial e a relaxada, devolvendo também:
        • deslocamento total (soma das normas);
        • os 10 átomos com maior deslocamento (top‑10).

    Parâmetros
    ----------
    initial : ase.Atoms
        Estrutura de partida (geralmente lida do CIF).
    relaxed : ase.Atoms
        Estrutura resultante da minimização LAMMPS.

    Retorna
    -------
    dict
        {
            "displacements": List[List[float]],   # N x 3
            "total_displacement": float,
            "top10": List[{"index": int, "symbol": str, "disp": float}]
        }
    """
    # ---------------------------------------------------------------
    # 1️⃣ Validação permissiva
    # ---------------------------------------------------------------
    # Em alguns casos o dump pode conter um número de átomos ligeiramente
    # diferente (por exemplo, hidrogênio a mais).  Para que a V14.5.1 seja
    # robusta, usamos apenas o número **mínimo** de átomos presente nas
    # duas estruturas.  Os átomos excedentes são ignorados nas métricas
    # de deslocamento – eles ainda aparecem nas contagens de `build_report`.
    # ---------------------------------------------------------------
    n_initial = initial.get_number_of_atoms()
    n_relaxed = relaxed.get_number_of_atoms()
    n_common = min(n_initial, n_relaxed)

    # ---- Vetores de deslocamento (apenas átomos comuns) ----
    pos_initial = initial.get_positions()[:n_common]
    pos_relaxed = relaxed.get_positions()[:n_common]

    disp_vec = pos_relaxed - pos_initial       # (n_common, 3) ndarray
    norms = np.linalg.norm(disp_vec, axis=1)   # vetor de tamanho n_common

    # ---- Métricas -------------------------------------------------
    total_disp = float(np.sum(norms))

    # ---- Top‑10 maiores deslocamentos ----------------------------
    top_idx = np.argsort(-norms)[:10]          # índices em ordem decrescente
    top10: List[Dict[str, any]] = [
        {
            "index": int(idx + 1),                     # 1‑based (amigável ao usuário)
            "symbol": initial[idx].symbol,
            "disp": float(norms[idx]),
        }
        for idx in top_idx
    ]

    # ---- Resultado ------------------------------------------------
    result: Dict = {
        "displacements": disp_vec.tolist(),   # lista de [dx, dy, dz] por átomo
        "total_displacement": total_disp,
        "top10": top10,
    }

    return result