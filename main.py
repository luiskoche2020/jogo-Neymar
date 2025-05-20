import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.util import formatarPontuacao
import json

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Iron Man do Marcão")
icone  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )

imagemPause = pygame.image.load("assets/pause.png") 

neymar = pygame.image.load("assets/neymar.png")
fundoStart = pygame.image.load("assets/fundoStart.jpg")
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoDead = pygame.image.load("assets/fundoDead.png")
clt = pygame.image.load("assets/clt.png")
missileSound = pygame.mixer.Sound("assets/missile.wav")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("assets/ironsound.mp3")

def jogar():
    largura_janela = 300
    altura_janela = 50

    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()
    root.mainloop()

    telaBoasVindas(nome)

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    pausado = False

    larguraPersona = 160
    alturaPersona = 120
    larguaMissel = 190
    alturaMissel = 150
    dificuldade = 30

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
                elif evento.key == pygame.K_UP:
                    movimentoYPersona = -15
                elif evento.key == pygame.K_DOWN:
                    movimentoYPersona = 15
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado  # alterna pause

            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0
                if evento.key in [pygame.K_UP, pygame.K_DOWN]:
                    movimentoYPersona = 0

        # EXIBIR PAUSA
        if pausado:
            tela.blit(fundoJogo, (0, 0))
            tela.blit(imagemPause, (tamanho[0]//2 - imagemPause.get_width()//2,
                                    tamanho[1]//2 - imagemPause.get_height()//2))
            pygame.display.update()
            relogio.tick(5)
            continue

        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        # Limites da tela
        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > (1000 - larguraPersona):
            posicaoXPersona = 1000 - larguraPersona

        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > (700 - alturaPersona):
            posicaoYPersona = 700 - alturaPersona

        tela.fill(branco)
        tela.blit(fundoJogo, (0, 0))
        tela.blit(neymar, (posicaoXPersona, posicaoYPersona))

        posicaoYMissel += velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos += 1
            velocidadeMissel += 1
            posicaoXMissel = random.randint(0, 800)
            pygame.mixer.Sound.play(missileSound)

        tela.blit(clt, (posicaoXMissel, posicaoYMissel))

        texto = fonteMenu.render("Pontos: " + formatarPontuacao(pontos), True, branco)
        tela.blit(texto, (15, 15))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))

        os.system("cls")
        if len(set(pixelsMisselY).intersection(pixelsPersonaY)) > dificuldade:
            if len(set(pixelsMisselX).intersection(pixelsPersonaX)) > dificuldade:
                escreverDados(nome, pontos)
                dead()
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")

        pygame.display.update()
        relogio.tick(60)

def telaBoasVindas(nome):
    botao_largura = 200
    botao_altura = 50

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    return  # sai da tela e inicia o jogo

        tela.fill(branco)

        # Texto: Boas-vindas
        saudacao = fonteMenu.render(f"Bem-vindo, {nome}!", True, preto)
        tela.blit(saudacao, (tamanho[0]//2 - saudacao.get_width()//2, 100))

        # Instruções
        instrucoes = [
            "Use as setas ( <- e ->) do teclado para mover o Neymar.",
            "Desvie das CLTs para que o Neymar não começar a trabalhar.",
            "Para cada CLT desviada você pontua",
            "Obs: Você pode PAUSAR em qualquer momento apertando ESPAÇO (SPACE)"
        ]

        for i, linha in enumerate(instrucoes):
            texto = fonteMenu.render(linha, True, preto)
            tela.blit(texto, (tamanho[0]//2 - texto.get_width()//2, 160 + i*30))

        # Botão "Começar"
        botao_rect = pygame.draw.rect(
            tela,
            (0, 200, 0),
            (tamanho[0]//2 - botao_largura//2, 350, botao_largura, botao_altura),
            border_radius=10
        )
        texto_botao = fonteMenu.render("Começar", True, branco)
        tela.blit(texto_botao, (tamanho[0]//2 - texto_botao.get_width()//2, 360))

        pygame.display.update()
        relogio.tick(60)

def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        
            
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)


start()

