# Explicação do código do simulador - By Macanhan

## 1. Importação e inicialização

````python
import pygame
import random
import math

pygame.init()
````
- <b><i>pygame</i></b>: biblioteca que usamos para fazer a janela e os desenhos (como robô, parede, etc).

- <b><i>random</i></b>: usada para gerar posições aleatórias para os obstáculos e direções do robô.

- <b><i>math</i></b>: usada para fazer contas matemáticas mais complexas, como a distância entre dois pontos.

## 2. Tamanho do Ambiente

````python
largura_total, altura_total = 600, 600
tamanho_sala = 400
tamanho_celula = 40
linhas = tamanho_sala // tamanho_celula
colunas = tamanho_sala // tamanho_celula
````
- A tela tem 600 por 600 pixels.

- O ambiente, onde o robô se move, é um quadrado de 400 pixels no meio da tela.

- Cada célula tem 40 pixels, então a sala terá:

- 400 ÷ 40 = 10 linhas

- 400 ÷ 40 = 10 colunas
- Ou seja, temos um tabuleiro de 10x10 quadrados.

## 3. Centralizando o ambiente na tela
````python
offset_x = (largura_total - tamanho_sala) // 2
offset_y = (altura_total - tamanho_sala) // 2
````
Esses cálculos servem para posicionar a sala bem no centro da tela.

- (600 - 400) // 2 = 100

- Isso quer dizer que a sala começa 100 pixels depois do canto esquerdo e de cima da tela.

## 4. Cores Usadas
````python
COR_FUNDO = (230, 230, 230)
COR_SALA = (250, 250, 250)
COR_PAREDE = (120, 120, 120)
COR_OBSTACULO = (200, 50, 50)
COR_ROBO = (30, 144, 255)
````

## 5. Criando a Tela
````python
tela = pygame.display.set_mode((largura_total, altura_total))
pygame.display.set_caption("Simulador 2D - RAS")
````
- Cria a janela do jogo com o tamanho de 600x600 pixels.

- Coloca um nome no topo da janela.

## 6. Gerando Obstáculos

````python
obstaculos = []
espacos_livres = [(x, y) for x in range(linhas) for y in range(colunas) if (x, y) != (1, 1)]
random.shuffle(espacos_livres)
for i in range(12): 
    obstaculos.append(espacos_livres[i])
````

- Aqui o código cria 12 obstáculos aleatórios, sem ocupar a posição (1, 1), onde o robô começa.

### Cálculos:
- range(linhas) → vai de 0 a 9 (10 linhas)

- range(colunas) → vai de 0 a 9 (10 colunas)

- Isso cria uma lista com todas as posições possíveis da sala, menos (1,1)

## 7. Posição inicial do robô

````python
robo_pos_grid = [1, 1]
direcoes = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
direcao_atual = random.choice(direcoes)
````
Esses pares representam:

- (1, 0) → descer

- (-1, 0) → subir

- (0, 1) → direita

- (0, -1) → esquerda

- (1,1) / (-1,-1) → diagonais

## 8. Cálculo da posição real 

````python
robo_pos_real = [
    offset_x + robo_pos_grid[0] * tamanho_celula + tamanho_celula // 2,
    offset_y + robo_pos_grid[1] * tamanho_celula + tamanho_celula // 2
]
````

robo_pos_grid[0] * tamanho_celula → posição do robô em pixels (baseado na célula).

+ tamanho_celula // 2 → leva o robô até o centro da célula, e não à borda.

+ offset_x → desloca a posição, porque a sala está centralizada na janela do jogo (600x600 pixels).

## 9. Função que verifica se o robô pode se mover

````python
def pode_mover(pos):
    x, y = pos
    return (
        0 <= x < linhas and
        0 <= y < colunas and
        (x, y) not in obstaculos
    )
````
Aqui o códiguin:

- Checa se a posição está dentro da sala

- Checa se não tem obstáculo nessa posição

 ## 10. Função que desenha tudo na tela

