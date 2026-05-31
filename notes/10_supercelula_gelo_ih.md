Etapa 10 — Supercelula do Gelo Ih Aproximado
Etapa 1 — Conceito fisico
Uma celula pequena ajuda a entender a geometria local, mas nao e suficiente
para estudar defeitos. Para investigar vacancias, intersticiais ou deformacao,
precisamos de um sistema maior. Esse sistema maior e chamado de supercelula.

Nesta etapa, repetimos o modelo aproximado de gelo Ih em 3x3x2.

Como a celula da etapa 09 possui 4 moleculas de agua:

4 moleculas x 3 x 3 x 2 = 72 moleculas H2O
Como cada molecula tem 3 atomos:

72 moleculas x 3 atomos = 216 atomos
Etapa 2 — Implementacao computacional
O ASE cria supercelulas com:

supercell = unit_cell.repeat((3, 3, 2))
O script 10_supercelula_gelo_ih.py:

le structures/gelo_ih_aproximado.cif;
repete a estrutura em 3x3x2;
salva XYZ e CIF;
gera HTML interativo;
imprime numero de atomos, oxigenios, hidrogenios e moleculas.
Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/10_supercelula_gelo_ih.py
Depois abra:

figures/supercelula_gelo_ih_3x3x2_interativa.html
Etapa 4 — Explicacao do codigo
INPUT_CIF = Path("structures/gelo_ih_aproximado.cif")
Define o modelo aproximado do gelo Ih que sera repetido.

REPETITIONS = (3, 3, 2)
Define a repeticao da celula nas direcoes dos vetores de rede.

unit_cell = read(INPUT_CIF)
Le a celula molecular aproximada.

supercell = unit_cell.repeat(REPETITIONS)
Cria a supercelula.

write(OUTPUT_CIF, supercell)
Salva a supercelula para uso posterior.

create_interactive_view(supercell)
Gera uma visualizacao HTML interativa.

Etapa 5 — Melhorias futuras
Proximas melhorias:

criar versoes 2x2x2, 4x4x2 e 4x4x4;
otimizar a visualizacao para muitos atomos;
destacar uma molecula especifica;
remover uma molecula para criar uma vacancia;
exportar a estrutura para LAMMPS.
Etapa 6 — Conexao com pesquisa cientifica real
Supercelulas sao essenciais em simulacoes de materiais. Para estudar defeitos
no gelo Ih, precisamos de um cristal suficientemente grande para que a remocao
de uma molecula nao represente uma perturbacao artificial exagerada.

Esta etapa prepara diretamente a primeira investigacao de defeitos pontuais:
uma vacancia molecular.