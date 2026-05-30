Etapa 09 — Gelo Ih Aproximado
Etapa 1 — Conceito fisico
O gelo Ih e a fase comum do gelo em condicoes ambientes. Ele possui uma rede
hexagonal e moleculas de agua organizadas por ligacoes de hidrogenio.

Uma molecula de agua possui:

um atomo de oxigenio;
dois atomos de hidrogenio;
geometria angular, com angulo H-O-H de aproximadamente 104,5 graus;
distancia O-H de aproximadamente 0,96 Angstrom.
O gelo Ih real nao e obtido simplesmente repetindo uma molecula H2O qualquer.
Ele envolve:

orientacao molecular;
ligacoes de hidrogenio;
coordenacao aproximadamente tetraedrica;
regras de Bernal-Fowler.
Nesta etapa, o modelo ainda e didatico. O objetivo e colocar moleculas de agua
em uma celula hexagonal para conectar estrutura molecular, celula, periodicidade
e visualizacao.

Etapa 2 — Implementacao computacional
O script 09_gelo_ih_aproximado.py:

cria uma celula hexagonal;
posiciona quatro atomos de oxigenio em coordenadas fracionarias;
adiciona dois hidrogenios ao redor de cada oxigenio;
alterna a orientacao das moleculas;
ativa pbc=True;
salva XYZ e CIF;
gera uma visualizacao HTML interativa.
Arquivos gerados:

structures/gelo_ih_aproximado.xyz;
structures/gelo_ih_aproximado.cif;
figures/gelo_ih_aproximado_interativo.html.
Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/09_gelo_ih_aproximado.py
Depois abra:

figures/gelo_ih_aproximado_interativo.html
Etapa 4 — Explicacao do codigo
A = 7.8
C = 7.3
GAMMA = 120.0
Define uma celula hexagonal didatica.

OH_DISTANCE = 0.96
HOH_ANGLE_DEGREES = 104.5
Define parametros geometricos aproximados da molecula de agua.

water_geometry(...)
Calcula os deslocamentos dos dois hidrogenios em relacao ao oxigenio.

oxygen_fractional_positions = [...]
Define posicoes de oxigenios dentro da celula usando coordenadas fracionarias.

atoms = Atoms(symbols=symbols, positions=positions, cell=cell, pbc=True)
Cria a estrutura atomica com celula e periodicidade.

atoms.wrap()
Move atomos equivalentes para dentro da celula periodica.

write(OUTPUT_CIF, atoms)
Salva a estrutura em formato CIF.

fig.write_html(...)
Gera a visualizacao interativa no navegador.

Etapa 5 — Melhorias futuras
Melhorias importantes:

comparar com parametros cristalograficos reais do gelo Ih;
melhorar a orientacao molecular;
representar ligacoes de hidrogenio entre moleculas;
gerar supercelula do gelo aproximado;
inserir vacancia removendo uma molecula H2O;
preparar exportacao para LAMMPS.
Etapa 6 — Conexao com pesquisa cientifica real
Esta etapa e a primeira estrutura do projeto diretamente ligada ao tema da IC:
gelo Ih. Ainda nao e o modelo final, mas ja combina conceitos essenciais:

molecula H2O + celula hexagonal + periodicidade + visualizacao interativa
Em uma apresentacao de IC, esta etapa pode ser descrita como o primeiro modelo
didatico do gelo Ih, usado para preparar estudos posteriores de supercelulas,
defeitos cristalinos e dinamica molecular.