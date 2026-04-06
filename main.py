import juiz as j
import time

while True:
    print()
    print("############ INFORME UM COMANDO ############")
    print("Pastifica: cria a pasta do aluno com seu codigo")
    print("Julga: compara as saidas do cod_student com o Output")
    print("Testifica: gera testes a partir de arquivo txt (ex.:Input.txt)")
    print("Del [...]: Apaga casos de testes indesejados. Aceita varios argumentos.")
    print("Add [...]: Adiciona casos de testes indesejados. Aceita varios argumentos.")
    print("Sair: Fecha programa")
    print()

    lista = input().lower()
    lista = lista.split()
    operador = lista[0]

    if operador == 'pastifica':
        if (len(lista) > 1):  #verifica se existe algum argumento para o pastifica (default: seperador NULL, sorted false, max_limite 1)
            separador = "NULL"
            sorted = "sorted"

            if sorted in lista: #pastifica, tlv sorted (len ja eh maior que 1)
                indice_do_sorted = lista.index(sorted)
                
                if (len(lista) > indice_do_sorted + 1):  #pastifica, sorted, tlv max_limite   ///   #verifica se existe o max_limite do sorted
                    max_limite = lista[indice_do_sorted + 1]

                    if (len(lista) > 3): #pastifica, tvl separador, sorted, max_limite
                        separador = lista[1]

                    j.pastifica(separador, True, max_limite)  #todos os argumentos

                else:
                    if (len(lista) > 2): #pastifica, tvl separador, sorted
                        separador = lista[1]

                    j.pastifica(separador, True) #faltou o max_limite (acaba gerando apenas 1 caso por separador)
                    
            else: #pastifica, tlv separador
                separador = lista[1]
                j.pastifica(separador)  #gera casos de testes com base no separador fornecido

        else:
            j.pastifica() #Input -> test_1.txt

    elif operador == 'julga':
        j.julga()

    elif operador == 'testifica':
        if (len(lista) > 1):  #verifica se existe algum argumento para o testifica (default: seperador NULL, sorted false, max_limite 1)
            arquivo = lista[1]
            sorted = "sorted"
            separador = "NULL"

            if sorted in lista and len(lista) > 2: #testifica, arquivo, tlv sorted...  #TEM SORTED
                indice_do_sorted = lista.index(sorted)
                
                if (len(lista) > indice_do_sorted + 1): #existe valor de max_limite
                    max_limite = lista[indice_do_sorted + 1]

                    if (len(lista) > 4): #testifica, arquivo, separador, sorted, tvl max_limite...
                        separador = lista[2]

                    j.randomriza_qtd_testes(max_limite) 
                    j.gera_testes(arquivo, separador)

                else:
                    if (len(lista) > 3):  #testifica, arquivo, separador, sorted
                        separador = lista[2]

                    j.randomriza_qtd_testes()
                    j.gera_testes(arquivo, separador) #faltou o max_limite (acaba gerando apenas 1 caso por separador)
                    

            else: #NAO TEM SORTED
                if (len(lista) > 2): #testifica, arquivo, tlv separador
                    separador = lista[2]

                j.gera_testes(arquivo, separador)  #gera casos de testes com base no separador fornecido

        else:
            j.gera_testes(arquivo) #Input -> test_1.txt


    elif operador == 'del':
        j.apaga(lista)

    elif operador == 'add':
        j.adiciona_teste(lista[1], lista[2:])

    elif operador == 'sair':
        break

    time.sleep(1)

print("MUITO OBRIGADO!")


# trazer sugestão de data para os eventos do dia pet para the next reuniao (POR MIM QUALQUER UM)