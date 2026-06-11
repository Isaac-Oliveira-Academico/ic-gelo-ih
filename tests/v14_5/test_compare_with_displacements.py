# tests/v14_5/test_compare_with_displacements.py
"""
Teste automatizado da nova função compare_with_displacements (V14.5.1).

Objetivos:
- Verificar que a função retorna as chaves esperadas.
- Garantir que o número de vetores corresponde ao número de átomos.
- Checar que o top‑10 contém exatamente 10 entradas e que estão ordenadas
  de forma decrescente (maior deslocamento primeiro).
"""

import sys
from pathlib import Path
import pytest  # <‑‑ IMPORTAÇÃO necessária

# ----------------------------------------------------------------------
# 1️⃣  Garantir que o diretório raiz do projeto esteja no PYTHONPATH.
# ----------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parents[2]   # dois níveis acima: /.../ic-gelo-ih
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ----------------------------------------------------------------------
# 2️⃣  Imports do código‑fonte
# ----------------------------------------------------------------------
from src.lammps_builder import read_cif
from src.lammps_parser import read_lammps_dump
from src.compare_structures import compare_with_displacements

# ----------------------------------------------------------------------
# 3️⃣  Fixtures – carregam as estruturas usadas nos testes
# ----------------------------------------------------------------------
@pytest.fixture
def initial_atoms():
    """Estrutura inicial – usa um CIF já presente no repositório."""
    cif_path = PROJECT_ROOT / "structures" / "gelo_ih_vacancia.cif"
    return read_cif(cif_path)


@pytest.fixture
def relaxed_atoms():
    """Estrutura relaxada – dump produzido pela minimização LAMMPS."""
    dump_path = PROJECT_ROOT / "lammps" / "dump.relaxed"
    return read_lammps_dump(dump_path)


# ----------------------------------------------------------------------
# 4️⃣  Testes propriamente ditos
# ----------------------------------------------------------------------
def test_compare_with_displacements_keys(initial_atoms, relaxed_atoms):
    """Verifica que o dicionário possui as chaves corretas."""
    out = compare_with_displacements(initial_atoms, relaxed_atoms)

    assert isinstance(out, dict)
    assert set(out.keys()) == {"displacements", "total_displacement", "top10"}

    # número de vetores deve ser igual ao número de átomos
    assert len(out["displacements"]) == initial_atoms.get_number_of_atoms()
    # deslocamento total deve ser positivo
    assert out["total_displacement"] > 0.0


def test_top10_is_sorted(initial_atoms, relaxed_atoms):
    """Top‑10 deve ter exatamente 10 itens e estar ordenado decrescentemente."""
    out = compare_with_displacements(initial_atoms, relaxed_atoms)

    top = out["top10"]
    assert len(top) == 10

    # Verifica ordenação decrescente pelo campo 'disp'
    disps = [item["disp"] for item in top]
    assert disps == sorted(disps, reverse=True)

    # Cada entrada deve conter os campos esperados
    for entry in top:
        assert {"index", "symbol", "disp"} <= set(entry.keys())
        assert isinstance(entry["index"], int)
        assert isinstance(entry["symbol"], str)
        assert isinstance(entry["disp"], float)