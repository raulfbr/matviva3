"""
Data Corpus - Realistic Examples for Validator Testing
Contains 'Gold Standard' (Compliant) and 'Failure' (Non-compliant) examples
for each pedagogical persona.
"""

# --- CHARLOTTE MASON EXAMPLES ---

MASON_COMPLIANT = """
Era uma manhã fria de inverno quando Cristóvão Colombo avistou pela primeira vez as luzes
estranhas no horizonte. Ele não sabia, mas aquele pequeno brilho oscilante mudaria o mapa do mundo para sempre.
Os marinheiros, cansados e com medo de cair na borda da terra, murmuravam entre si, mas o almirante
permaneceu firme no convés, observando o mistério que se desdobrava diante de seus olhos.
"""

MASON_NON_COMPLIANT_LIST = """
Aqui estão os fatos principais sobre Cristóvão Colombo:
- Ele nasceu em Gênova.
- Descobriu a América em 1492.
- Fez quatro viagens no total.
- Morreu sem saber que tinha descoberto um novo continente.
Isso é muito importante para a prova.
"""

MASON_NON_COMPLIANT_TWADDLE = """
Oi galerinha! Vamos aprender sobre o Colombo? Foi super legal!
Ele pegou o barquinho dele e foi navegar. É moleza entender isso, né?
A viagem foi muito divertida e todo mundo ficou feliz.
"""

# --- SINGAPORE MATH EXAMPLES ---

# Phase: CONCRETE
SINGAPORE_CONCRETE_COMPLIANT = """
Imagine que você tem três maçãs vermelhas brilhantes na mesa.
Agora, sua mãe coloca mais duas maçãs verdes ao lado delas.
Se você juntar todas as maçãs na cesta, quantas frutas você vê?
Conte com seus dedos se precisar.
"""

SINGAPORE_CONCRETE_NON_COMPLIANT = """
Para resolver isso, você só precisa fazer 3 + 2.
Sabemos que 3 + 2 é igual a 5.
Escreva o número 5 no caderno.
"""

# Phase: PICTORIAL
SINGAPORE_PICTORIAL_COMPLIANT = """
Vamos desenhar isso para entender melhor.
[BAR MODEL]
Total: ?
+-------+-----+
|   3   |  2  |
+-------+-----+
A barra maior representa as maçãs vermelhas. A menor, as verdes.
O comprimento total da barra nos diz quantas maçãs temos ao todo.
"""

SINGAPORE_PICTORIAL_NON_COMPLIANT = """
A resposta é 5.
3 + 2 = 5.
Não precisa desenhar nada, é só calcular de cabeça.
"""

# --- C.S. LEWIS EXAMPLES ---

LEWIS_COMPLIANT = """
A fé, parece-me, não é uma tentativa de acreditar em algo que você sabe que não é verdade.
Imagine que você está segurando um mapa num dia de nevoeiro. Você não consegue ver a estrada,
mas confia no mapa porque ele foi desenhado por alguém que viu a estrada num dia de sol.
A fé é essa teimosia em seguir o mapa mesmo quando os seus olhos só veem neblina.
"""

LEWIS_NON_COMPLIANT = """
A fé é a certeza das coisas que se esperam e a prova das coisas que não se veem.
É um conceito teológico fundamental para a salvação e deve ser praticado diariamente
para garantir a eficácia da graça.
"""
