import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos2.funcoes import inicializarBancoDeDados
from recursos2.funcoes import escreverDados
from recursos2.util import formatarPontuacao
import json
import speech_recognition as sr
import pyttsx3

def falar(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Velocidade da fala
    engine.setProperty('volume', 1.0)  # Volume máximo
    engine.say(texto)
    engine.runAndWait()

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
raio_lua = 25
direcao_lua = 1  # 1 para crescer, -1 para diminuir
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Neymar Game 2.0")
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
alarmSound = pygame.mixer.Sound("recursos/alarm.mpeg")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/champions.mpeg")

def reconhecer_fala():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale seu nome...")
        audio = r.listen(source)

    try:
        texto = r.recognize_google(audio, language="pt-BR")
        print("Você disse:", texto)
        return texto
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return ""
    except sr.RequestError as e:
        print("Erro ao conectar:", e)
        return ""
    
def jogar():
    largura_janela = 300
    altura_janela = 120

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

    # Botão para digitar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    # Botão para falar o nome
    def falar_nome():
        nome_falado = reconhecer_fala()
        if nome_falado:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, nome_falado)

    botao_falar = tk.Button(root, text="Falar nome", command=falar_nome)
    botao_falar.pack()
    root.mainloop()

    telaBoasVindas(nome)

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    posicaoXClt = 400
    posicaoYClt = -240
    velocidadeClt = 1
    pygame.mixer.Sound.play(alarmSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    pausado = False

    larguraPersona = 160
    alturaPersona = 120
    margemInferior = 40
    posicaoYPersona = tamanho[1] - alturaPersona - margemInferior
    larguaClt = 190
    alturaClt = 150
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

        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > (1000 - larguraPersona):
            posicaoXPersona = 1000 - larguraPersona

        # Animação de pulso da lua
        global raio_lua, direcao_lua
        raio_lua += direcao_lua * 0.2
        if raio_lua >= 35:
            direcao_lua = -1
        elif raio_lua <= 25:
            direcao_lua = 1

        tela.fill(branco)
        tela.blit(fundoJogo, (0, 0))
        tela.blit(neymar, (posicaoXPersona, posicaoYPersona))

        posicaoYClt += velocidadeClt
        if posicaoYClt > 600:
            posicaoYClt = -240
            pontos += 1
            velocidadeClt += 1
            posicaoXClt = random.randint(0, 800)
            pygame.mixer.Sound.play(alarmSound)

        # Desenhar lua com contorno e detalhes no canto superior direito
        centro_lua = (tamanho[0] - 100, 90)  # canto superior direito, abaixo da mensagem de pausa

        # Cores
        cor_lua = (240, 240, 255)
        cor_contorno = (200, 200, 235)
        cor_sombra = (200, 200, 230)
        cor_cratera = (180, 180, 210)

        raio_int = int(raio_lua)

        # Contorno externo (leve brilho ao redor)
        pygame.draw.circle(tela, cor_contorno, centro_lua, raio_int + 3)

        # Lua principal
        pygame.draw.circle(tela, cor_lua, centro_lua, raio_int)

        # Sombra suave sobreposta para dar volume
        pygame.draw.circle(tela, cor_sombra, (centro_lua[0] - 6, centro_lua[1] - 4), int(raio_lua * 0.8))

        # Crateras decorativas
        pygame.draw.circle(tela, cor_cratera, (centro_lua[0] + 5, centro_lua[1] - 3), 4)
        pygame.draw.circle(tela, cor_cratera, (centro_lua[0] - 5, centro_lua[1] + 4), 3)
        pygame.draw.circle(tela, cor_cratera, (centro_lua[0] + 2, centro_lua[1] + 6), 2)

        tela.blit(clt, (posicaoXClt, posicaoYClt))

        # Exibe pontos
        texto_pontos = fonteMenu.render("Pontos: " + formatarPontuacao(pontos), True, branco)
        tela.blit(texto_pontos, (15, 15))

        # Exibe instrução de pausa
        mensagem_pausa = fonteMenu.render("Pressione ESPAÇO para pausar o game", True, branco)
        tela.blit(mensagem_pausa, (1000 - mensagem_pausa.get_width() - 15, 15))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + alturaPersona))
        pixelsCltX = list(range(posicaoXClt, posicaoXClt + larguaClt))
        pixelsCltY = list(range(posicaoYClt, posicaoYClt + alturaClt))

        os.system("cls")
        if len(set(pixelsCltY).intersection(pixelsPersonaY)) > dificuldade:
            if len(set(pixelsCltX).intersection(pixelsPersonaX)) > dificuldade:
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
    cinza_escuro = (50, 50, 50)
    branco_suave = (240, 240, 240)
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

        tela.fill(cinza_escuro)

        # Título centralizado
        titulo = fonteTitulo.render(f"Bem-vindo, {nome}!", True, branco_suave)
        tela.blit(titulo, (tamanho[0]//2 - titulo.get_width()//2, 80))

        # Instruções do jogo
        instrucoes = [
            "Use as setas ( ← e → ) do teclado para mover o Neymar.",
            "Desvie das CLTs para que o Neymar não comece a trabalhar.",
            "Para cada CLT desviada você ganha pontos.",
            "Você pode PAUSAR o jogo a qualquer momento com ESPAÇO (SPACE).",
            "Pressione ENTER para iniciar a partida!"
        ]

        for i, linha in enumerate(instrucoes):
            texto = fonteTexto.render(linha, True, branco_suave)
            tela.blit(texto, (tamanho[0]//2 - texto.get_width()//2, 140 + i*35))

        # Botão visual de sair
        texto_sair = fonteBotao.render("Sair", True, branco_suave)
        padding_x, padding_y = 20, 10
        botao_largura = texto_sair.get_width() + padding_x * 2
        botao_altura = texto_sair.get_height() + padding_y * 2
        x_botao = tamanho[0] - botao_largura - 20
        y_botao = tamanho[1] - botao_altura - 20

        botao_sair = pygame.draw.rect(
            tela, vermelho,
            (x_botao, y_botao, botao_largura, botao_altura),
            border_radius=10
        )
        tela.blit(texto_sair, (x_botao + padding_x, y_botao + padding_y))

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
    falar("Game Over")

    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40

    # Carregar os últimos 5 registros do log
    try:
        with open("log.dat.", "r") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}

    ultimos_registros = sorted(
        dados.items(),
        key=lambda item: item[1][1],
        reverse=True
    )[:5]

    texto_logs = []
    for nick, (pontos, data_hora) in ultimos_registros:
        texto_logs.append(f"Pontos: {pontos} - Data: {data_hora} - Nick: {nick}")

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
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()

        tela.fill(branco)
        tela.blit(fundoDead, (0,0))

        # Exibe título
        vermelho = (255, 0, 0)
        titulo_logs = fonteMenu.render("Últimos 5 Registros:", True, vermelho)
        tela.blit(titulo_logs, (350, 200))

        vermelho = (255, 0, 0)  # vermelho forte
        for i, texto in enumerate(texto_logs):
                log_texto = fonteMenu.render(texto, True, vermelho)
                tela.blit(log_texto, (150, 250 + i*30))

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))

        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))

        pygame.display.update()
        relogio.tick(60)
start()

