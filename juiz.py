import os
import shutil
import subprocess
import random

lista_limites_max = []
gabaritos = "Gabaritos"

def gera_caminho(diretorio): #retorna todos os arquivos dentro de uma certa pasta
    try:
        lista = os.listdir(diretorio)
    except FileNotFoundError:
        print('DEU MERDA, ARQUIVO NAO ENCONTRADO')
        exit()   

    array = []
    for arquivos in lista:
        array.append(f'{diretorio}/{arquivos}')

    return sorted(array, key=lambda palavra: (len(palavra), palavra))

def adiciona_teste(pasta_desejada, arquivos_desejados):
    if os.path.exists(gabaritos):
        pasta_desejada = os.path.join(gabaritos, pasta_desejada)
        if os.path.exists(pasta_desejada):
            for arquivo_desejado in arquivos_desejados:
                testes = gera_caminho(pasta_desejada) #array com todos os testes
                indice_final = os.path.basename(testes[-1][:-4]) #pega a string do ultimo teste (test_5)
                indice_final = int(indice_final[5:]) #pega a parte inteira (5)

                if os.path.exists(arquivo_desejado):
                    novo_nome = f'test_{indice_final + 1}.txt' #adiciona ao novo teste da pasta o indice_final + 1
                    os.rename(arquivo_desejado, novo_nome) 
                    shutil.move(novo_nome, pasta_desejada) 
                    print(f"Arquivo {arquivo_desejado} sendo movido para pasta {pasta_desejada}")

                else:
                    print(f"Arquivo {arquivo_desejado} não existe")
        
        else:
            print(f"Pasta {pasta_desejada} não existe")
    
    else:
        print(f"Comando não executado! Pasta {gabaritos} não existe")


def le_testes(separar_por_linha, tem_argumento, arq):
    testes = []
    if tem_argumento:
        grupo = ""
        bloco = ""
        contador = 0
        indice_limite = 0

        while True:
            linha = arq.readline()
            bloco += linha
            
            if not separar_por_linha:
                if linha == "":
                    grupo += bloco
                    if (contador + 1)%max_limites[indice_limite] != 0:
                        testes.append(grupo)
                    break
                
                if linha[0] == '\n':
                    contador += 1
                    grupo += bloco
                    bloco = ""

                    if (contador + 1)%max_limites[indice_limite] == 0:
                        contador = 0
                        indice_limite += 1
                        testes.append(grupo[:-1])
                        grupo = ""
                
            else:
                if linha == "":
                    break
                testes.append(linha)

    else:
        testes.append("".join(arq.readlines()))

    return testes

def le_txt_e_gera_casos_de_teste(arquivo_base_txt, separador):
    testes = []
    string_base = arquivo_base_txt.read()

    if (separador != "NULL"):
        testes = string_base.split(separador)

    else:
        testes.append(string_base)

    if (len(lista_limites_max) > 0):
        lista_sorted = []
        i = 0
        j = 0
        while j < len(testes):
            lista_sorted.append(testes[j:j+lista_limites_max[i]])
            j += lista_limites_max[i]
            i += 1

        return lista_sorted

    return testes


def gera_testes(arquivos, separador = "NULL"):
    if os.path.exists(arquivos): #so eh pra gerar testes se o arquivo de testes.txt existir
        if os.path.exists(gabaritos):
            diretorio = os.path.join(gabaritos, arquivos[:-4])
            if not os.path.exists(diretorio):
                os.mkdir(diretorio)
            else:
                shutil.rmtree(diretorio)
                os.mkdir(diretorio)

            with open(arquivos, 'r') as arq:
                testes = le_txt_e_gera_casos_de_teste(arq, separador)
                
                for i, grupo in enumerate(testes):
                    caminho_arquivo = os.path.join(gabaritos, f'{arquivos[:-4]}', f'test_{i+1}.txt')
                    with open(caminho_arquivo, 'w', encoding='UTF-8', newline='\n') as test:
                        test.write(grupo)

            os.remove(arquivos)     

        else:
            os.mkdir(gabaritos)

    else:
        print(f"Arquivo {arquivos} não encontrado")

def randomriza_qtd_testes(max_limite = 1):
    for i in range(0, 20):
        limite = random.randint(1, max_limite)
        lista_limites_max.append(limite)

def pastifica(separador = "NULL", sorted = False, max_limite = 1):
    if not os.path.exists('Alunos'):
        os.mkdir('Alunos')

    if not os.path.exists(gabaritos):
        os.mkdir(gabaritos)

    caminhos = os.listdir() #diretorio atual

    for arquivos in caminhos:
        if arquivos.endswith('.txt'): #arquivos para gerar testes (ex.: Input, Output)
            if sorted:
                randomriza_qtd_testes(max_limite)

            gera_testes(arquivos, separador)

        elif arquivos.endswith('.c'): #codigos dos alunos
            caminho_do_c = os.path.join('Alunos', f'{arquivos[:-2]}')
            if not os.path.exists(caminho_do_c):
                os.mkdir(caminho_do_c)
                shutil.move(arquivos, caminho_do_c)  