````python
 def desenhar():
    tela.fill(COR_FUNDO)

   
    pygame.draw.rect(tela, COR_PAREDE, (offset_x - 5, offset_y - 5, tamanho_sala + 10, tamanho_sala + 10), border_radius=10)
    pygame.draw.rect(tela, COR_SALA, (offset_x, offset_y, tamanho_sala, tamanho_sala), border_radius=10)

   
    for (x, y) in obstaculos:
        rect = pygame.Rect(offset_x + x * tamanho_celula + 5,
                           offset_y + y * tamanho_celula + 5,
                           tamanho_celula - 10,
                           tamanho_celula - 10)
        pygame.draw.rect(tela, COR_OBSTACULO, rect, border_radius=8)

   
    pygame.draw.circle(tela, COR_ROBO, (int(robo_pos_real[0]), int(robo_pos_real[1])), tamanho_celula // 3)

    pygame.display.flip()
````

 Essa função desenha:

- A parede da sala (com borda)

- Os obstáculos (pequenos quadrados vermelhos)

- O robô (um círculo azul no centro da célula)

  ## 11. Laço principal do programa
  
````python
clock = pygame.time.Clock()
rodando = True
velocidade = 2 
while rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False


    alvo_real = [offset_x + robo_pos_grid[0] * tamanho_celula + tamanho_celula // 2,
                 offset_y + robo_pos_grid[1] * tamanho_celula + tamanho_celula // 2]

    dist = math.hypot(robo_pos_real[0] - alvo_real[0], robo_pos_real[1] - alvo_real[1])

    if dist < 2:
        nova_direcao = direcao_atual
        nova_pos = [robo_pos_grid[0] + nova_direcao[0], robo_pos_grid[1] + nova_direcao[1]]

        tentativas = 0
        while not pode_mover(nova_pos) and tentativas < len(direcoes):
            nova_direcao = random.choice(direcoes)
            nova_pos = [robo_pos_grid[0] + nova_direcao[0], robo_pos_grid[1] + nova_direcao[1]]
            tentativas += 1

        if pode_mover(nova_pos):
            robo_pos_grid = nova_pos
            direcao_atual = nova_direcao


    dx = alvo_real[0] - robo_pos_real[0]
    dy = alvo_real[1] - robo_pos_real[1]
    distancia = math.hypot(dx, dy)
    if distancia != 0:
        robo_pos_real[0] += dx / distancia * velocidade
        robo_pos_real[1] += dy / distancia * velocidade

    desenhar()
    
````
- clock.tick(60) → limita o programa a 60 atualizações por segundo.

- velocidade = 2 → o robô anda 2 pixels por frame.

##  12. Cálculo de distância até o centro da célula

````python
alvo_real = [...]
dist = math.hypot(robo_pos_real[0] - alvo_real[0], robo_pos_real[1] - alvo_real[1])
````

- math.hypot(dx, dy) → calcula a distância entre dois pontos (em linha reta).

- Isso serve para saber se o robô chegou no centro da célula.

## 13. Escolher nova direção se bater em obstáculo
````python
nova_direcao = direcao_atual
nova_pos = [robo_pos_grid[0] + nova_direcao[0], robo_pos_grid[1] + nova_direcao[1]]

tentativas = 0
while not pode_mover(nova_pos) and tentativas < len(direcoes):
    nova_direcao = random.choice(direcoes)
    nova_pos = [robo_pos_grid[0] + nova_direcao[0], robo_pos_grid[1] + nova_direcao[1]]
    tentativas += 1
````

Esse trecho:

- Tenta mover o robô na mesma direção.

- Se tiver obstáculo, tenta outra direção aleatória.

- Repete até achar uma direção válida ou testar todas.

  ## 14. Mover suavemente o robô com base na distância
 ````python
dx = alvo_real[0] - robo_pos_real[0]
dy = alvo_real[1] - robo_pos_real[1]
distancia = math.hypot(dx, dy)
if distancia != 0:
    robo_pos_real[0] += dx / distancia * velocidade
    robo_pos_real[1] += dy / distancia * velocidade
  ````
- dx e dy são as diferenças horizontais e verticais.


## Glossário de termos do código

| Termo/Código                        | Significado                                                                 |
|------------------------------------|------------------------------------------------------------------------------|
| `import`                           | Importa bibliotecas para usar funções prontas (ex: `math`, `pygame`, `random`). |
| `pygame.init()`                    | Inicializa todos os módulos do Pygame.                                      |
| `range(n)`                         | Gera números de 0 até n-1.                                                  |
| `for x in lista:`                  | Laço que percorre cada item da lista.                                       |
| `if`, `elif`, `else`               | Condições: se, senão se, senão.                                             |
| `and`, `or`, `not`                 | Operadores lógicos (e, ou, não).                                            |
| `def nome():`                      | Cria uma função (bloco de código reutilizável).                             |
| `math.hypot(x, y)`                 | Calcula a distância entre dois pontos (usando Pitágoras).                   |
| `random.choice(lista)`             | Escolhe um item aleatório da lista.                                         |
| `random.shuffle(lista)`            | Embaralha a ordem dos itens da lista.                                       |
| `pygame.draw.rect()`               | Desenha um retângulo na tela.                                               |
| `pygame.draw.circle()`             | Desenha um círculo na tela.                                                 |
| `pygame.display.set_mode()`        | Cria a janela do jogo com a resolução escolhida.                            |
| `pygame.event.get()`               | Captura eventos (como fechar a janela).                                     |
| `pygame.QUIT`                      | Evento de "fechar o jogo".                                                  |
| `pygame.display.flip()`            | Atualiza o conteúdo da tela.                                                |
| `pygame.time.Clock()`              | Controla o tempo do jogo (FPS).                                             |
| `clock.tick(60)`                   | Limita o jogo a 60 frames por segundo.                                      |
| `+=`, `-=`                         | Aumenta/diminui e já atribui (`x += 1` é igual a `x = x + 1`).              |
| `//`                               | Divisão inteira (retorna só a parte inteira).                               |
| `[x, y]`                           | Lista mutável (pode mudar).                                                 |
| `(x, y)`                           | Tupla imutável (valor fixo).                                                |
| `(x, y) not in lista`              | Verifica se a posição NÃO está na lista.                                    |

- dx / distancia e dy / distancia → transformam isso em um vetor de direção unitário.

- Multiplica por velocidade = 2 → o robô anda 2 pixels na direção certa, sem sair do caminho.
