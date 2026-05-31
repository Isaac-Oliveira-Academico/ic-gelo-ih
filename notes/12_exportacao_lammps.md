# Etapa 12b — Relatorio Visual da Vacancia

## Etapa 1 — Conceito fisico

Depois de criar uma vacancia, e importante comparar a estrutura defeituosa com
a estrutura sem defeito. Essa comparacao ajuda a enxergar que o defeito nao e
uma nova substancia, mas uma alteracao local na rede.

Nesta etapa, comparamos:

- supercelula do gelo Ih aproximado sem defeito;
- supercelula do gelo Ih aproximado com uma molecula `H2O` removida.

## Etapa 2 — Implementacao computacional

O script `12b_html_final_vacancia.py` gera um HTML final com dois paineis:

1. estrutura sem defeito;
2. estrutura com vacancia molecular.

O arquivo gerado funciona como figura interativa para apresentacao tecnica da
versao inicial do projeto.

## Etapa 3 — Como executar

No G7Node:

```bash
cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/12b_html_final_vacancia.py
```

Depois abra:

```text
figures/relatorio_visual_vacancia_gelo_ih.html
```

## Etapa 4 — Explicacao do codigo

```python
PERFECT_CIF = Path("structures/supercelula_gelo_ih_3x3x2.cif")
VACANCY_CIF = Path("structures/gelo_ih_vacancia.cif")
```

Define as duas estruturas comparadas.

```python
make_subplots(...)
```

Cria dois paineis 3D no mesmo HTML.

```python
estimate_vacancy_position(...)
```

Estima a posicao da vacancia comparando a estrutura sem defeito com a estrutura
defeituosa.

```python
add_vacancy_marker(...)
```

Destaca a posicao da vacancia com um marcador amarelo.

## Etapa 5 — Melhorias futuras

Melhorias possiveis:

- adicionar texto explicativo dentro do HTML;
- sincronizar camera entre os dois paineis;
- comparar distancias ao redor da vacancia;
- exportar uma imagem PNG automatica do relatorio;
- transformar o relatorio em pagina web do projeto.

## Etapa 6 — Conexao com pesquisa cientifica real

Comparar estrutura perfeita e estrutura defeituosa e uma pratica comum em
simulacoes de materiais. Em uma etapa futura, essa comparacao pode incluir:

- energia de formacao da vacancia;
- relaxacao estrutural;
- mudancas em vizinhanca local;
- resposta mecanica sob deformacao.