def organiza_testes(arquivos): #organiza os testes em ordem, caso estejam não tenha um deles (test_1, test_2, test_4) -> (test_1, test_2, test_3)
    casos = gera_caminho(arquivos)
    for i, testes in enumerate(casos):
        indice_do_teste = (len(os.path.dirname(testes)) + len('test_*')) #remove tudo que venha antes do indice do teste
        indice = int(testes[indice_do_teste:-4]) #-4 eh pra remover .txt (tudo que vem depois)
        if indice != i+1:
            indice = 'test_' + str(i + 1) 
            novo_teste = os.path.dirname(testes) + '/'+ indice + '.txt'
            os.rename(testes, novo_teste)

def apaga(lista : list):
    if os.path.exists(gabaritos):
        in_out = os.listdir(gabaritos)
        if len(in_out) > 0:
            test_existe = False
            caminho = gera_caminho(gabaritos)
            for arquivos in caminho:
                casos = gera_caminho(arquivos)
                for testes in casos:
                    for t in lista[1:]:
                        if os.path.basename(testes)[:-4] == t: #compara o arquivo com a entrada do admin para apaga-lo
                            os.remove(testes)
                            test_existe = True

                organiza_testes(arquivos)

            if not test_existe:
                print("Arquivo informado não encontrado")
        else:
            print(f"Comando não executado, pasta {gabaritos} vazia")
    
    else:
        print(f"Comando não executado, pasta {gabaritos} não existe")

def julga():
    caminhos = gera_caminho("Alunos")
    respostas = gera_caminho(f"{gabaritos}/Output")
    entradas = gera_caminho(f"{gabaritos}/Input")

    for pastas in caminhos:
        arquivos = gera_caminho(pastas)
        for tem_c in arquivos:
            if tem_c.endswith('.c'):
                resultados = os.path.join(pastas, 'Resultados')
                
                if not os.path.exists(resultados):
                    os.mkdir(resultados)
                    os.mkdir(os.path.join(resultados, "Casos"))

                else:
                    shutil.rmtree(resultados)
                    os.mkdir(resultados)
                    os.mkdir(os.path.join(resultados, "Casos"))


                comando = ['gcc', '-o', os.path.join(resultados, os.path.basename(tem_c[:-2])) + '.exe', tem_c]
                
                with open(f'{resultados}/resumo.txt', 'w') as resumo:
                    try:
                        relatorio = subprocess.run(comando, text=True, capture_output=True, check=True, timeout=15)
                        resumo.write('COMPILADO')

                    except subprocess.CalledProcessError as c:
                        resumo.write('ERRO DE COMPILACAO')
                        resumo.write(c.stderr)
                        exit()
                    
                    except subprocess.TimeoutExpired:
                        resumo.write('TEMPO DE COMPILACAO EXCEDIDO')
                        exit()

                contador = 0
                i = 0
                erros = []
                for inputs, outputs in zip(entradas, respostas):
                    string = f'./{os.path.join(resultados, os.path.basename(tem_c[:-2]))}' + '.exe'
                    comando = [string] 
                    i += 1
                    with open(inputs, 'r') as en:
                        inputa = en.read()
                        try:
                            relatorio = subprocess.run(comando, text=True, capture_output=True, input=inputa, timeout=5)
                            saida = relatorio.stdout
                            with open(f'{resultados}/Casos/test_{i}.txt', 'w', encoding='UTF-8', newline='\n') as out:
                                out.write(saida)

                                try:
                                    with open(outputs, 'r') as gabarito:
                                        if saida.strip() == gabarito.read().strip():
                                            contador += 1
                                        else:
                                            erros.append(i)

                                except FileNotFoundError:
                                    print('DEU MERDA')
                                    exit(1)


                        except subprocess.TimeoutExpired:
                            with open(f'{resultados}/Casos/test_{i}.txt', 'w', encoding='UTF-8', newline='\n') as out:
                                out.write('Tempo expirado')

                print(f'{os.path.basename(pastas)}', end=': ') #imprime no terminal o nome do aluno
                with open(f'{resultados}/acertos.txt', 'w') as outs:
                    outs.write(f'ACERTOU {contador}/{len(entradas)}\n')
                    print(f'ACERTOU {contador}/{len(entradas)}') #imprime no terminal a pct de acertos do aluno

                    if len(erros) > 0:
                        outs.write('\nERROS: \n')
                        outs.write('-------------------\n')
                        for j in erros:
                            outs.write(f'test_{j}\n')
                        outs.write('-------------------\n')

                os.remove(os.path.join(resultados, os.path.basename(tem_c[:-2]) + '.exe'))
