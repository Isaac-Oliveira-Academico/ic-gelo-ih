Etapa 08 — Condicoes Periodicas de Contorno
Etapa 1 — Conceito fisico
Condicoes periodicas de contorno, ou PBC, permitem representar um material
extenso usando uma caixa finita. A ideia central e:

sai por um lado, entra pelo outro
Isso nao significa que existe uma parede fisica. Significa que a caixa e
interpretada como uma repeticao infinita dela mesma em todas as direcoes
periodicas.

Em cristais, essa ideia e natural: uma celula unitaria repetida no espaco gera
o material ideal. Em simulacoes, usamos PBC para reduzir efeitos de borda.

Etapa 2 — Implementacao computacional
No ASE, ativamos periodicidade com:

atoms.set_pbc(True)
O script 08_condicoes_periodicas.py:

le structures/celula_hexagonal_simples.cif;
garante pbc=True;
salva structures/celula_hexagonal_pbc.cif;
gera figures/condicoes_periodicas.html;
mostra imagens periodicas vizinhas;
demonstra uma posicao cruzando a fronteira e reaparecendo do outro lado.
Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/08_condicoes_periodicas.py
Depois abra:

figures/condicoes_periodicas.html
Etapa 4 — Explicacao do codigo
atoms = read(INPUT_CIF)
Le a celula hexagonal simples.

atoms.set_pbc(True)
Ativa periodicidade nas tres direcoes.

write(OUTPUT_CIF, atoms)
Salva uma versao da estrutura com PBC.

shifts = [a1, -a1, a2, -a2, ...]
Cria deslocamentos para mostrar imagens periodicas da celula.

wrapped_scaled = end_scaled_outside % 1.0
Aplica a ideia matematica de PBC em coordenadas fracionarias. Por exemplo:

1.12 -> 0.12
Isso representa um ponto que ultrapassou a fronteira da celula e reapareceu no
lado equivalente.

Etapa 5 — Melhorias futuras
Melhorias possiveis:

demonstrar PBC nas tres direcoes;
calcular distancia usando convencao da imagem minima;
comparar mic=False e mic=True no ASE;
usar PBC em uma supercelula;
aplicar PBC a uma estrutura aproximada do gelo Ih.
Etapa 6 — Conexao com pesquisa cientifica real
PBC e uma das ideias centrais em dinamica molecular, Monte Carlo e DFT. Sem PBC,
uma simulacao pequena teria muitos efeitos artificiais de superficie. Com PBC,
o sistema se comporta como um pedaco representativo de um material maior.

No estudo do gelo Ih, PBC sera essencial para simular cristais, supercelulas,
defeitos pontuais e futuramente arquivos de entrada para LAMMPS.