Fase 1 — Script 03: Exportacao de Formatos
Etapa 1 — Conceito fisico
Uma estrutura atomica pode ser salva em diferentes formatos. Cada formato
carrega um tipo de informacao e foi criado para usos diferentes.

XYZ: formato simples. Guarda numero de atomos, especies quimicas e
coordenadas cartesianas.
PDB: muito usado em moleculas, biomoleculas e visualizadores 3D.
CIF: formato cristalografico. Normalmente guarda celula unitaria, simetria
e coordenadas relacionadas ao cristal.
Nesta etapa, a estrutura ainda nao e uma celula unitaria fisica do gelo Ih.
Por isso, ao exportar CIF, usamos uma caixa auxiliar ao redor dos atomos.
Essa caixa ajuda o arquivo a ser lido por programas cristalograficos, mas ainda
nao deve ser interpretada como a celula real do gelo.

Etapa 2 — Implementacao computacional
O ASE le a estrutura com read e exporta com write.

O script:

le data/rede_gelo_inicial.xyz;
verifica se existe celula definida;
cria uma caixa auxiliar se a celula nao existir;
salva a estrutura em structures/rede_gelo_inicial.xyz;
salva a estrutura em structures/rede_gelo_inicial.pdb;
salva a estrutura em structures/rede_gelo_inicial.cif.
Etapa 3 — Como executar
No G7Node, dentro do projeto:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/03_exportar_formatos.py
Etapa 4 — Explicacao do codigo
from pathlib import Path
Cria caminhos de arquivo de forma legivel e independente do sistema.

import numpy as np
Usado para montar uma matriz diagonal da caixa auxiliar.

from ase.io import read, write
Importa as funcoes do ASE para ler e escrever estruturas atomicas.

INPUT_XYZ = Path("data/rede_gelo_inicial.xyz")
OUTPUT_DIR = Path("structures")
Define o arquivo de entrada e a pasta de saida.

atoms = read(INPUT_XYZ)
Le o arquivo XYZ e cria um objeto Atoms.

atoms.cell.volume > 0.0
Verifica se o objeto possui uma celula com volume diferente de zero.

positions.min(axis=0)
positions.max(axis=0)
Encontra os limites espaciais da estrutura nas direcoes x, y e z.

atoms.set_cell(np.diag(cell_lengths))
Define uma caixa retangular auxiliar.

atoms.set_pbc(False)
Mantem a estrutura sem periodicidade. A caixa e apenas auxiliar.

write(cif_output, export_atoms)
Exporta a estrutura no formato CIF.

Etapa 5 — Melhorias futuras
Melhorias naturais:

comparar os arquivos gerados em um visualizador;
abrir o .pdb ou .cif no ASE;
criar uma celula unitaria fisica, nao apenas uma caixa auxiliar;
salvar metadados explicando que a estrutura ainda e didatica.
Etapa 6 — Conexao com pesquisa real
Formatos de arquivo sao parte essencial da pesquisa computacional. Um mesmo
modelo pode precisar passar por ASE, VESTA, OVITO, LAMMPS, pymatgen ou outros
programas. Aprender a exportar formatos e o primeiro passo para construir um
fluxo reprodutivel de Ciencia dos Materiais.

Em uma apresentacao de IC, esta etapa mostra que o projeto ja consegue
transformar uma estrutura atomica em formatos usados pela comunidade.