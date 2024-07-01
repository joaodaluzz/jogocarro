import pygame, sys
from button import Button
import random
from pygame.locals import *
import time

recorde = [0]
pontuacao = 0

pygame.init()

# criando janela
largura = 500
altura = 700
tamanho_janela = (largura, altura)
janela = pygame.display.set_mode(tamanho_janela)
pygame.display.set_caption("RUN-CAR\n joão da luz martins")

BG = pygame.image.load("assets/teladeinicio.png")
GM = pygame.image.load("assets/tela.gameover.png")
garagem_fundo = pygame.image.load('assets/tela.garagem.png')

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# CRIANDO BARULHO DOS BOTOES

som_botao = pygame.mixer.Sound('assets/botao.som.mp3')

# CRIANDO BARULHO DO CARRO BATENDO

batida = pygame.mixer.Sound('assets/batida.mp3')

# MUSICAS DO JOGO
musica_jogo = pygame.mixer.Sound('assets/musica.jogo.mp3')
musica_menu = pygame.mixer.Sound('assets/musica.menu.mp3')
musica_gameover = pygame.mixer.Sound('assets/musica.gameover.mp3')

# CARRO INICIAL

carrousuario = pygame.image.load("assets/carrousuario.png")

# O JOGO EM SI
def play():
    global pontuacao
    running = True
    
    # TELA DO JOGO

    # colors
    cinza = (100, 100, 100)
    verde = (76, 208, 56)
    vermelho = (200, 0, 0)
    branco = (255, 255, 255)
    amarelo = (255, 232, 0)

    # road and marker sizes
    largura_estrada = 300
    largura_marcador = 10
    altura_marcador = 50

    # pistas
    pista_esquerda = 150
    pista_centro = 250
    pista_direita = 350
    pistas = [pista_esquerda, pista_centro, pista_direita]

    # estrada e marcadores
    estrada = (100, 0, largura_estrada, altura)
    marcador_borda_esquerda = (95, 0, largura_marcador, altura)
    marcador_borda_direita = (395, 0, largura_marcador, altura)

    # animar as linhas
    movimento_pista_y = 0

    # Coordenadas do jogador (inicio)
    jogador_x = 250
    jogador_y = 600

    # Configurações de frame
    clock = pygame.time.Clock()
    fps = 120

    # configurações do jogo
    gameover = False
    velocidade = 2
    pontuacao = 0
    
    # DEFININDO CARRO DO JOGO 

    class Veiculos(pygame.sprite.Sprite):
        
        def __init__(self, image, x, y):
            pygame.sprite.Sprite.__init__(self)
            
            image_scale = 45 / image.get_rect().width
            nova_largura = image.get_rect().width * image_scale
            nova_altura = image.get_rect().height * image_scale
            self.image = pygame.transform.scale(image, (nova_largura, nova_altura))
            
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            
    class CarroJogador(Veiculos):
        
        def __init__(self, x, y):
            image = carrousuario
            super().__init__(image, x, y)
        def update(self,image):
            self.image = pygame.image.load(image)
            
    # Grupo de Carros
    jogador_group = pygame.sprite.Group()
    veiculo_group = pygame.sprite.Group()

    # criar carro do jogador
    jogador = CarroJogador(jogador_x, jogador_y)
    jogador_group.add(jogador)

    # carregar imagens de veiculos
    image_filenames = ['imagens.jogo/pickup_truck.png', 'imagens.jogo/semi_trailer.png', 'imagens.jogo/taxi.png', 'imagens.jogo/van.png']
    veiculos_imagens = []
    for image_filename in image_filenames:
        image = pygame.image.load(image_filename)
        veiculos_imagens.append(image)
        
    # carregar a imagem de explosão
    explosao = pygame.image.load('imagens.jogo/explosao..png')
    explosao_rect = explosao.get_rect()

        
    while running:
        
        musica_menu.stop()
        musica_jogo.play(loops=20000)

        clock.tick(fps)

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        janela.fill("black")

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
            
                if event.key == K_LEFT and jogador.rect.center[0] > pista_esquerda or event.key == K_a and jogador.rect.center[0] > pista_esquerda:
                    jogador.rect.x -= 100
                elif event.key == K_RIGHT and jogador.rect.center[0] < pista_direita or event.key == K_d and jogador.rect.center[0] < pista_direita:
                    jogador.rect.x += 100
                    
                # vendo se tem colisões/explosão
                for veiculo in veiculo_group:
                    if pygame.sprite.collide_rect(jogador, veiculo):
                        
                        gameover = True
                        
                        # localização do carro do jogador
                        # para determinar o lugar que vai aparecer a explosão
                        if event.key == K_LEFT or event.key == K_a:
                            jogador.rect.left = veiculo.rect.right
                            explosao_rect.center = [jogador.rect.left, (jogador.rect.center[1] + veiculo.rect.center[1]) / 2]
                        elif event.key == K_RIGHT or event.key == K_d:
                            jogador.rect.right = veiculo.rect.left
                            explosao_rect.center = [jogador.rect.right, (jogador.rect.center[1] + veiculo.rect.center[1]) / 2]

            # desenhando grama
        janela.fill(verde)
        
        # desenhando estrada
        pygame.draw.rect(janela, cinza, estrada)
        
        # desenhando bordas
        pygame.draw.rect(janela, amarelo, marcador_borda_esquerda)
        pygame.draw.rect(janela, amarelo, marcador_borda_direita)
        
        # desenhando linhas das pistas
        movimento_pista_y += velocidade * 2
        if movimento_pista_y >= altura_marcador * 2:
            movimento_pista_y = 0
        for y in range(altura_marcador * -2, altura, altura_marcador * 2):
            pygame.draw.rect(janela, branco, (pista_esquerda + 45, y + movimento_pista_y, largura_marcador, altura_marcador))
            pygame.draw.rect(janela, branco, (pista_centro + 45, y + movimento_pista_y, largura_marcador, altura_marcador))
            
        # desenhando carro do jogador
        jogador_group.draw(janela)
        
        # adicionando veiculo
        if len(veiculo_group) < 2:
            
            # vendo se tem espaço entre os veiculos
            add_veiculo = True
            for veiculo in veiculo_group:
                if veiculo.rect.top < veiculo.rect.height * 1.5:
                    add_veiculo = False
                    
            if add_veiculo:
                
                # selecionando pista aleatória
                pista = random.choice(pistas)
                
                # selecionando imagem de carro aleatorio
                image = random.choice(veiculos_imagens)
                veiculo = Veiculos(image, pista, altura / -2)
                veiculo_group.add(veiculo)
        
        # movimento dos veiculos
        for veiculo in veiculo_group:
            veiculo.rect.y += velocidade
            
            # remover veiculo quando sair da tela
            if veiculo.rect.top >= altura:
                veiculo.kill()
                
                # adicionar pontuacao
                pontuacao += 1
                
                # almentar velocidade se passar 5 veiculos
                if pontuacao > 0 and pontuacao % 5 == 0:
                    velocidade += 1
        
        # desenhando veiculos
        veiculo_group.draw(janela)
        
        # mostrando pontuação
        texto = get_font(17).render("Pontuação:" + ' ' + str(pontuacao), True, "orange")
        texto_rect = texto.get_rect()
        texto_rect.center = (110, 40)
        janela.blit(texto, texto_rect)
        
        # verificando se a colisões de frente
        if pygame.sprite.spritecollide(jogador, veiculo_group, True):
            gameover = True
            explosao_rect.center = [jogador.rect.center[0], jogador.rect.top]
                
        # Mostrando gameOver
        if gameover:
            janela.blit(explosao, explosao_rect)
            musica_jogo.stop()
            batida.play()
           
        pygame.display.update()
        if gameover:
             time.sleep(0.7)
        while gameover:
            musica_jogo.stop()
            musica_gameover.play(loops=20000)
            janela.blit(GM, (0, 0))

            texto = get_font(40).render('VOCÊ PERDEU!', True, branco)
            texto_rect = texto.get_rect()
            texto_rect.center = (largura / 2, 100)

            texto_pontuacao = get_font(20).render(f'Pontuação: {str(pontuacao)}', True, branco)
            texto_pontuacao_rect = texto_pontuacao.get_rect()
            texto_pontuacao_rect.center = (largura / 2, 150)
            
            
            janela.blit(texto, texto_rect)
            janela.blit(texto_pontuacao, texto_pontuacao_rect)
            
            GV_MOUSE_POS = pygame.mouse.get_pos()
            clock.tick(fps)
            
            MENU_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(250, 350), 
                        text_input="VOLTAR PARA MENU", font=get_font(20), base_color="orange", hovering_color="red")
            
            JOGARNOVAMENTE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(250, 500), 
                            text_input="JOGAR NOVAMENTE", font=get_font(20), base_color="orange", hovering_color="red")
            
            for button in [MENU_BUTTON, JOGARNOVAMENTE_BUTTON]:
                button.changeColor(GV_MOUSE_POS)
                button.update(janela)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if JOGARNOVAMENTE_BUTTON.checkForInput(GV_MOUSE_POS):
                        musica_gameover.stop()
                        som_botao.play()
                        gameover = False
                        velocidade = 2
                        pontuacao = 0
                        veiculo_group.empty()
                        jogador.rect.center = [jogador_x, jogador_y]
                    if MENU_BUTTON.checkForInput(GV_MOUSE_POS):
                        musica_gameover.stop()
                        som_botao.play()
                        time.sleep(0.3)
                        menu()
            
            pygame.display.update()

