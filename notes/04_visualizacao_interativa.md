Etapa 05 — Visualizacao Interativa da Celula Hexagonal
Etapa 1 — Conceito fisico
Visualizar uma celula em 3D ajuda a entender que um cristal nao e apenas um
desenho plano. Os vetores a1, a2 e a3 definem direcoes espaciais, e a
base atomica fica posicionada dentro desse bloco.

Rotacionar a estrutura com o mouse ajuda a perceber:

o angulo entre a1 e a2;
a altura da celula na direcao a3;
a diferenca entre coordenadas cartesianas e fracionarias;
a ideia de repeticao periodica.
Etapa 2 — Implementacao computacional
Como o G7Node e acessado remotamente, abrir uma janela grafica com ASE pode
falhar se nao houver configuracao de display. Por isso, esta etapa usa Plotly
para gerar um arquivo HTML interativo.

O HTML pode ser aberto no navegador e permite:

rotacao com mouse;
zoom;
deslocamento da camera;
inspecao dos pontos da base.
Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/05_visualizar_celula_hexagonal.py
Saida esperada:

figures/celula_hexagonal_interativa.html
Etapa 4 — Explicacao do codigo
from ase.io import read
Le o arquivo CIF da celula hexagonal.

import plotly.graph_objects as go
Importa a biblioteca usada para criar graficos 3D interativos.

atoms = read(INPUT_CIF)
Transforma o CIF em um objeto Atoms.

positions = atoms.get_positions()
Extrai as coordenadas cartesianas dos atomos.

add_cell_edges(fig, atoms.cell)
Desenha as arestas da celula.

add_lattice_vectors(fig, atoms.cell)
Desenha os vetores a1, a2 e a3.

fig.write_html(...)
Salva a visualizacao interativa em HTML.

Etapa 5 — Melhorias futuras
Melhorias possiveis:

colorir atomos por elemento quimico;
adicionar supercelulas;
mostrar coordenadas ao passar o mouse;
gerar visualizacoes comparando celula simples e gelo Ih aproximado.
Etapa 6 — Conexao com pesquisa real
Visualizacao cientifica e parte do fluxo real de Ciencia dos Materiais. Antes
de rodar dinamica molecular ou DFT, pesquisadores inspecionam estruturas para
verificar celula, coordenadas, orientacao molecular e possiveis defeitos.

Esta etapa aproxima o projeto de ferramentas como VESTA, OVITO e visualizadores
integrados ao ASE, mas mantendo tudo em Python e em um fluxo reprodutivel.