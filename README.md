IC Gelo Ih
Repositório inicial de uma Iniciação Científica em Física Computacional e
Ciência dos Materiais, com foco introdutório na estrutura molecular e
cristalina do gelo Ih.

O projeto tem caráter educacional e científico. A proposta é construir,
passo a passo, uma base computacional para compreender coordenadas atômicas,
moléculas de água, células unitárias, redes cristalinas, periodicidade,
supercélulas, visualização 3D e, futuramente, defeitos cristalinos.

Contexto
Este projeto é desenvolvido como parte de uma Iniciação Científica no
Bacharelado em Física da Universidade Federal de Catalão (UFCAT), sob
orientação do Prof. Domingos Lopes da Silva Jr.

A linha geral envolve:

Física Computacional;
Ciência dos Materiais;
Matéria Condensada;
estrutura cristalina do gelo Ih;
visualização científica;
dinâmica molecular em etapas futuras;
defeitos cristalinos em etapas futuras.
Objetivo
Construir uma plataforma inicial em Python para estudar estruturas relacionadas
ao gelo Ih, começando por modelos didáticos e evoluindo progressivamente para
representações mais próximas de sistemas usados em pesquisa computacional de
materiais.

Os objetivos iniciais são:

gerar estruturas moleculares simples;
salvar coordenadas atômicas em formatos científicos;
visualizar estruturas em 3D;
construir células hexagonais;
estudar periodicidade;
gerar supercélulas;
preparar a base para estudos futuros de defeitos e dinâmica molecular.
Ambiente Computacional
O projeto foi desenvolvido em ambiente Linux remoto, acessado via VSCode Remote
SSH, com execução dos scripts em ambiente virtual Python.

Configuração geral:

Python 3.12;
ambiente virtual Python;
NumPy;
Matplotlib;
ASE;
Plotly;
SciPy;
GPU NVIDIA disponível para etapas futuras de simulação.
Por segurança, detalhes privados de rede, usuários, IPs, chaves, caminhos
internos e comandos de montagem remota não são publicados neste repositório.

Estrutura do Projeto
ic-gelo-ih/
├── README.md
├── requirements.txt
├── data/
│   └── rede_gelo_inicial.xyz
├── docs/
├── figures/
├── notes/
├── scripts/
├── structures/
└── tests/
Scripts Desenvolvidos
01 — Rede molecular inicial
Gera uma rede molecular 3D simplificada inspirada no gelo Ih.

Saídas principais:

data/rede_gelo_inicial.xyz;
figures/rede_gelo_inicial.png.
Observação: esta estrutura é didática e ainda não é cristalograficamente
rigorosa.

02 — Validação de XYZ com ASE
Lê o arquivo XYZ inicial usando ASE, mostra o número de átomos, identifica
espécies químicas e calcula distâncias interatômicas.

Conceitos estudados:

objeto Atoms do ASE;
espécies químicas;
coordenadas cartesianas;
distâncias interatômicas.
03 — Exportação de formatos
Exporta a estrutura inicial para formatos usados em visualização e
cristalografia computacional.

Formatos gerados:

XYZ;
PDB;
CIF.
04 — Célula hexagonal simples
Cria uma célula hexagonal didática com vetores de rede e periodicidade.

Conceitos estudados:

célula unitária;
vetores de rede;
coordenadas fracionárias;
simetria hexagonal;
pbc=True.
05 — Visualização interativa da célula
Gera um arquivo HTML interativo para visualizar a célula hexagonal no navegador.

Resultado:

rotação com mouse;
zoom;
inspeção visual dos vetores e pontos da base.
06 — Supercélula hexagonal
Repete a célula hexagonal para formar uma supercélula.

Conceitos estudados:

repetição periódica;
crescimento do número de átomos;
diferença entre célula unitária e supercélula.
07 — Visualização interativa da supercélula
Gera uma visualização HTML interativa da supercélula hexagonal.

08 — Condições periódicas de contorno
Demonstra a ideia de que, em sistemas periódicos, uma partícula que sai por uma
face da célula reaparece pela face oposta.

Conceito central:

sai por um lado, entra pelo outro
08b — Animação de PBC
Gera uma animação HTML mostrando uma partícula cruzando a fronteira da célula e
reaparecendo na posição equivalente.

09 — Gelo Ih aproximado
Cria um primeiro modelo didático de gelo Ih, combinando:

moléculas de água;
célula hexagonal;
periodicidade;
visualização interativa.
Observação: o modelo ainda é aproximado e educacional. Ele não deve ser tratado
como estrutura cristalográfica final do gelo Ih.

10 — Supercélula do gelo Ih aproximado
Repete o modelo aproximado do gelo Ih para construir um sistema molecular maior,
preparando o projeto para estudos de vacâncias e defeitos pontuais.

Como Executar
Clone o repositório:

git clone https://github.com/Isaac-Oliveira-Academico/ic-gelo-ih.git
cd ic-gelo-ih
Crie e ative um ambiente virtual:

python3 -m venv .venv
source .venv/bin/activate
Instale as dependências:

pip install -r requirements.txt
Execute um script, por exemplo:

python scripts/09_gelo_ih_aproximado.py
Os arquivos de saída são gerados principalmente em:

structures/;
figures/;
data/.
Resultados Atuais
O projeto já permite:

gerar uma rede molecular inicial;
validar estruturas com ASE;
exportar arquivos XYZ, PDB e CIF;
construir uma célula hexagonal simples;
gerar supercélulas;
visualizar estruturas em HTML interativo;
demonstrar condições periódicas de contorno;
criar um modelo didático aproximado do gelo Ih.
Aprendizado Científico
Até esta etapa, o projeto documenta conceitos fundamentais para Física
Computacional aplicada à Ciência dos Materiais:

coordenadas atômicas;
molécula de água;
formatos de arquivos atomísticos;
célula unitária;
vetores de rede;
coordenadas fracionárias;
periodicidade;
supercélulas;
visualização científica;
modelo molecular aproximado do gelo Ih.
Próximos Passos
Próximas etapas planejadas:

criar uma supercélula maior do gelo Ih aproximado;
inserir uma vacância molecular;
visualizar defeitos pontuais;
exportar estruturas para LAMMPS;
estudar potenciais interatômicos;
comparar modelos didáticos com dados cristalográficos reais;
preparar a base para dinâmica molecular.
Observação Sobre Segurança
Este repositório não publica detalhes privados de infraestrutura, como:

endereços IP;
usuários de servidores;
caminhos internos de armazenamento;
comandos de montagem remota;
tokens;
senhas;
chaves SSH.
Essas informações devem permanecer em documentação privada local.

Licença
Este projeto está em fase inicial de desenvolvimento acadêmico. A licença será
definida em etapa posterior.