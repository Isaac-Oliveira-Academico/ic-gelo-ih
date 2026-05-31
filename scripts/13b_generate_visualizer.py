"""Gera um HTML completamente autossuficiente do visualizador cristalografico.

Modo de operacao:
  - Le os CIF com ASE
  - Calcula geometria, ligacoes e posicao da vacancia
  - Emite o JSON como bloco <script> inline dentro do HTML
  - O resultado e um unico arquivo .html portavel:
      * Abre offline em qualquer navegador
      * Compartilhavel por WhatsApp, email, GitHub Releases
      * Sem CORS, sem servidor, sem dependencias externas alem do CDN Plotly

Execucao:
    cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
    source ~/.venvs/ic-gelo-ih/bin/activate
    python scripts/generate_visualizer.py

Saida:
    figures/gelo_ih_visualizador.html   (arquivo unico, ~3-5 MB)
"""

from pathlib import Path
import json
import numpy as np
from ase.io import read
from render_html import render_html
import sys

# Adiciona a raiz do projeto (uma pasta acima de 'scripts') ao caminho do Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from src.version import APP_VERSION

# ── Caminhos ──────────────────────────────────────────────────────────────────
STRUCTURES_DIR = PROJECT_ROOT / "structures"
TEMPLATES_DIR  = PROJECT_ROOT / "templates"
FIGURES_DIR    = PROJECT_ROOT / "figures"

PERFECT_CIF = (
    STRUCTURES_DIR
    / "supercelula_gelo_ih_3x3x2.cif"
)

VACANCY_CIF = (
    STRUCTURES_DIR
    / "gelo_ih_vacancia.cif"
)

TEMPLATE_HTML = (
    TEMPLATES_DIR
    / "visualizer_template.html"
)

OUTPUT_HTML = (
    FIGURES_DIR
    / "gelo_ih_visualizador.html"
)

OUTPUT_JSON = (
    FIGURES_DIR
    / "crystal_data.json"
)

# Tambem exporta o JSON separado (para debug e versionamento)



# ── Geometria da celula ────────────────────────────────────────────────────────
def get_cell_edges(cell: np.ndarray) -> list:
    o = np.zeros(3)
    a1, a2, a3 = cell
    corners = [
        o, a1, a2, a3,
        a1+a2, a1+a3, a2+a3, a1+a2+a3,
    ]
    edges = [
        (0,1),(0,2),(0,3),
        (1,4),(1,5),
        (2,4),(2,6),
        (3,5),(3,6),
        (4,7),(5,7),(6,7),
    ]
    return [[corners[i].tolist(), corners[j].tolist()] for i, j in edges]


# ── Ligacoes O-H por distancia ─────────────────────────────────────────────────
def compute_bonds(atoms, cutoff_oh: float = 1.3) -> list:
    positions = atoms.get_positions()
    symbols   = atoms.get_chemical_symbols()
    o_idx = [i for i, s in enumerate(symbols) if s == "O"]
    h_idx = [i for i, s in enumerate(symbols) if s == "H"]
    bonds = []
    for oi in o_idx:
        for hi in h_idx:
            if np.linalg.norm(positions[oi] - positions[hi]) <= cutoff_oh:
                bonds.append([positions[oi].tolist(), positions[hi].tolist()])
    return bonds


# ── Posicao da vacancia ────────────────────────────────────────────────────────
def estimate_vacancy_position(perfect, vacancy) -> list:
    p_o = perfect.get_positions()[[i for i,a in enumerate(perfect) if a.symbol=="O"]]
    v_o = vacancy.get_positions()[[i for i,a in enumerate(vacancy)  if a.symbol=="O"]]
    best, best_d = p_o[0], -1.0
    for c in p_o:
        d = np.linalg.norm(v_o - c, axis=1).min()
        if d > best_d:
            best, best_d = c, d
    return best.tolist()


# ── Serializacao ───────────────────────────────────────────────────────────────
def serialize_atoms(atoms) -> list:
    pos = atoms.get_positions()
    sym = atoms.get_chemical_symbols()
    return [
        {"index": int(i), "symbol": str(s),
         "x": float(pos[i,0]), "y": float(pos[i,1]), "z": float(pos[i,2])}
        for i, s in enumerate(sym)
    ]


