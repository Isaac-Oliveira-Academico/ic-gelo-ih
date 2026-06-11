# tests/v14_4/test_lammps_parser_mapping.py
"""Teste da correção V14.4.1 – mapeamento de tipos LAMMPS para símbolos químicos.

O dump ``lammps/dump.relaxed`` contém apenas a coluna ``type``.
Após a correção, o parser deve devolver:
- tipo 1 → O
- tipo 2 → H
"""

import sys
from pathlib import Path

# --------------------------------------------------------------
# 1️⃣ Garantir que o diretório raiz do projeto esteja no PYTHONPATH
# --------------------------------------------------------------
# Quando o teste é executado, o Python não conhece o pacote ``src``.
# Inserimos o caminho da raiz (duas pastas acima deste arquivo)
# para que o import a seguir funcione.
PROJECT_ROOT = Path(__file__).parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from src.lammps_parser import read_lammps_dump


@pytest.fixture
def dump_path() -> Path:
    """Caminho absoluto do dump gerado por LAMMPS."""
    return Path(__file__).parents[2] / "lammps" / "dump.relaxed"


def test_type_mapping(dump_path: Path):
    """Verifica se o parser devolve 72 O e 144 H (tipo 1 → O, tipo 2 → H)."""
    # 1️⃣ O dump deve existir
    assert dump_path.is_file(), f"Dump file not found: {dump_path}"

    # 2️⃣ Ler o dump usando a função corrigida
    atoms = read_lammps_dump(dump_path)

    # 3️⃣ Obter a lista de símbolos químicos
    symbols = atoms.get_chemical_symbols()

    # O dump tem 216 átomos (conforme arquivo)
    assert len(symbols) == 216

    # Contagens esperadas de acordo com o relatório inicial/relaxado
    o_count = symbols.count("O")
    h_count = symbols.count("H")

    assert o_count == 72, f"O count mismatch: expected 72, got {o_count}"
    assert h_count == 144, f"H count mismatch: expected 144, got {h_count}"