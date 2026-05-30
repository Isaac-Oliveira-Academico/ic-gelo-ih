tapa 06 — Supercelula Hexagonal
Etapa 1 — Conceito fisico
Uma celula unitaria e o bloco minimo usado para descrever um cristal. Uma
supercelula e criada quando repetimos essa celula nas direcoes dos vetores de
rede.

Se uma celula possui 2 atomos e repetimos essa celula em 4x4x2, o numero de
atomos passa a ser:

2 x 4 x 4 x 2 = 64 atomos
Essa ideia e essencial em simulacoes de materiais, porque muitos fenomenos nao
podem ser estudados em uma celula muito pequena. Defeitos, vacancias e
deformacoes mecanicas precisam de sistemas maiores.

Etapa 2 — Implementacao computacional
O ASE possui um metodo direto para criar supercelulas:

supercell = atoms.repeat((4, 4, 2))
Esse comando repete:

4 vezes na direcao de a1;
4 vezes na direcao de a2;
2 vezes na direcao de a3.
O script 06_supercelula_hexagonal.py le a celula hexagonal simples e gera:

structures/supercelula_hexagonal_4x4x2.xyz;
structures/supercelula_hexagonal_4x4x2.cif;
figures/supercelula_hexagonal_4x4x2.png.
Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/06_supercelula_hexagonal.py
Etapa 4 — Explicacao do codigo
INPUT_CIF = Path("structures/celula_hexagonal_simples.cif")
Define a celula unitaria que sera repetida.

REPETITIONS = (4, 4, 2)
Define quantas repeticoes serao feitas em cada direcao.

unit_cell = read(INPUT_CIF)
Le a celula hexagonal simples.

supercell = unit_cell.repeat(REPETITIONS)
Cria a supercelula.

write(cif_output, supercell)
Salva a supercelula em formato CIF.

plot_supercell(unit_cell, supercell, figure_output)
Gera uma figura mostrando os pontos repetidos, a caixa da supercelula e a
celula original tracejada.

Etapa 5 — Melhorias futuras
Proximas melhorias:

gerar tambem supercelulas 1x1x1, 2x2x2 e 8x8x4;
criar uma visualizacao interativa da supercelula;
comparar quantidade de atomos e tamanho da celula;
introduzir moleculas de agua no lugar dos pontos didaticos.
Etapa 6 — Conexao com pesquisa cientifica real
LAMMPS, dinamica molecular e estudos de defeitos raramente usam apenas uma
celula unitaria. Supercelulas sao usadas para simular um pedaco maior do
material e reduzir efeitos artificiais de tamanho.

Para a IC, esta etapa prepara diretamente o estudo de vacancias, defeitos
pontuais e propriedades mecanicas em gelo Ih.