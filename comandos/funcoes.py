import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    try:
        with open("base.atitus", "r") as banco:
            dados = banco.read()
            dadosDict = json.loads(dados) if dados else {}
    except FileNotFoundError:
        dadosDict = {}

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # inclui data e hora
    dadosDict[nome] = (pontos, data_hora)

    with open("base.atitus", "w") as banco:
        banco.write(json.dumps(dadosDict, indent=4))
    
    # END - inserindo no arquivo