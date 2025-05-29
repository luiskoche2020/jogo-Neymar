import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from comandos.funcoes import inicializarBancoDeDados
from comandos.funcoes import escreverDados
from comandos.util import formatarPontuacao
import json

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Iron Man do Marcão")
icone  = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )

imagemPause = pygame.image.load("recursos/pause.png") 

decoracao = pygame.image.load("recursos/decoracao.png")
neymar = pygame.image.load("recursos/neymar.png")
fundoStart = pygame.image.load("recursos/fundoStart.jpg")
fundoJogo = pygame.image.load("recursos/fundoJogo.png")
fundoDead = pygame.image.load("recursos/fundoDead.png")
clt = pygame.image.load("recursos/clt.png")
missileSound = pygame.mixer.Sound("recursos/missile.wav")
explosaoSound = pygame.mixer.Sound("recursos/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/ironsound.mp3")

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
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    pausado = False

    larguraPersona = 160
    alturaPersona = 120
    margemInferior = 40
    posicaoYPersona = tamanho[1] - alturaPersona - margemInferior
    larguaMissel = 190
    alturaMissel = 150
    dificuldade = 30

    # Objeto decorativo
    larguraDecoracao = 120
    alturaDecoracao = 120
    xDecoracao = random.randint(0, tamanho[0] - larguraDecoracao)
    yDecoracao = random.randint(0, tamanho[1] - alturaDecoracao)
    velocidadeDecoracao = [random.choice([-2, 2]), random.choice([-2, 2])]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado  # alterna pause

            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0

        # EXIBIR PAUSA
        if pausado:
            tela.blit(fundoJogo, (0, 0))
            tela.blit(imagemPause, (tamanho[0]//2 - imagemPause.get_width()//2,
                                    tamanho[1]//2 - imagemPause.get_height()//2))
            pygame.display.update()
            relogio.tick(5)
            continue

        posicaoXPersona += movimentoXPersona
        
        # Movimento aleatório da decoração

        xDecoracao += velocidadeDecoracao[0]
        yDecoracao += velocidadeDecoracao[1]

        # Rebater nas bordas da tela

        if xDecoracao <= 0 or xDecoracao >= tamanho[0] - larguraDecoracao:
            velocidadeDecoracao[0] *= -1
        if yDecoracao <= 0 or yDecoracao >= tamanho[1] - alturaDecoracao:
            velocidadeDecoracao[1] *= -1

        # Limites da tela
        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > (1000 - larguraPersona):
            posicaoXPersona = 1000 - larguraPersona

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

        # Exibe pontos
        texto_pontos = fonteMenu.render("Pontos: " + formatarPontuacao(pontos), True, branco)
        tela.blit(texto_pontos, (15, 15))

        # Exibe instrução de pausa
        mensagem_pausa = fonteMenu.render("Pressione ESPAÇO para pausar o game", True, branco)
        tela.blit(mensagem_pausa, (1000 - mensagem_pausa.get_width() - 15, 15))

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
        
        tela.blit(decoracao, (xDecoracao, yDecoracao))
        pygame.display.update()
        relogio.tick(60)

def telaBoasVindas(nome):
    botao_largura = 200
    botao_altura = 50
    cinza_claro = (230, 230, 230)
    verde = (0, 150, 0)
    vermelho = (200, 0, 0)

    fonteTitulo = pygame.font.SysFont("arial", 32, bold=True)
    fonteTexto = pygame.font.SysFont("arial", 22)
    fonteBotao = pygame.font.SysFont("arial", 20, bold=True)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair.collidepoint(evento.pos):
                    quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return  # ENTER inicia o jogo

        tela.fill(cinza_claro)

        # Título centralizado
        titulo = fonteTitulo.render(f"Bem-vindo, {nome}!", True, preto)
        tela.blit(titulo, (tamanho[0]//2 - titulo.get_width()//2, 80))

        # Instruções do jogo
        instrucoes = [
            "Use as setas ( <- e -> ) do teclado para mover o Neymar.",
            "Desvie das CLTs para que o Neymar não comece a trabalhar.",
            "Para cada CLT desviada você ganha pontos.",
            "Você pode PAUSAR o jogo a qualquer momento com ESPAÇO (SPACE).",
            "Pressione ENTER para iniciar a partida!"
        ]

        for i, linha in enumerate(instrucoes):
            texto = fonteTexto.render(linha, True, preto)
            tela.blit(texto, (tamanho[0]//2 - texto.get_width()//2, 140 + i*30))

        # Botão visual de sair
        botao_sair = pygame.draw.rect(
        tela, vermelho,
        (tamanho[0] - botao_largura - 20, tamanho[1] - botao_altura - 20, botao_largura, botao_altura),
        border_radius=10
        )
        texto_sair = fonteBotao.render("Sair", True, branco)
        tela.blit(texto_sair, (tamanho[0] - 120 + 25, tamanho[1] - 60 + 10))

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

