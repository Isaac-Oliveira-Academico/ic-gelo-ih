# scripts/compare_structures.py
"""
CLI para comparar a estrutura inicial (CIF) com a estrutura relaxada
(dump LAMMPS) e gerar um relatório JSON.

Uso típico:
    python -m scripts.compare_structures \
        --cif structures/supercelula_gelo_ih_3x3x2.cif \
        --dump lammps/dump.relaxed \
        --out  lammps/report.json
"""

import argparse
import sys
from pathlib import Path

from src.compare_structures import (
    read_initial_structure,
    read_relaxed_structure,
    build_report,
    write_report,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compara estrutura inicial (CIF) e relaxada (dump LAMMPS)."
    )
    parser.add_argument(
        "--cif",
        type=Path,
        required=True,
        help="Caminho para o arquivo CIF da estrutura inicial.",
    )
    parser.add_argument(
        "--dump",
        type=Path,
        required=True,
        help="Caminho para o dump LAMMPS da estrutura relaxada (dump.relaxed).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("lammps/report.json"),
        help="Arquivo JSON de saída (padrão: lammps/report.json).",
    )
    args = parser.parse_args()

    try:
        initial = read_initial_structure(args.cif)
        relaxed = read_relaxed_structure(args.dump)
        report = build_report(initial, relaxed)
        write_report(report, args.out)
    except Exception as exc:
        sys.stderr.write(f"Erro: {exc}\n")
        sys.exit(1)

    # Resumo rápido na tela
    disp = report["displacement"]
    print("\n=== Relatório de deslocamento ===")
    print(f"Deslocamento médio  : {disp['average_displacement']:.6f} Å")
    print(f"Deslocamento máximo : {disp['maximum_displacement']:.6f} Å")
    print(f"Relatório gravado em : {args.out.resolve()}")
    print("Detalhes por átomo podem ser encontrados no campo \"per_atom\" do JSON.")
    print("==================================================================")

if __name__ == "__main__":
    main()