Roadmap da IC — Gelo Ih
Fase 0 — Infraestrutura concluida
Estado atual:

Linux remoto;
SSH;
VSCode Remote;
Git e GitHub;
Python;
ambiente virtual;
ASE instalado no ambiente do projeto;
primeira visualizacao molecular gerada.
Resultados ja obtidos:

figures/rede_gelo_inicial.png;
data/rede_gelo_inicial.xyz.
Fase 1 — Manipulacao de estruturas atomicas com ASE
Objetivo cientifico: entender que uma estrutura atomica computacional e formada
por especies quimicas e coordenadas.

Objetivo computacional: dominar o objeto Atoms do ASE.

Entrega atual:

scripts/02_validar_xyz_ase.py.
O script le o arquivo XYZ, imprime informacoes da estrutura e calcula distancias
interatomicas.

Proxima entrega:

scripts/03_exportar_formatos.py, convertendo xyz, cif e pdb.
Fase 2 — Cristalografia computacional
Conceitos:

rede de Bravais;
base atomica;
celula unitaria;
vetores de rede a1, a2, a3;
simetria.
Perguntas-guia:

onde ficam os pontos da rede?
o que colocamos em cada ponto?
qual e o bloco minimo que reproduz o cristal?
Fase 3 — Primeira celula hexagonal
Entrega:

scripts/04_celula_hexagonal.py.
Objetivo: criar uma celula hexagonal simples com parametros a, b, c,
alpha, beta e gamma, usando gamma = 120 graus.

Aprendizado:

simetria hexagonal;
vetores de rede;
periodicidade.
Fase 4 — Estrutura aproximada do gelo Ih
Entrega:

scripts/05_gelo_ih_aproximado.py.
Objetivo: gerar moleculas de agua em posicoes inspiradas na celula do gelo Ih.

Pontos fisicos importantes:

rede hexagonal;
moleculas H2O;
coordenacao tetraedrica;
ligacoes de hidrogenio;
regras de Bernal-Fowler.
Fase 5 — Visualizador cientifico interativo
Entrega:

scripts/06_viewer_gelo.py.
Objetivo: abrir uma visualizacao 3D interativa com rotacao, zoom e inspecao.

Ferramentas:

ase.visualize.view;
opcionalmente Matplotlib para visualizacoes customizadas.
Fase 6 — Supercelulas
Entrega:

scripts/07_supercelula.py.
Objetivo: gerar sistemas 1x1x1, 2x2x2, 4x4x4 e 8x8x8.

Aprendizado:

repeticao periodica;
escalabilidade;
diferenca entre celula unitaria e cristal maior.
Fase 7 — Condicoes periodicas de contorno
Entrega:

scripts/08_pbc.py.
Objetivo: ativar e visualizar atoms.set_pbc(True).

Conceito fisico:

um atomo que sai por um lado da caixa entra pelo outro lado.
Importancia:

dinamica molecular;
Monte Carlo;
DFT.
Fase 8 — Defeitos pontuais
Entrega:

scripts/09_vacancia.py.
Objetivo: remover uma molecula de agua e visualizar uma vacancia.

Conexao cientifica:

defeitos cristalinos;
propriedades mecanicas;
plasticidade.
Fase 9 — Exportacao para LAMMPS
Entrega:

scripts/10_export_lammps.py;
lammps/gelo.data.
Objetivo: exportar a estrutura para um formato que pode ser usado em dinamica
molecular com LAMMPS.

Fase 10 — Estrutura pronta para dinamica molecular
O projeto passa a conter:

estrutura cristalina;
celula periodica;
supercelula;
defeito;
arquivo para LAMMPS.
Nesse ponto, a ponte cientifica esta montada:

Cristalografia -> Fisica do Estado Solido -> Defeitos Cristalinos ->
Dinamica Molecular.

Marco dos proximos 10 dias
Entregas recomendadas:

gerar celula hexagonal simples com ASE;
gerar supercelula 4x4x4;
abrir visualizador 3D interativo;
inserir uma vacancia;
exportar para formato LAMMPS.