# MENU
def menu():
    menu = True
    while menu:
        musica_gameover.stop()
        musica_jogo.stop()
        musica_menu.play(loops=20000)
        
        janela.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("RUN-CAR", True, "orange1")
        MENU_RECT = MENU_TEXT.get_rect(center=(250, 160))

        
            

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(250, 450), 
                            text_input="JOGAR", font=get_font(30), base_color="orange", hovering_color="red")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(250, 650), 
                            text_input="QUIT", font=get_font(30), base_color="orange", hovering_color="red")

        GARAGEM_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(250, 550), 
                            text_input="GARAGEM", font=get_font(30), base_color="orange", hovering_color="red")
        recorde.sort()
        if pontuacao > recorde[-1]:
            recorde.append(pontuacao)
            MENU_TEXT_HIGHSCORE = get_font(20).render(f"RECORDE: {recorde[-1]} ", True, "orange1")
            MENU_RECT_HIGHSCORE = MENU_TEXT.get_rect(center=(250, 250))
            janela.blit(MENU_TEXT, MENU_RECT)
            janela.blit(MENU_TEXT_HIGHSCORE, MENU_RECT_HIGHSCORE)
        
        else:
            MENU_TEXT_HIGHSCORE = get_font(20).render(f"RECORDE: {recorde[-1]} ", True, "orange1")
            MENU_RECT_HIGHSCORE = MENU_TEXT.get_rect(center=(250, 250))
            janela.blit(MENU_TEXT, MENU_RECT)
            janela.blit(MENU_TEXT_HIGHSCORE, MENU_RECT_HIGHSCORE)

        for button in [PLAY_BUTTON, QUIT_BUTTON, GARAGEM_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(janela)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    time.sleep(0.3)
                    play()
                
                if GARAGEM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    time.sleep(0.3)
                    garagem()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    time.sleep(0.3)
                    pygame.quit()
                    sys.exit()
            

        pygame.display.update()

# GARAGEM
def garagem():
    global carrousuario
    garagem = True
    
    while garagem:
        
        musica_menu.play()
        
        pygame.display.update()
        
        janela.fill('black')

        janela.blit(garagem_fundo, (0, 0))

        GARAGEM_MOUSE_POS = pygame.mouse.get_pos()

        GARAGEM_TEXT = get_font(50).render("GARAGEM", True, "white")
        GARAGEM_RECT = GARAGEM_TEXT.get_rect(center=(250, 150))

        CARRO1_BUTTON = Button(image=pygame.image.load("assets/carrousuario.png"), pos=(100, 300), 
                            text_input="1", font=get_font(10), base_color="orange", hovering_color="red")
        
        CARRO2_BUTTON = Button(image=pygame.image.load("assets/carro.1.png"), pos=(400, 300), 
                            text_input="2", font=get_font(10), base_color="orange", hovering_color="red")

        CARRO3_BUTTON = Button(image=pygame.image.load("assets/carro.2.png"), pos=(100, 550), 
                            text_input="3", font=get_font(10), base_color="orange", hovering_color="red")
        
        CARRO4_BUTTON = Button(image=pygame.image.load("assets/carro.3.png"), pos=(400, 550), 
                            text_input="4", font=get_font(10), base_color="orange", hovering_color="red")

        MENU_BUTTON = Button(image=pygame.image.load("assets/Menu.png"), pos=(50, 50), 
                            text_input="MENU", font=get_font(10), base_color="orange", hovering_color="red")


        janela.blit(GARAGEM_TEXT, GARAGEM_RECT)

        for button in [CARRO1_BUTTON, CARRO2_BUTTON, CARRO3_BUTTON, CARRO4_BUTTON, MENU_BUTTON]:
            button.changeColor(GARAGEM_MOUSE_POS)
            button.update(janela)
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if CARRO1_BUTTON.checkForInput(GARAGEM_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    time.sleep(0.3)
                    carrousuario = pygame.image.load("assets/carrousuario.png")
                    play()
                    
                if CARRO2_BUTTON.checkForInput(GARAGEM_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    time.sleep(0.3)
                    carrousuario = pygame.image.load("assets/carro.1.png")
                    play()

                if CARRO3_BUTTON.checkForInput(GARAGEM_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    musica_menu.play()
                    carrousuario = pygame.image.load("assets/carro.2.png")
                    play()

                if CARRO4_BUTTON.checkForInput(GARAGEM_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    musica_menu.play()
                    carrousuario = pygame.image.load("assets/carro.3.png")
                    play()

                if MENU_BUTTON.checkForInput(GARAGEM_MOUSE_POS):
                    musica_menu.stop()
                    som_botao.play()
                    time.sleep(0.3)
                    menu()

menu()