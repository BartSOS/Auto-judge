import os
import shutil
import re

FOLDER_GABARITOS = "Gabaritos"
FOLDER_ALUNOS = "Alunos"
FOLDER_CASOS_OCULTOS = "Casos Ocultos"

def create_new_path(caminho : str):
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

def remove_if_exist(caminho : str):
    if (os.path.exists(caminho)):
        shutil.rmtree(caminho)

def escreve_binario(file_name : str, mensagem : str):
    with open(file_name, "w", encoding='utf-8') as w:
        msg = "".join(chr(ord(letra) + 1425) for letra in mensagem) #joga o valor ord para proximo da faixa de char hebraicos no utf-8
        w.write(msg)

def le_binario(file_name : str) -> str:
    with open(file_name, "r", encoding='utf-8') as r:
        leitura = r.read()
        msg = "".join(chr(ord(letra) - 1425) for letra in leitura)
        return msg

def rename_and_update(old_name : str, new_name : str)-> str:
    os.rename(old_name, new_name)
    return new_name

def move_and_update(file_src : str, caminho_dest : str) -> str:
    shutil.move(file_src, caminho_dest)
    return os.path.join(caminho_dest, file_src)

def gera_caminho(diretorio : str) -> list:  #retorna todos os arquivos dentro de uma certa pasta
    try:
        lista = os.listdir(diretorio)
    except FileNotFoundError:
        print(f'DEU MERDA, ARQUIVO {diretorio} NAO ENCONTRADO')
        exit()   

    array = []
    for arquivos in lista:
        array.append(f'{diretorio}/{arquivos}') #junta os caminhos

    def chave_ordem_natural(caminho : str):
        return [int(texto) if texto.isdigit() else texto.lower() for texto in re.findall(r'\d+|\D+', caminho)]

    return sorted(array, key=chave_ordem_natural) #organiza de acordo com ordem alfabetica
   
class IntervalIndefinedError(Exception):
    """Inappropriate argument value of interval(of correct type)."""

    def __init__(self, mensagem : str = "O intervalo não foi definido corretamente. É esperado dois numeros no formato int-int.", tupla_interval : str | None = None, flag : str | None = None):
        self.mensagem = mensagem
        self.flag = flag
        self.tupla = tupla_interval
        super().__init__(self.mensagem)

    def __str__(self):
        if (self.tupla and self.flag):
            return f"{self.mensagem}\nFoi tentado inserir o seguinte intervalo {self.tupla}\nA flag utilizada: {self.flag}"

        return self.mensagem

class ArgumentFlagError(Exception):
    """Inappropriate argument flag."""

    def __init__(self, mensagem : str = "O argumento da flag não existe.", flag : str | None = None):
        self.mensagem = mensagem
        self.flag = flag
        super().__init__(self.mensagem)

    def __str__(self):
        if (self.flag):
            return f"{self.mensagem}\nFlag requerida {self.flag}"

        return self.mensagem