# Etapa 13 — Visualizador Científico Multiplataforma do Gelo Ih

## Etapa 1 — Conceito físico

Nesta etapa foi desenvolvido um visualizador científico para comparar uma supercélula perfeita de gelo Ih com uma supercélula contendo uma vacância molecular.

A comparação visual permite identificar a posição do defeito cristalino e compreender como a remoção de uma molécula H₂O altera localmente a rede cristalina.

Foram representados:

* Oxigênios
* Hidrogênios
* Ligações O–H
* Célula cristalina
* Vacância molecular

---

## Etapa 2 — Implementação computacional

Os dados cristalográficos são obtidos a partir de estruturas CIF utilizando ASE.

O script gera automaticamente:

* crystal_data.json
* gelo_ih_visualizador.html

O visualizador final é produzido como um único arquivo HTML autossuficiente.

Todos os dados cristalográficos são incorporados diretamente ao HTML durante a geração, eliminando dependências externas de JSON, problemas de CORS e necessidade de servidor backend.

O mesmo arquivo pode ser utilizado:

* localmente
* offline
* GitHub Pages
* dispositivos móveis
* compartilhamento por e-mail ou mensageiros

---

## Etapa 3 — Execução

Ativar ambiente:

```bash
source ~/.venvs/ic-gelo-ih/bin/activate
```

Executar:

```bash
python scripts/13_visualizador_cientifico_ multiplataforma.py
```

Arquivos gerados:

```text
figures/crystal_data.json
figures/gelo_ih_visualizador.html
```

---

## Etapa 4 — Resultado

O visualizador permite:

* comparação lado a lado entre estrutura perfeita e estrutura com vacância
* visualização 3D interativa baseada em Plotly
* visualização responsiva para desktop, tablet e smartphone
* identificação automática da vacância molecular
* exibição da célula cristalina
* exibição das ligações O–H
* câmera inicial padronizada
* exibição de metadados cristalográficos
* funcionamento totalmente offline
* compatibilidade com GitHub Pages
---

## Etapa 5 — Melhorias futuras

Próximas funcionalidades planejadas:

* seleção individual de átomos
* painel de propriedades atômicas
* NeighborList (ASE)
* coordenação atômica
* distâncias O–O
* distâncias O–H
* múltiplas vacâncias
* defeitos intersticiais
* sincronização de câmera
* exportação PNG automática

---

## Etapa 6 — Conexão com a pesquisa científica

Esta etapa estabelece a base visual para estudos futuros envolvendo:

* defeitos pontuais
* relaxação estrutural
* plasticidade do gelo Ih
* dinâmica molecular
* exportação para LAMMPS
* comparação futura com regolito lunar

O visualizador desenvolvido nesta etapa torna-se a principal ferramenta de inspeção estrutural do projeto, permitindo análise visual rápida de defeitos cristalinos em gelo Ih e servindo como base para futuras investigações envolvendo relaxação estrutural, dinâmica molecular e comparação com materiais de interesse para aplicações espaciais.
