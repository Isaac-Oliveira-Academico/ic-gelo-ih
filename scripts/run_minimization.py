# scripts/run_minimization.py
"""CLI simples para disparar a minimização LAMMPS (V14.2)."""

import argparse
from pathlib import Path

from src.lammps_runner import run_lammps


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Executa minimização LAMMPS a partir de data.lammps."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("lammps/in.minimize"),
        help="Arquivo de input LAMMPS (default: lammps/in.minimize).",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=Path("lammps"),
        help="Diretório onde será executado LAMMPS (default: lammps).",
    )
    args = parser.parse_args()

    log_path, dump_path = run_lammps(args.input, args.work_dir)

    print(f"✅ LAMMPS finalizado")
    print(f"  Log  → {log_path}")
    print(f"  Dump → {dump_path}")


if __name__ == "__main__":
    main()