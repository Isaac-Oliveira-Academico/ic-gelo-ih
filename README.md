# IC Gelo Ih

Repositório inicial da Iniciação Científica em Física Computacional e Ciência dos Materiais, com foco introdutório na estrutura molecular/cristalina do gelo Ih.

## Objetivo

Construir um ambiente computacional remoto para estudar, programar e visualizar estruturas relacionadas ao gelo Ih usando Python.

## Arquitetura Computacional
CLOUD

Estou desenvolvendo uma Iniciação Científica em Física Computacional e Ciência dos Materiais, com foco inicial em estrutura molecular/cristalina do gelo Ih, orientada pelo Prof. Domingos Lopes da Silva Jr. O objetivo inicial é demonstrar capacidade computacional: configurar ambiente remoto, versionar código, gerar coordenadas moleculares e visualizar uma estrutura 3D simples em Python.

Infraestrutura configurada:
- MacBook como estação principal.
- VSCode conectado via Remote SSH ao servidor Latitude.
- Latitude hostname: aivgo-tech.
- Latitude LAN IP: 192.168.0.105.
- Latitude Tailscale IP: 100.99.53.125.
- Cofre no Latitude: /mnt/cofre/dados.
- G7Node hostname: aivgo-g7node.
- G7Node usado como nó de execução.
- GPU do G7Node: NVIDIA GeForce GTX 1050 Ti, 4 GB VRAM.
- Driver NVIDIA: 535.309.01.
- CUDA runtime reportado por nvidia-smi: 12.2.
- Python no G7Node: 3.12.3.

Fluxo operacional:
- Edito arquivos no VSCode via SSH no Latitude.
- Projeto no Latitude: /mnt/cofre/dados/startup-cientifica/ic-gelo-ih.
- No G7Node, o cofre do Latitude foi montado via SSHFS em:
  /home/vingo/latitude-dados.
- Caminho do projeto no G7Node:
  /home/vingo/latitude-dados/startup-cientifica/ic-gelo-ih.
- Comando de montagem usado no G7Node:
  sshfs vingo@100.99.53.125:/mnt/cofre/dados ~/latitude-dados -o reconnect,ServerAliveInterval=15,ServerAliveCountMax=3.

Ambiente Python:
- venv criada localmente no G7Node em:
  ~/.venvs/ic-gelo-ih.
- Para ativar:
  source ~/.venvs/ic-gelo-ih/bin/activate.
- Dependências instaladas:
  numpy, matplotlib, ase, scipy e dependências do requirements.txt.

Repositório:
- Nome: ic-gelo-ih.
- GitHub: https://github.com/Isaac-Oliveira-Academico/ic-gelo-ih.
- Branch principal: main.
- Commits importantes:
  - Configura ambiente inicial da IC e visualizacao molecular.
  - Adiciona primeira visualizacao molecular do gelo.
  - Documenta setup inicial da IC.
  - Integra repositório local com GitHub.

Estrutura do projeto:
ic-gelo-ih/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   └── rede_gelo_inicial.xyz
├── figures/
│   └── rede_gelo_inicial.png
├── notes/
│   └── 00_setup_inicial.md
├── runs/
└── scripts/
    └── 01_plot_rede_inicial.py

Primeiro resultado:
- scripts/01_plot_rede_inicial.py gera uma rede molecular 3D simplificada inspirada no gelo Ih.
- Saídas:
  data/rede_gelo_inicial.xyz
  figures/rede_gelo_inicial.png.
- Importante: a estrutura ainda não é cristalograficamente rigorosa; é um exercício inicial para entender coordenadas atômicas, moléculas de água, visualização 3D e fluxo computacional.

Como executar no G7Node:
cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/01_plot_rede_inicial.py

Próximos passos desejados:
1. Melhorar o README para reprodução por terceiros.
2. Criar script 02 para ler e validar arquivos XYZ com ASE.
3. Exportar estruturas em formatos úteis para visualizadores científicos.
4. Construir uma célula hexagonal aproximada do gelo Ih.
5. Estudar redes de Bravais, célula unitária e parâmetros cristalográficos.
6. Criar visualizações de defeitos simples, como vacância.
7. Preparar base futura para LAMMPS e Quantum ESPRESSO.

8. ### Gelo Ih