def structure_metadata(atoms, label: str) -> dict:
    sym = atoms.get_chemical_symbols()
    nO  = sym.count("O")
    lengths = np.linalg.norm(atoms.cell, axis=1).tolist()
    return {
        "label":       label,
        "n_atoms":     int(len(atoms)),
        "n_molecules": int(nO),
        "n_oxygen":    int(nO),
        "n_hydrogen":  int(sym.count("H")),
        "cell_lengths": [round(x,4) for x in lengths],
        "formula":     atoms.get_chemical_formula(),
    }


# ── Monta payload de dados ─────────────────────────────────────────────────────
def build_data(perfect, vacancy) -> dict:
    vpos = estimate_vacancy_position(perfect, vacancy)
    return {
        "version": APP_VERSION,
        "description": "Gelo Ih — supercelula perfeita vs. vacancia molecular",
        "generated_by":"generate_visualizer.py — IC Gelo Ih / UFCAT",
        "perfect": {
            "metadata":   structure_metadata(perfect, "Supercelula sem defeito"),
            "cell_edges": get_cell_edges(np.array(perfect.cell)),
            "atoms":      serialize_atoms(perfect),
            "bonds":      compute_bonds(perfect),
        },
        "vacancy": {
            "metadata":          structure_metadata(vacancy, "Supercelula com vacancia molecular"),
            "cell_edges":        get_cell_edges(np.array(vacancy.cell)),
            "atoms":             serialize_atoms(vacancy),
            "bonds":             compute_bonds(vacancy),
            "vacancy_position":  vpos,
        },
    }


# ── Template HTML ──────────────────────────────────────────────────────────────

def validate_html(html_path):
    text = html_path.read_text(
        encoding="utf-8"
    )

    placeholders = [
        "@@CRYSTAL_DATA@@"
    ]

    for token in placeholders:
        if token in text:
            raise RuntimeError(
                f"Placeholder não substituído: {token}"
            )


# ── Injeta dados no template e grava ──────────────────────────────────────────
def main():
    for p in [PERFECT_CIF, VACANCY_CIF]:
        if not p.exists():
            raise FileNotFoundError(f"CIF nao encontrado: {p}")

    FIGURES_DIR.mkdir(exist_ok=True)

    perfect = read(PERFECT_CIF)
    vacancy = read(VACANCY_CIF)

    data = build_data(perfect, vacancy)

    # Salva JSON separado (para debug e versionamento Git)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Injeta JSON no template HTML
    json_str  = json.dumps(data, ensure_ascii=False)

    # Debug temporário
    print()
    print("=== DEBUG PATHS ===")
    print("PROJECT_ROOT :", PROJECT_ROOT)
    print("TEMPLATE     :", TEMPLATE_HTML)
    print("EXISTS       :", TEMPLATE_HTML.exists())
    print()

    #Renderiza o HTML final
    render_html(TEMPLATE_HTML, OUTPUT_HTML,
    {
        "CRYSTAL_DATA": json_str
    }
    )
    validate_html(OUTPUT_HTML)

    pm = data["perfect"]["metadata"]
    vm = data["vacancy"]["metadata"]
    size_kb = OUTPUT_HTML.stat().st_size // 1024

    print("=== Visualizador gerado com sucesso ===")
    print(f"  HTML Final         : {OUTPUT_HTML} ({size_kb} KB)")
    print(f"  JSON separado        : {OUTPUT_JSON} ({size_kb} KB)")
    print(f"  Perfeita : {pm['n_atoms']} atomos, {pm['n_molecules']} H2O")
    print(f"  Vacancia : {vm['n_atoms']} atomos, {vm['n_molecules']} H2O")
    print(f"  Vacancia em : {[round(x,3) for x in data['vacancy']['vacancy_position']]} A")
    print()
    print("  Compartilhe o arquivo HTML diretamente.")
    print("  Abre offline em qualquer navegador (Android, iOS, macOS, Windows, Linux).")


if __name__ == "__main__":
    main()