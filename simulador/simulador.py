import pygame
import random
import math

pygame.init()

largura_total, altura_total = 600, 600
tamanho_sala = 400
tamanho_celula = 40
linhas = tamanho_sala // tamanho_celula
colunas = tamanho_sala // tamanho_celula


offset_x = (largura_total - tamanho_sala) // 2
offset_y = (altura_total - tamanho_sala) // 2


COR_FUNDO = (230, 230, 230)
COR_SALA = (250, 250, 250)
COR_PAREDE = (120, 120, 120)
COR_OBSTACULO = (200, 50, 50)
COR_ROBO = (30, 144, 255)


tela = pygame.display.set_mode((largura_total, altura_total))
pygame.display.set_caption("Simulador 2D em Sala - RAS")


obstaculos = []
espacos_livres = [(x, y) for x in range(linhas) for y in range(colunas) if (x, y) != (1, 1)]
random.shuffle(espacos_livres)
for i in range(12): 
    obstaculos.append(espacos_livres[i])


robo_pos_grid = [1, 1]
direcoes = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
direcao_atual = random.choice(direcoes)


robo_pos_real = [offset_x + robo_pos_grid[0] * tamanho_celula + tamanho_celula // 2,
                 offset_y + robo_pos_grid[1] * tamanho_celula + tamanho_celula // 2]

def pode_mover(pos):
    x, y = pos
    return (
        0 <= x < linhas and
        0 <= y < colunas and
        (x, y) not in obstaculos
    )

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

pygame.quit()
