# src/html_builder.py
"""
HTML Builder – V14.5.3

Responsável por transformar o relatório JSON produzido por
`src.compare_structures.build_report` em um documento HTML estático
usando o template Jinja2 localizado em `templates/report.html`.

O fluxo executado por `render_report` é:

1️⃣ Carregar o arquivo JSON (path fornecido pelo usuário ou padrão
   `figures/report.json`).
2️⃣ Instanciar um `jinja2.Environment` apontando para o diretório
   `templates/`.
3️⃣ Renderizar o template `report.html` passando todas as chaves do
   dicionário JSON como contexto (initial, relaxed, displacement,
   top10, initial_xyz, relaxed_xyz, displacements).
4️⃣ Gravar o HTML resultante em `figures/report.html` (cria o diretório
   caso ainda não exista).

Nenhum outro módulo do projeto é alterado; a lógica de cálculo e
geração do JSON permanece em `compare_structures.py`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Any

# ----------------------------------------------------------------------
# Dependências externas (devem ser adicionadas ao requirements.txt)
# ----------------------------------------------------------------------
# Jinja2 – motor de templates usado para renderizar o HTML.
#   pip install Jinja2
# ----------------------------------------------------------------------
from jinja2 import Environment, FileSystemLoader, select_autoescape


def _load_json(json_path: Path) -> Mapping[str, Any]:
    """
    Carrega o dicionário JSON a partir do caminho informado.
    Lança FileNotFoundError se o arquivo não existir.
    """
    if not json_path.is_file():
        raise FileNotFoundError(f"Relatório JSON não encontrado: {json_path}")

    with json_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)

    # Garantimos que o objeto seja um Mapping (dict‑like)
    if not isinstance(data, Mapping):
        raise ValueError("O conteúdo JSON não é um objeto de mapeamento.")
    return data


def _render_template(context: Mapping[str, Any]) -> str:
    """
    Renderiza `templates/report.html` usando Jinja2.
    O diretório base de templates é o diretório raiz do projeto.
    """
    # O template está em `templates/report.html` relativo ao diretório raiz.
    # Utilizamos Path(__file__) para encontrar o caminho do repositório.
    project_root = Path(__file__).resolve().parent.parent
    templates_dir = project_root / "templates"

    env = Environment(
        loader=FileSystemLoader(searchpath=str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("report.html")
    return template.render(**context)


def render_report(
    json_path: Path | str = Path("figures/report.json"),
    output_path: Path | str = Path("figures/report.html"),
) -> None:
    """
    Função principal da V14.5.3.

    Parameters
    ----------
    json_path : Path | str, opcional
        Caminho para o arquivo JSON gerado por `compare_structures.build_report`.
        Valor padrão → ``figures/report.json``.
    output_path : Path | str, opcional
        Onde o HTML renderizado será escrito. Valor padrão → ``figures/report.html``.
    """
    json_path = Path(json_path)
    output_path = Path(output_path)

    # 1️⃣ Carrega JSON
    data = _load_json(json_path)

    # 2️⃣ Renderiza o template com todas as chaves presentes no JSON.
    #    O template espera exatamente as variáveis abaixo; como o dicionário
    #    contém todas elas, basta repassá‑las como contexto.
    rendered_html = _render_template(data)

    # 3️⃣ Garante que o diretório de destino exista
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 4️⃣ Grava o HTML final
    with output_path.open("w", encoding="utf-8") as fp:
        fp.write(rendered_html)

    print(f"Relatório HTML gerado com sucesso: {output_path}")


# ----------------------------------------------------------------------
# Execução direta (para depuração rápida)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Renderiza o relatório HTML a partir do JSON criado por "
            "compare_structures.build_report."
        )
    )
    parser.add_argument(
        "-j",
        "--json",
        type=str,
        default="figures/report.json",
        help="Caminho para o JSON de entrada (padrão: figures/report.json)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="figures/report.html",
        help="Caminho para o HTML de saída (padrão: figures/report.html)",
    )
    args = parser.parse_args()

    render_report(json_path=args.json, output_path=args.output)