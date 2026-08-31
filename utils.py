import os
import shutil

def create_if_not_exist(caminho : str):
    if not os.path.exists(caminho):
        os.mkdir(caminho)

    else:
        shutil.rmtree(caminho)
        os.mkdir(caminho)

def create(caminho : str):
    if not os.path.exists(caminho):
        os.mkdir(caminho)

def cifra_codigo(mensagem : str, chave : int):
    result = ""
    for letra in mensagem:
        result += chr(ord(letra) ^ chave)
    
    return result

def escreve_binario(file_name : str, mensagem : str):
    with open(file_name, "w", encoding='utf-8') as w:
        msg = "".join(chr(ord(letra) + 1425) for letra in mensagem) #joga o valor ord para proximo da faixa de char hebraicos no utf-8
        w.write(msg)

def le_binario(file_name : str) -> str:
    with open(file_name, "r", encoding='utf-8') as r:
        leitura = r.read()
        msg = "".join(chr(ord(letra) - 1425) for letra in leitura)
        return msg

def gera_caminho(diretorio : str) -> list:  #retorna todos os arquivos dentro de uma certa pasta
    try:
        lista = os.listdir(diretorio)
    except FileNotFoundError:
        print(f'DEU MERDA, ARQUIVO {diretorio} NAO ENCONTRADO')
        exit()   

    array = []
    for arquivos in lista:
        array.append(f'{diretorio}/{arquivos}') #junta os caminhos

    return sorted(array, key=lambda palavra: (len(palavra), palavra)) #organiza de acordo com ordem alfabetica
   
