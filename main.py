import explorer
import time
import pandas

# ideias
# -s (separador)
# julge 

operadores = ['folder', 'judge', 'test', 'add', 'del', 'quit', 'q', '-s', '-l', '-o']
juizo = explorer.Explorer()
lista = []    


def imprime_menu():
    print()
    print("############ INFORME UM COMANDO ############")
    print("folder: cria a pasta do aluno com seu codigo")
    print("judge: compara as saidas do cod_student com o Output")
    print("test: gera testes a partir de arquivo txt (ex.:Input.txt)")
    print("del [...]: Apaga casos de testes indesejados. Aceita varios argumentos.")
    print("add [...]: Adiciona casos de testes desejados. Digite add . para adicionar todos.")
    print("quit(q): Fecha programa")
    print()

def valida_operador_str(flag : str) -> str | None:
    idx = lista.index(flag) + 1

    try:
        argumento = lista[idx]

        if (argumento in operadores):
            print("Uso de flag invalida")
            return None

        return argumento

    except IndexError:
        print("Falta argumentos para a flag")

    return None

def valida_operador_int(flag : str) -> int | None:
    idx = lista.index(flag) + 1

    try:
        valor = int(lista[idx])

        if (valor in operadores):
            print("Uso de flag invalida")
            return None

        return valor

    except ValueError:
        print(f"Para a flag {flag}, é nessário fornecer um número")
    except IndexError:
        print("Falta argumentos para a flag")

    return None

def valida_oculto(oculto : str | None) -> tuple[int, int]:
    if (oculto is not None):
        if '-' in oculto:
            limites = oculto.split('-')
            start, end = limites
            
            try:
                start = int(start)
                end = int(end)

                st = min(start, end)
                ed = max(start, end)

                return (st, ed)

            except ValueError:
                print('Intervalos definidos não são strings')
                return (0, 0)

        print('Intervalo não definido corretamente')
        return (0, 0)
    return (0,0)

def analisa_operacao() -> tuple[str, int]: 
    """
    Returns:
        tuple[str, int]: retornado
            - (str) : Separador.
            - (int) : lucky.
    """

    global lista

    separador = "NULL"
    lucky = 1
    oculto = (0, 0)

    if ('-s' in lista): #separador
        val = valida_operador_str('-s')
        separador = val if val is not None else separador

    if ('-l' in lista): #lucky
        val = valida_operador_int('-l') 
        lucky = val if val is not None else lucky

    elif ('-o' in lista): #oculto
        val = valida_operador_str('-o') 
        oculto = valida_oculto(val)

    juizo.set_lucky(lucky)
    juizo.set_separador(separador)
    juizo.set_oculto(oculto)

def get_operator() -> bool:
    global lista
    lista = input()
    lista = lista.split()

    if (len(lista) > 0):
        if (not lista[0].lower() in operadores):
            print("Operador Invalido!")
            return False    
        
        return True

    else:
        print("Falta operador!")
        return False


def get_add():
    global lista

    try: 
        pasta_desejada = lista[1]

        if (len(lista) >= 3):
            if (lista[2] == '.'):
                print('kdk')
                juizo.adiciona_teste(pasta_desejada)

            else:
                juizo.adiciona_teste(pasta_desejada, lista[2:])
        else:
            print("Falta argumetos para a operacao")
        
    except IndexError:
        print("Provável que falta indicar o diretorio para a que o teste seja adicionado")


if __name__ == "__main__":

    while True:
        imprime_menu()

        if (not get_operator()): #verifica se o primeiro operador é valido
            continue
        

        operador = lista[0] #get first element (operador)
        juizo.update_childrens()

        if operador == 'folder': #organiza tudo, se tiver Input ele gera testes, e se tiver .c ele organiza os codigos
            analisa_operacao()
            juizo.pastifica()

        elif operador == 'judge': #julga os alunos
            juizo.julga()

        elif operador == 'test': #cria uma in/out informando o .txt
            try:
                arquivo = lista[1]

                if (not arquivo.endswith('.txt')):
                    print("Argumento inválido, forneça um arquivo .txt")

                else:
                    analisa_operacao()
                    juizo.gera_testes(arquivo)

            except IndexError:
                print("Falta argumentos para a flag")

        elif operador == 'del': #apaga uma sequencia de testes
            if (len(lista) >= 2):
                if (all(arquivo.endswith('.txt') for arquivo in lista[1:])):
                    juizo.apaga(lista[1:])
                else:
                    print('Algum dos arquivos não termina em txt')
            else:
                print("Falta argumentos para a flag")

        elif operador == 'add': #adiciona um unico teste
            analisa_operacao()
            get_add()

        elif operador == 'quit' or operador.lower() == 'q':
            break

        time.sleep(1)

    print("2026 Bernardo - git hub : BartSOS")

# trazer sugestão de data para os eventos do dia pet para the next reuniao (POR MIM QUALQUER UM)