import pygame
import sys
from time import sleep
from random import sample
from questions import questoes, listaPremio
from ui import Button

# Inicialização do Pygame
pygame.init()

# Configurações da tela
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Show do Pythão")

# Variáveis globais
contador = 0
contadorpulos = 0
contador_delecoes = 0  # Contador de deleções
errou = False
pontuacao = 0
tempo_restante = 15  # Tempo em segundos para cada pergunta

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Imagem de fundo
BG = pygame.image.load("assets/imagens/Background.jpg")

# Imagens
BUTTON_IMAGE = pygame.image.load("assets/imagens/button.png")  
LOGO = pygame.image.load("assets/imagens/logo.png")
derrota = pygame.image.load("assets/imagens/derrota.png")
vitoria = pygame.image.load("assets/imagens/vitoria.png")

#Efeitos sonoros

pygame.mixer.init()

som_acerto = pygame.mixer.Sound("assets/musicas/silvio-santos-certa-resposta_1.wav")
som_erro = pygame.mixer.Sound("assets/musicas/errou-show-do-milhao.wav")
som_tempo = pygame.mixer.Sound("assets/musicas/suspense-show-do-milhao.wav")
som_tempo_fim = pygame.mixer.Sound("assets/musicas/tempo-acabou-show-do-milhao-_1_.wav")
som_vitoria = pygame.mixer.Sound("assets/musicas/parabens-voce-acaba-de-ganhar-um-milhao-de-reais_1.wav")
som_inicio = pygame.mixer.Sound("assets/musicas/silvio-santos-abertura-show-do-milhao.wav")

#Ajuste de volume dos sons

som_inicio.set_volume(0.5)
som_acerto.set_volume(1)

# Fontes
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Função para exibir texto na tela
def mostrar_texto(texto, x, y, cor=white):
    texto_surface = get_font(26).render(texto, True, cor)
    screen.blit(texto_surface, (x, y))

# Função para exibir a mensagens do Facilitador e Pulo
def mostrar_mensagem_alternativas(mensagem):
    texto_surface = get_font(26).render(mensagem, True, red)
    largura_texto, altura_texto = texto_surface.get_size()
    x = width - largura_texto - 20  # Margem de 20 pixels da borda direita
    y = height - altura_texto - 20  # Margem de 20 pixels da borda inferior
    screen.blit(texto_surface, (x, y))

# Função para exibir o temporizador
def mostrar_temporizador():
    mostrar_texto(f"Tempo: {tempo_restante}s", 20, 20)

# Função para exibir uma pergunta
def exibir_pergunta(pergunta, alternativas):
    screen.fill(black)
    mostrar_texto(f"Pergunta {contador + 1}:", 50, 50)
    mostrar_texto(pergunta, 50, 150)
    y_offset = 100
    for alternativa in alternativas:
        mostrar_texto(alternativa.strip(), 50, y_offset)  # Ajustado para x=50 (alinhado à esquerda)
        y_offset += 40
    mostrar_temporizador()

    # Divide a pergunta em várias linhas
    linhas_pergunta = mostrar_texto(pergunta, 70)  # 80 caracteres por linha
    y_offset = 150
    for linha in linhas_pergunta:
        mostrar_texto(linha, 50, y_offset)
        y_offset += 30  # Espaçamento entre as linhas

    # Exibe as alternativas
    y_offset += 20  # Espaçamento adicional antes das alternativas
    for alternativa in alternativas:
        linhas_alternativa = mostrar_texto(alternativa.strip(), 80)  # 80 caracteres por linha
        for linha in linhas_alternativa:
            mostrar_texto(linha, 50, y_offset)
            y_offset += 30  # Espaçamento entre as linhas

    # Exibe a pontuação e o temporizador
    mostrar_temporizador()

