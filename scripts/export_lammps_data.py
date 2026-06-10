# scripts/export_lammps_data.py
"""Entrypoint de linha de comando para gerar LAMMPS DATA a partir do CIF padrão."""

import argparse
from pathlib import Path

from src.lammps_builder import build_from_cif


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta a estrutura CIF para formato LAMMPS DATA (V14.1)."
    )
    parser.add_argument(
        "--cif",
        type=Path,
        default=Path("structures/supercelula_gelo_ih_3x3x2.cif"),
        help="Caminho para o arquivo CIF de entrada.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("lammps/data.lammps"),
        help="Caminho de saída para o arquivo LAMMPS DATA.",
    )
    parser.add_argument(
        "--atom-style",
        default="full",
        help="Estilo de átomo LAMMPS (default: full).",
    )
    parser.add_argument(
        "--units",
        default="metal",
        help="Unidades LAMMPS (default: metal).",
    )
    args = parser.parse_args()

    out_file = build_from_cif(
        args.cif,
        args.out,
        atom_style=args.atom_style,
        units=args.units,
    )
    print(f"LAMMPS DATA gerado com sucesso: {out_file}")


if __name__ == "__main__":
    main()