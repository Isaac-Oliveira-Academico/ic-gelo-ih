Etapa 08b — Animacao de PBC
Etapa 1 — Conceito fisico
A visualizacao anterior mostrava as condicoes periodicas de contorno de forma
estatica. Esta etapa adiciona uma animacao para mostrar o que acontece quando
uma particula cruza a fronteira da celula.

Em coordenadas fracionarias, a celula vai de 0 ate 1 em cada direcao. Se uma
particula passa para 1.12 na direcao a1, a posicao equivalente dentro da
celula e:

1.12 modulo 1 = 0.12
Fisicamente, isso representa a ideia:

sai por um lado, entra pelo outro
Etapa 2 — Implementacao computacional
O script 08b_animacao_pbc.py usa Plotly para criar um HTML com botao de play.

Ele mostra duas posicoes:

ponto laranja: movimento sem aplicar PBC;
ponto verde: posicao equivalente com PBC.
Quando a coordenada fracionaria passa de 1.0, o ponto verde reaparece no lado
oposto da celula.

Etapa 3 — Como executar
No G7Node:

cd ~/latitude-dados/startup-cientifica/ic-gelo-ih
source ~/.venvs/ic-gelo-ih/bin/activate
python scripts/08b_animacao_pbc.py
Depois abra:

figures/animacao_pbc.html
Etapa 4 — Explicacao do codigo
START_FRACTIONAL_X = 0.75
END_FRACTIONAL_X = 1.25
Define o movimento da particula em coordenada fracionaria na direcao a1.

wrapped_fractional = unwrapped_fractional % 1.0
Aplica a regra periodica. Valores maiores que 1 voltam para dentro da celula.

fractional_to_cartesian(...)
Converte coordenadas fracionarias para coordenadas cartesianas, permitindo
desenhar a posicao no espaco 3D.

go.Frame(...)
Cria cada quadro da animacao.

fig.write_html(...)
Salva a animacao como HTML.

Etapa 5 — Melhorias futuras
Melhorias possiveis:

animar o movimento nas direcoes a2 e a3;
mostrar a distancia por imagem minima;
adicionar trajetorias moleculares;
aplicar a animacao a uma supercelula;
usar moleculas de agua em vez de um ponto didatico.
Etapa 6 — Conexao com pesquisa cientifica real
Em dinamica molecular, atomos e moleculas se movem continuamente. Quando cruzam
as fronteiras da caixa de simulacao, as condicoes periodicas mantem a
continuidade do sistema. Esse conceito sera essencial antes de exportar
estruturas para LAMMPS.