# Função para remover duas alternativas erradas
def remover_alternativas_erradas(alternativas, resposta_correta):
    alternativas_erradas = [alt for alt in alternativas if alt != resposta_correta]
    if len(alternativas_erradas) >= 2:
        alternativas_remover = sample(alternativas_erradas, 2)
        for alt in alternativas_remover:
            alternativas.remove(alt)
    return alternativas

def reiniciar_jogo():
    global contador, contadorpulos, contador_delecoes, errou, pontuacao, tempo_restante
    contador = 0
    contadorpulos = 0
    contador_delecoes = 0  # Reinicia o contador de deleções
    errou = False
    pontuacao = 0
    tempo_restante = 15

def tela_derrota():
    som_erro.play() # Da play na musica
    som_tempo.stop() # Para o som para que  não sobressaia o outro
    reiniciar_jogo()  # Reinicia as variáveis ao voltar ao menu

    while True:
        screen.blit(BG, (0, 0))  # Desenha o fundo

        DERROTA_MOUSE_POS = pygame.mouse.get_pos()

        # Texto de derrota
        screen.blit(derrota, (130, 200))

        # Botão para voltar ao menu
        VOLTAR_BUTTON = Button(image=None, pos=(640, 460), 
                              text_input="VOLTAR AO MENU", font=get_font(50), base_color=white, hovering_color=green)
        VOLTAR_BUTTON.changeColor(DERROTA_MOUSE_POS)
        VOLTAR_BUTTON.update(screen)

        # Verifica eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLTAR_BUTTON.checkForInput(DERROTA_MOUSE_POS):
                    reiniciar_jogo()  # Reinicia o jogo antes de voltar ao menu
                    main_menu()  # Volta ao menu principal

        pygame.display.update()

def tela_vitoria():
    som_acerto.stop()
    som_vitoria.play()
    som_tempo.stop()
    while True:
        screen.blit(BG, (0, 0))  # Desenha o fundo

        VITORIA_MOUSE_POS = pygame.mouse.get_pos()

        # Texto de vitória
        screen.blit(vitoria, (130, 100))

        # Exibe a pontuação final
        PONTUACAO_TEXT = get_font(50).render(f"Parabéns você ganhou: R$1.000.000", True, white)
        PONTUACAO_RECT = PONTUACAO_TEXT.get_rect(center=(640, 360))
        screen.blit(PONTUACAO_TEXT, PONTUACAO_RECT)

        # Botão para voltar ao menu
        VOLTAR_BUTTON = Button(image=None, pos=(640, 460), 
                              text_input="VOLTAR AO MENU", font=get_font(50), base_color=white, hovering_color=green)
        VOLTAR_BUTTON.changeColor(VITORIA_MOUSE_POS)
        VOLTAR_BUTTON.update(screen)

        # Verifica eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if VOLTAR_BUTTON.checkForInput(VITORIA_MOUSE_POS):
                    main_menu()  # Volta ao menu principal

        pygame.display.update()

