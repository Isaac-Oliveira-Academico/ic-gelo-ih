# src/lammps_parser.py
"""
Leitor de arquivos LAMMPS *dump* → objeto ``ase.Atoms``.

Esta versão utiliza a API oficial da ASE:
    ase.io.lammpsrun.read_lammps_dump
para garantir que o formato “dump.atom” seja interpretado
corretamente (o método genérico ``ase.io.read`` falha em algumas
versões/instalações).

Uso rápido:
    python -m src.lammps_parser lammps/dump.relaxed
"""

from pathlib import Path
from typing import Union

from ase import Atoms
from ase.io.lammpsrun import read_lammps_dump as _ase_read_lammps_dump


def read_lammps_dump(
    dump_path: Union[str, Path],
    *,
    frame: int = -1,
) -> Atoms:
    """
    Lê um arquivo LAMMPS *atom dump* e devolve um ``ase.Atoms``.

    Parameters
    ----------
    dump_path : str | Path
        Caminho para o dump gerado por LAMMPS (ex.: ``lammps/dump.relaxed``).
    frame : int, optional
        Índice do frame a ser lido.  ``-1`` (padrão) lê o **último**
        frame – o dump da minimização possui apenas um, mas o parâmetro
        garante robustez caso o usuário tenha vários frames.

    Returns
    -------
    ase.Atoms
        Estrutura contendo posições, símbolos químicos, caixa periódica,
        cargas, tipos etc. (tudo o que o dump contém).

    Raises
    ------
    FileNotFoundError
        Se ``dump_path`` não existir.
    RuntimeError
        Se a leitura falhar (formato inesperado, etc.).
    """
    dump_path = Path(dump_path)

    if not dump_path.is_file():
        raise FileNotFoundError(f"Arquivo LAMMPS dump não encontrado: {dump_path}")

    try:
        # ``_ase_read_lammps_dump`` aceita o argumento ``index`` que
        # corresponde ao frame a ser lido.
        atoms: Atoms = _ase_read_lammps_dump(str(dump_path), index=frame)
    except Exception as exc:
        raise RuntimeError(
            f"Falha ao ler o dump LAMMPS '{dump_path}': {exc}"
        ) from exc

    return atoms


# ----------------------------------------------------------------------
# Demo executável (python -m src.lammps_parser <caminho/dump>)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description=(
            "Lê um dump LAMMPS e exibe número de átomos, coordenadas "
            "finais e símbolos químicos (se houver)."
        )
    )
    parser.add_argument(
        "dump",
        type=Path,
        help="Caminho para o arquivo dump (ex.: lammps/dump.relaxed)",
    )
    parser.add_argument(
        "-f",
        "--frame",
        type=int,
        default=-1,
        help="Índice do frame a ser lido (padrão = -1 → último).",
    )
    args = parser.parse_args()

    try:
        atoms = read_lammps_dump(args.dump, frame=args.frame)
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)

    # 1️⃣ Número de átomos
    n_atoms = atoms.get_number_of_atoms()
    print(f"Número de átomos : {n_atoms}")

    # 2️⃣ Coordenadas finais (Å)
    print("\nCoordenadas finais (Å):")
    for i, (x, y, z) in enumerate(atoms.get_positions(), start=1):
        print(f"  {i:4d}:  {x: .6f}  {y: .6f}  {z: .6f}")

    # 3️⃣ Símbolos químicos (se houver)
    symbols = atoms.get_chemical_symbols()
    if symbols:
        print("\nSímbolos químicos:")
        print("  " + " ".join(symbols))