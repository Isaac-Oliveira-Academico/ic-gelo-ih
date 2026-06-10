# src/lammps_builder.py
"""Módulo utilitário para gerar arquivos LAMMPS DATA a partir de CIFs.

Utiliza a API ASE (ase.io.read / ase.io.lammpsdata) para:
1. Ler um arquivo CIF e obter um objeto `ase.Atoms`.
2. Exportar esse objeto para o formato LAMMPS DATA.

O caminho de saída padrão da V14.1 será:  lammps/data.lammps
"""

from pathlib import Path
from typing import Union

from ase import Atoms
from ase.io import read, write


def read_cif(cif_path: Union[str, Path]) -> Atoms:
    """
    Lê um arquivo CIF usando ASE e devolve o objeto ``Atoms``.

    Parameters
    ----------
    cif_path : str | Path
        Caminho absoluto ou relativo para o arquivo *.cif*.

    Returns
    -------
    Atoms
        Estrutura atomística completa.
    """
    cif_path = Path(cif_path)
    if not cif_path.is_file():
        raise FileNotFoundError(f"CIF não encontrado: {cif_path}")
    return read(cif_path)


def write_lammps_data(
    atoms: Atoms,
    out_path: Union[str, Path],
    *,
    atom_style: str = "full",
    units: str = "metal",
) -> None:
    """
    Grava ``atoms`` no formato LAMMPS DATA.

    Parameters
    ----------
    atoms : Atoms
        Objeto ASE a ser exportado.
    out_path : str | Path
        Arquivo destino (ex.: ``lammps/data.lammps``).
    atom_style : str, optional
        Estilo de átomo para o data file (default ``'full'`` – contém
        id, tipo, carga, coordenadas etc.). Ajuste conforme necessidade.
    units : str, optional
        Unidades LAMMPS (default ``'metal'`` → Angstrom, eV, etc.).
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # ASE fornece a escrita direta para o formato LAMMPS DATA
    write(
        out_path,
        atoms,
        format="lammps-data",
        atom_style=atom_style,
        units=units,
    )


def build_from_cif(
    cif_path: Union[str, Path],
    out_path: Union[str, Path] = Path("lammps/data.lammps"),
    *,
    atom_style: str = "full",
    units: str = "metal",
) -> Path:
    """
    Função de conveniência: lê o CIF e grava o LAMMPS DATA.

    Returns
    -------
    Path
        Caminho absoluto do arquivo gerado.
    """
    atoms = read_cif(cif_path)
    write_lammps_data(atoms, out_path, atom_style=atom_style, units=units)
    return Path(out_path).resolve()