# Função principal do jogo
def play():
    som_tempo.play()
    som_inicio.stop()
    reiniciar_jogo()  # Reinicia as variáveis ao iniciar uma nova partida
    global contador, contadorpulos, contador_delecoes, errou, pontuacao, tempo_restante

    # Índice para percorrer a lista de perguntas em ordem
    indice_pergunta = 0

    while indice_pergunta < len(questoes):
        # Carrega a pergunta atual
        pergunta = questoes[indice_pergunta]["pergunta"]
        alternativas_originais = questoes[indice_pergunta]["opcoes"].copy()  # Cópia das alternativas originais
        alternativas = alternativas_originais.copy()  # Lista de alternativas que será modificada
        resposta_correta = questoes[indice_pergunta]["resposta"]

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()  # Reinicia o temporizador para cada pergunta

        proxima_pergunta = False  # Variável de controle para avançar para a próxima pergunta

        while not proxima_pergunta:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            # Atualiza o temporizador
            current_time = pygame.time.get_ticks()
            tempo_restante = 20 - ((current_time - start_time) // 1000)

            # Verifica se o tempo acabou
            if tempo_restante <= 0:
                som_tempo_fim.play()
                som_erro.stop()
                tela_derrota()  # Chama a tela de derrota
                return

            # Limpa a tela antes de redesenhar
            screen.fill(black)
            screen.blit(BG, (0, 0))

            # Redesenha a pergunta, pontuação e temporizador
            mostrar_texto(f"Pergunta {contador + 1}:", 50, 80)
            mostrar_texto(pergunta, 50, 150)
            mostrar_temporizador()

            # Botão de pular (com a quantidade de pulos restantes)
            PLAY_JUMP = Button(image=None, pos=(100, 680),
                               text_input=f"Pular ({3 - contadorpulos})", font=get_font(30), base_color=white, hovering_color=green)
            PLAY_JUMP.changeColor(PLAY_MOUSE_POS)
            PLAY_JUMP.update(screen)

            # Botão de deletar alternativas
            DELETE_BUTTON = Button(image=None, pos=(280, 680),
                                   text_input=f"Facilitar ({3 - contador_delecoes})", font=get_font(30), base_color=white, hovering_color=green)
            DELETE_BUTTON.changeColor(PLAY_MOUSE_POS)
            DELETE_BUTTON.update(screen)

            # Botões para as alternativas
            botoes_alternativas = []
            y_offset = 250  
            for alternativa in alternativas:
                botao = Button(image=BUTTON_IMAGE, pos=(630, y_offset + 20),  # Use a imagem do botão
                               text_input=alternativa.strip(), font=get_font(19), base_color=white, hovering_color=green)
                botoes_alternativas.append(botao)
                y_offset += 100

            for botao in botoes_alternativas:
                botao.changeColor(PLAY_MOUSE_POS)
                botao.update(screen)

            # Verifica eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_JUMP.checkForInput(PLAY_MOUSE_POS):
                        if contadorpulos < 3:
                            contadorpulos += 1
                            contador += 1
                            indice_pergunta += 1  # Avança para a próxima pergunta
                            proxima_pergunta = True  # Sai do loop interno
                            break  # Sai do loop interno para carregar a próxima pergunta
                        else:
                            mostrar_mensagem_alternativas("Você não tem mais pulos")
                            pygame.display.flip()
                            sleep(2)
                    if DELETE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                        if contador_delecoes < 3:
                            alternativas = remover_alternativas_erradas(alternativas, resposta_correta)
                            contador_delecoes += 1
                        else:
                            mostrar_mensagem_alternativas("Você não pode mais deletar alternativas")
                            pygame.display.flip()
                            sleep(2)
                    for i, botao in enumerate(botoes_alternativas):
                        if botao.checkForInput(PLAY_MOUSE_POS):
                            if alternativas[i] == resposta_correta:
                                som_acerto.play()
                                contador += 1
                                indice_pergunta += 1  # Avança para a próxima pergunta
                                if indice_pergunta >= len(questoes):  # Verifica se todas as perguntas foram respondidas
                                    tela_vitoria()  # Chama a tela de vitória com a pontuação total
                                    return  # Sai da função play
                                proxima_pergunta = True  # Sai do loop interno
                                som_tempo.stop()
                                som_tempo.play()
                                break  # Sai do loop interno para carregar a próxima pergunta
                            else:
                                errou = True
                                break

            if errou:
                tela_derrota()  # Chama a tela de derrota
                return

            pygame.display.update()
            clock.tick(20)

# Função do menu principal e inicio de jogo
def main_menu():
    som_inicio.play()
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(LOGO, (130, 40))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/imagens/Play Rect.png"), pos=(640, 350), 
                             text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/imagens/Quit Rect.png"), pos=(640, 550), 
                             text_input="QUIT", font=get_font(70), base_color="#d7fcd4", hovering_color="White")

        
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Iniciar o jogo
main_menu()