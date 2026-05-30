Etapa 04 — Celula Hexagonal Simples
Etapa 1 — Conceito fisico
Uma celula unitaria e o bloco geometrico minimo que, repetido no espaco,
constroi um cristal ideal. Ela e definida por tres vetores de rede:

a1;
a2;
a3.
No sistema hexagonal, os dois vetores da base possuem o mesmo comprimento:

a = b;
gamma = 120 graus;
alpha = beta = 90 graus.
Isso cria uma geometria diferente de uma caixa retangular. Essa diferenca e
central para entender o gelo Ih, pois o gelo comum possui simetria hexagonal.

Nesta etapa, ainda nao estamos construindo o gelo Ih real. Estamos construindo
uma celula hexagonal didatica para aprender a representar vetores de rede,
coordenadas fracionarias e periodicidade.

Etapa 2 — Implementacao computacional
O ASE representa uma celula usando o objeto Atoms com:

especies quimicas;
coordenadas;
matriz de celula;
condicoes periodicas de contorno.
O script 04_celula_hexagonal.py cria:

uma celula hexagonal com a = b = 4.5 Angstrom;
altura c = 7.3 Angstrom;
angulo gamma = 120 graus;
dois pontos atomicos didaticos dentro da celula;
pbc=True, indicando periodicidade.
O script salva:

structures/celula_hexagonal_simples.xyz;
structures/celula_hexagonal_simples.cif;
figures/celula_hexagonal_simples.png.
Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/04_celula_hexagonal.py
Etapa 4 — Explicacao do codigo
from ase import Atoms
Importa o objeto principal usado pelo ASE para representar estruturas atomicas.

from ase.geometry import cellpar_to_cell
Converte os parametros de celula a, b, c, alpha, beta, gamma em uma
matriz de vetores de rede.

A = 4.5
C = 7.3
GAMMA = 120.0
Define uma celula hexagonal didatica. Os valores sao aproximados e usados para
aprendizado de geometria, nao como parametros finais do gelo Ih.

cell = cellpar_to_cell([A, A, C, ALPHA, BETA, GAMMA])
Cria a matriz da celula. Como A aparece duas vezes, temos a = b.

fractional_positions = np.array(...)
Define posicoes fracionarias. Coordenadas fracionarias descrevem posicoes em
relacao aos vetores da celula, nao diretamente em x, y, z.

atoms = Atoms(..., scaled_positions=fractional_positions, cell=cell, pbc=True)
Cria a estrutura com celula e periodicidade.

write(cif_output, atoms)
Exporta a estrutura para CIF, agora com uma celula real do ponto de vista
computacional.

plot_hexagonal_cell(atoms, figure_output)
Gera uma figura 3D mostrando os pontos da base e as arestas da celula.

Etapa 5 — Melhorias futuras
Proximas melhorias:

desenhar tambem a vista superior da celula;
criar uma supercelula 2x2x1;
substituir os pontos didaticos por moleculas de agua;
comparar essa celula didatica com parametros reais do gelo Ih;
abrir a estrutura em um visualizador 3D interativo.
Etapa 6 — Conexao com pesquisa cientifica real
Cristais reais sao descritos por celula unitaria, simetria e base atomica. Em
simulacoes de materiais, essa representacao e usada antes de dinamica molecular,
DFT ou estudos de defeitos.

Para a IC, esta etapa e a ponte entre arquivos moleculares simples e estruturas
cristalinas. Em uma apresentacao, ela pode ser mostrada como o primeiro modelo
periodico do projeto, destacando os vetores de rede e o papel da simetria
hexagonal no estudo do gelo Ih.