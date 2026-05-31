"""Valida uma estrutura XYZ usando ASE.

Este script faz a primeira leitura computacional da estrutura gerada no
projeto da IC. Ele carrega um arquivo XYZ, imprime informacoes basicas dos
atomos e calcula distancias interatomicas.

Execucao esperada, a partir da raiz do repositorio:

    python scripts/02_validar_xyz_ase.py
"""

from collections import Counter
from pathlib import Path

import numpy as np
from ase.io import read


INPUT_XYZ = Path("data/rede_gelo_inicial.xyz")
MAX_DISTANCES_TO_SHOW = 12


def format_pair(symbols, i, j):
    """Retorna uma representacao legivel de um par atomico."""
    return f"{symbols[i]}{i}-{symbols[j]}{j}"


def main():
    """Executa a leitura, validacao e analise simples da estrutura."""
    if not INPUT_XYZ.exists():
        raise FileNotFoundError(
            f"Arquivo nao encontrado: {INPUT_XYZ}\n"
            "Execute este script a partir da raiz do repositorio ou gere "
            "primeiro o arquivo data/rede_gelo_inicial.xyz."
        )

    atoms = read(INPUT_XYZ)
    symbols = atoms.get_chemical_symbols()
    positions = atoms.get_positions()
    species_count = Counter(symbols)

    print("=== Validacao XYZ com ASE ===")
    print(f"Arquivo lido: {INPUT_XYZ}")
    print(f"Objeto ASE: {atoms}")
    print(f"Numero total de atomos: {len(atoms)}")
    print(f"Especies quimicas: {sorted(species_count)}")
    print(f"Contagem por especie: {dict(species_count)}")

    print("\n=== Primeiras coordenadas cartesianas (Angstrom) ===")
    for index, (symbol, position) in enumerate(zip(symbols, positions)):
        x, y, z = position
        print(f"{index:3d}  {symbol:2s}  x={x:9.4f}  y={y:9.4f}  z={z:9.4f}")
        if index == 9 and len(atoms) > 10:
            print(f"... {len(atoms) - 10} atomos restantes omitidos")
            break

    distances = atoms.get_all_distances(mic=False)
    pairs = []

    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            pairs.append((distances[i, j], i, j))

    pairs.sort(key=lambda item: item[0])

    print("\n=== Menores distancias interatomicas (Angstrom) ===")
    for distance, i, j in pairs[:MAX_DISTANCES_TO_SHOW]:
        pair_name = format_pair(symbols, i, j)
        print(f"{pair_name:10s}  {distance:8.4f}")

    if pairs:
        all_distances = np.array([distance for distance, _, _ in pairs])
        print("\n=== Resumo das distancias ===")
        print(f"Menor distancia: {all_distances.min():.4f} Angstrom")
        print(f"Maior distancia: {all_distances.max():.4f} Angstrom")
        print(f"Distancia media: {all_distances.mean():.4f} Angstrom")


if __name__ == "__main__":
    main()