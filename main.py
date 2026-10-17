import explorer
import time
from utils import *

operadores = ['folder', 'judge', 'test', 'add', 'del', 'quit', 'q']
flags = ['-s', '-l', '-o']
explore = explorer.Explorer()
lista = []    


def imprime_menu():
    print()
    print("=" * 72)
    print("                         MENU DE OPÇÕES - JUIZ C                        ")
    print("=" * 72)
    print("  COMANDOS:")
    print("    folder [flags]                Organiza códigos (.c) em Alunos/ e")
    print("                                  gera testes de arquivos (.txt) na raiz")
    print("    test <arquivo.txt> [flags]    Gera casos de teste em Gabaritos/ a")
    print("                                  partir de um arquivo .txt (ex: Input.txt)")
    print("    add <pasta> <arq.txt... | .>  Adiciona novos arquivos .txt à pasta de")
    print("                                  gabarito (use '.' para adicionar todos)")
    print("    del <test_1.txt ...>          Remove os casos de teste informados de")
    print("                                  Input/Output e reordena os restantes")
    print("    judge                         Compila e executa os códigos dos alunos")
    print("                                  comparando com os gabaritos")
    print("    quit (ou q)                   Encerra o programa")
    print("-" * 72)
    print("  FLAGS OPCIONAIS (para 'folder' e 'test'):")
    print("    -s <sep>         Define o separador entre casos de teste (ex: -s \\n)")
    print("    -o <ini>-<fim>   Define o intervalo de casos ocultos (ex: -o 1-3)")
    print("    -l <min>-<max>   Agrupa subcasos aleatoriamente por teste (ex: -l 1-5)")
    print("=" * 72)
    print()

def valida_operador_str(flag : str) -> str | None:
    idx = lista.index(flag) + 1

    try:
        return lista[idx]

    except IndexError:
        raise ArgumentFlagError(flag = flag)

def valida_operador_int(flag : str) -> int | None:
    try:
        operador_str = valida_operador_str()
        operador_int = int(operador_str)
        return operador_int
        
    except ValueError as e:
        raise ArgumentFlagError(f"O argumento da flag {flag} não é um int")
    
def valida_intervalo(flag : str) -> tuple[int, int] | None:
    try:
        oculto = valida_operador_str(flag)

        if not '-' in oculto:
            raise IntervalIndefinedError(f'Para definir um intervalo é preciso seperá-lo com um traço -.', tupla_interval=oculto, flag=flag)

        limites = oculto.split('-')
        limites = [item for item in limites if item != '']

        if len(limites) < 2:
            raise IntervalIndefinedError('O intervalo deve ter um valor inicial e final', tupla_interval=oculto, flag=flag)

        start, end = limites
        
        start = int(start)
        end = int(end)

        st = min(start, end)
        ed = max(start, end)

        if (st < 0 or ed < 0):
            raise IntervalIndefinedError('Os valores do intervalo devem ser positivos', tupla_interval=oculto, flag=flag)

        return (st, ed)

    except ValueError:
        raise IntervalIndefinedError(f'Intervalos definidos não são inteiros.', tupla_interval=oculto, flag=flag)

def analisa_operacao() -> tuple[str, int]: 
    global lista

    if ('-s' in lista): #separador
        separador = valida_operador_str('-s')
        explore.set_separador(separador)

    if ('-l' in lista): #lucky
        lucky = valida_intervalo('-l')
        explore.set_lucky(lucky)

    if ('-o' in lista): #oculto
        oculto = valida_intervalo('-o')
        explore.set_oculto(oculto)


def get_operator() -> bool:
    global lista
    lista = input()
    lista = lista.split()

    if (len(lista) > 0):
        lista[0] = lista[0].lower()

        if (not lista[0] in operadores):
            print("Comando Invalido!")
            return False    
        
        return True

    else:
        print("É necessário fornecer um comando")
        return False


def get_add():
    global lista

    try: 
        pasta_desejada = lista[1]

        if (len(lista) >= 3):
            if (lista[2] == '.'):
                print('kdk')
                explore.adiciona_teste(pasta_desejada)

            else:
                explore.adiciona_teste(pasta_desejada, lista[2:])
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
        explore.update_childrens()

        try:
            if operador == 'folder': #organiza tudo, se tiver Input ele gera testes, e se tiver .c ele organiza os codigos
                analisa_operacao()
                explore.pastifica()

            elif operador == 'judge': #julga os alunos
                explore.julga()

            elif operador == 'test': #cria uma in/out informando o .txt
                try:
                    arquivo = lista[1]

                    if (not arquivo.endswith('.txt')):
                        print("Argumento inválido, forneça um arquivo .txt")

                    else:
                        analisa_operacao()
                        explore.gera_testes(arquivo)

                except IndexError:
                    print("Falta argumentos para a flag")

            elif operador == 'del': #apaga uma sequencia de testes
                if (len(lista) >= 2):
                    if (all(arquivo.endswith('.txt') for arquivo in lista[1:])):
                        explore.apaga(lista[1:])
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

        except IntervalIndefinedError as e:
            print(f"Erro: {e}")

        except ArgumentFlagError as e:
            print(f"Erro: {e}")


    print("2026 Bernardo - git hub : BartSOS")

# trazer sugestão de data para os eventos do dia pet para the next reuniao (POR MIM QUALQUER UM)