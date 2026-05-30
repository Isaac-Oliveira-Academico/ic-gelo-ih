Etapa 07 — Visualizacao Interativa da Supercelula
Etapa 1 — Conceito fisico
Uma supercelula mostra como a celula unitaria se repete no espaco. Essa
repeticao e a base da ideia de cristal ideal. Ao visualizar uma supercelula,
fica mais claro que o cristal nao e uma molecula isolada, mas um arranjo
periodico.

Nesta etapa, a estrutura ainda e didatica: os pontos representam uma base
simples, nao moleculas reais de agua. Mesmo assim, ela ja contem os conceitos
fundamentais para chegar ao gelo Ih:

vetores de rede;
repeticao espacial;
periodicidade;
crescimento do numero de atomos.
Etapa 2 — Implementacao computacional
O script le:

structures/supercelula_hexagonal_4x4x2.cif
e gera:

figures/supercelula_hexagonal_interativa.html
O arquivo HTML usa Plotly. Isso permite visualizar a supercelula no navegador,
sem depender de uma janela grafica aberta diretamente no G7Node.

Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/07_visualizar_supercelula_interativa.py
Depois, abra no navegador:

figures/supercelula_hexagonal_interativa.html
Etapa 4 — Explicacao do codigo
INPUT_CIF = Path("structures/supercelula_hexagonal_4x4x2.cif")
Define a supercelula que sera visualizada.

atoms = read(INPUT_CIF)
Le o CIF e cria um objeto Atoms.

positions = atoms.get_positions()
Extrai as coordenadas cartesianas de todos os pontos da supercelula.

go.Scatter3d(...)
Cria a nuvem de pontos 3D interativa.

color=positions[:, 2]
Colore os pontos pela coordenada z, ajudando a perceber a profundidade.

hoverinfo="text"
Permite ver informacoes do ponto ao passar o mouse.

fig.write_html(...)
Salva a visualizacao como HTML.

Etapa 5 — Melhorias futuras
Melhorias possiveis:

desenhar tambem as celulas internas da supercelula;
adicionar controles para escolher 1x1x1, 2x2x2, 4x4x2;
trocar pontos didaticos por moleculas de agua;
destacar uma celula unitaria dentro da supercelula.
Etapa 6 — Conexao com pesquisa cientifica real
Supercelulas sao fundamentais para simulacoes de materiais. Defeitos pontuais,
vacancias e dinamica molecular exigem sistemas maiores para reduzir efeitos
artificiais de tamanho.

Para a IC, esta etapa mostra que o projeto ja consegue gerar e visualizar um
cristal periodico didatico em um fluxo remoto reprodutivel:

G7Node -> estrutura CIF -> HTML interativo -> navegador