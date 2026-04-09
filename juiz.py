import os
import shutil
import subprocess
import random

class Juiz:
    def __init__(self):
        self.__diretorio_atual = os.listdir()
        self.__gabaritos = "Gabaritos"
        self.__casos = "Casos"
        self.__faluno = 'Alunos'
        self.__lista_limites_max = []
        self.__lucky = 1
        self.__ocultos = 0
        self.__separador = "NULL"
        self.__childrens_gabaritos = []
        self.__childrens_alunos = []

    def update_childrens(self):
        create(self.__gabaritos)
        self.__childrens_gabaritos = gera_caminho(self.__gabaritos)
        create(self.__faluno)
        self.__childrens_alunos = gera_caminho(self.__faluno)
        self.__lista_limites_max = []

    def push_back_test(self, arquivo_desejado : str, pasta_desejada : str):
        testes = gera_caminho(pasta_desejada) #array com todos os testes

        if (len(testes) == 0):
            indice_final = 0

        else:
            indice_final = os.path.basename(testes[-1]).strip('.txt') #pega a string do ultimo teste (test_5)
            indice_final = int(indice_final.split('_')[1]) #pega a parte inteira (5)

        if os.path.exists(arquivo_desejado):
            nome_original = arquivo_desejado
            mascara = "#######"

            os.rename(arquivo_desejado, mascara) #evita nome igual 
            arquivo_desejado = mascara

            novo_nome = os.path.join(pasta_desejada, f'test_{indice_final + 1}.txt') #adiciona ao novo teste da pasta o indice_final + 1

            shutil.move(arquivo_desejado, pasta_desejada) 
            arquivo_desejado = os.path.join(pasta_desejada, arquivo_desejado)

            os.rename(arquivo_desejado, novo_nome) 
            print(f"Arquivo {nome_original} sendo movido para pasta {pasta_desejada}")

        else:
            print(f"Arquivo {arquivo_desejado} não existe")

    def adiciona_teste(self, pasta_desejada : str, arquivos_desejados : list | None = None):
        pasta_desejada = os.path.join(self.__gabaritos, pasta_desejada)

        if os.path.exists(pasta_desejada):

            if arquivos_desejados is None:
                for arquivos in self.__diretorio_atual:
                    if arquivos.endswith('.txt'): #arquivos para gerar testes (ex.: Input, Output)
                        self.push_back_test(arquivos, pasta_desejada)
            else:
                for arquivo_desejado in arquivos_desejados:
                    self.push_back_test(arquivo_desejado, pasta_desejada)
        
        else:
            print(f"Pasta {pasta_desejada} não existe")
        
    def le_txt_e_gera_casos_de_teste(self, arquivo_base_txt : str):
        testes = []
        string_base = arquivo_base_txt.read() #pega tudo do .txt

        if (self.__separador != "NULL"):
            testes = string_base.split(self.__separador) #separa conforme separador

        else:
            testes.append(string_base) #caso contrario pega tudo

        if (len(self.__lista_limites_max) > 0):  #avalia necessidade de lucky
            lista_sorted = []
            i = 0
            j = 0
            while j < len(testes):
                lista_sorted.append("".join(testes[j:j+self.__lista_limites_max[i]]))
                j += self.__lista_limites_max[i]
                i += 1

            return lista_sorted

        return testes


    def gera_testes(self, arquivos : str):
        self.randomriza_qtd_testes() 
        
        if os.path.exists(arquivos): #so eh pra gerar testes se o arquivo de In_Out.txt existir
            in_out = arquivos[:-4] #pega só o nome
            diretorio = os.path.join(self.__gabaritos, in_out)  #cria pasta de Input or Output
            create_if_not_exist(diretorio)
            
            with open(arquivos, 'r') as arq:
                testes = self.le_txt_e_gera_casos_de_teste(arq)
                
                for i, grupo in enumerate(testes):
                    caminho_visivel = os.path.join(self.__gabaritos, in_out, f'test_{i+1}.txt')
                    caminho_oculto = os.path.join(self.__gabaritos, in_out, "Casos_Ocultos", f'oculto_{i+1}.txt')

                    if (i < self.__ocultos):
                        if (i == 0):
                            os.mkdir(os.path.join(in_out, "Casos_Ocultos"))
                        escreve_binario(caminho_oculto, cifra_codigo(grupo, 42))

                    with open(caminho_visivel, 'w', encoding='UTF-8', newline='\n') as test:
                        test.write(grupo)                    

            os.remove(arquivos) #remove o .txt base    

        else:
            print(f"Arquivo {arquivos} não encontrado")

    def randomriza_qtd_testes(self):
        if (self.__lucky != 1):
            for i in range(0, 20):
                limite = random.randint(1, self.__lucky)
                self.__lista_limites_max.append(limite)

    def pastifica(self):
        for arquivos in self.__diretorio_atual:
            if arquivos.endswith('.txt'): #arquivos para gerar testes (ex.: Input, Output)
                self.gera_testes(arquivos)

            elif arquivos.endswith('.c'): #codigos dos alunos
                caminho_do_c = os.path.join(self.__faluno, arquivos.strip('.c'))
                if not os.path.exists(caminho_do_c):
                    os.mkdir(caminho_do_c)
                    shutil.move(arquivos, caminho_do_c)  

    def organiza_testes(self, pasta : str): #organiza os testes em ordem, caso estejam não tenha um deles (test_1, test_2, test_4) -> (test_1, test_2, test_3)
        casos = gera_caminho(pasta)
        for i, testes in enumerate(casos):
            indice_do_teste = (len(os.path.dirname(testes)) + len('test_*')) #remove tudo que venha antes do indice do teste
            indice = int(testes[indice_do_teste:-4]) #-4 eh pra remover .txt (tudo que vem depois)
            if indice != i+1:
                indice = 'test_' + str(i + 1) 
                novo_teste = os.path.dirname(testes) + '/'+ indice + '.txt'
                os.rename(testes, novo_teste)

    def apaga(self, lista_de_testes : list):
        if len(self.__childrens_gabaritos) == 2:
            In, Out = [children for children in self.__childrens_gabaritos]
            casos_In = gera_caminho(In)
            casos_Out = gera_caminho(Out)

            casos_in_final = [os.path.basename(test) for test in casos_In]
            casos_out_final = [os.path.basename(test) for test in casos_Out]

            for t in lista_de_testes:
                if ((not (t in casos_in_final and t in casos_out_final)) and (t in casos_in_final or t in casos_out_final)):
                    pasta = Out
                    if (t in casos_in_final):
                        pasta = In

                    print(f"Teste {t} presente em somente {pasta}")

                elif (t in casos_in_final and t in casos_out_final):
                    os.remove(os.path.join(In, t))
                    os.remove(os.path.join(Out, t)) 
                    print(f'Teste {t} apagado com sucesso')

                else:
                    print(f'Teste {t} não encontrado em nenhum pasta')

            self.organiza_testes(In)
            self.organiza_testes(Out)

        else:
            print(f"Falta a pasta de Input ou Output ou há pastas a mais")    

    def julga(self):
        for pastas in self.__childrens_alunos:  #pastas = nome de cada aluno
            aluno = Aluno(pastas)
            aluno.compilar()
            aluno.executar()
            aluno.imprime_dados_finais_aluno()
                
    def set_lucky(self, lucky : int):
        self.__lucky = lucky

    def set_separador(self, separador : str):
        self.__separador = separador

    def set_oculto(self, oculto : int):
        self.__ocultos = oculto

def gera_caminho(diretorio : str) -> list:  #retorna todos os arquivos dentro de uma certa pasta
    try:
        lista = os.listdir(diretorio)
    except FileNotFoundError:
        print(f'DEU MERDA, ARQUIVO {diretorio} NAO ENCONTRADO')
        exit()   

    array = []
    for arquivos in lista:
        array.append(f'{diretorio}/{arquivos}')

    return sorted(array, key=lambda palavra: (len(palavra), palavra))

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
        print(msg)
        w.write(msg)

def le_binario(file_name : str) -> str:
    with open(file_name, "r", encoding='utf-8') as r:
        leitura = r.read()
        msg = "".join(chr(ord(letra) - 1425) for letra in leitura)
        return msg

class Aluno:
    def __init__(self, diretorio_do_aluno : str):
        self.__diretorio_atual = gera_caminho(diretorio_do_aluno)
        self.__codigo_c = next((tem_c for tem_c in self.__diretorio_atual if tem_c.endswith('.c')), "NULL")  #pega o primeiro cod.c do aluno
        self.__fresultados = "Resultados"

        if (self.__codigo_c != "NULL"):
            self.__resultados = os.path.join(diretorio_do_aluno, self.__fresultados)
            create_if_not_exist(self.__resultados)

            self.__codigo_exe = os.path.basename(self.__codigo_c[:-2]) + '.exe'
            self.__codigo_exe = os.path.join(self.__resultados, self.__codigo_exe)
            os.mkdir(os.path.join(self.__resultados, "Casos"))

        self.__contador = 0
        self.__erros = []
        self.__respostas = gera_caminho("Gabaritos/Output")
        self.__entradas = gera_caminho("Gabaritos/Input")

    def compilar(self):
        if (self.__codigo_c != "NULL"):
            comando = ['gcc', '-o', self.__codigo_exe, self.__codigo_c]
                    
            with open(f'{self.__resultados}/resumo.txt', 'w') as resumo:
                try:
                    relatorio = subprocess.run(comando, text=True, capture_output=True, check=True, timeout=15)
                    resumo.write('COMPILADO')

                except subprocess.CalledProcessError as c:
                    resumo.write('ERRO DE COMPILACAO')
                    resumo.write(c.stderr)
                
                except subprocess.TimeoutExpired:
                    resumo.write('TEMPO DE COMPILACAO EXCEDIDO')

    
    def executar(self):
        for i, (inputs, outputs) in enumerate(zip(self.__entradas, self.__respostas), 1):
            comando = [f'./{self.__codigo_exe}']         

            texto_entrada = None

            if (os.path.basename(inputs).startswith('test_')):
                with open(inputs, 'r') as In:
                    texto_entrada = In.read()

            elif (os.path.basename(inputs).startswith('oculto_')):
                texto_entrada = cifra_codigo(le_binario(inputs), 42)

            if texto_entrada is not None:
                with open(f'{self.__resultados}/Casos/test_{i}.txt', 'w', encoding='UTF-8', newline='\n') as Out: #saida do aluno
                    try:
                        relatorio = subprocess.run(comando, text=True, capture_output=True, input=texto_entrada, timeout=5)
                        Out.write(relatorio.stdout)

                        with open(outputs, 'r') as gabarito: #saida do gabarito
                            if relatorio.stdout.strip() == gabarito.read().strip():
                                self.__contador += 1 #acertou
                            else:
                                self.__erros.append(i) #errou

                    except subprocess.TimeoutExpired:
                        Out.write('Tempo expirado')

    def imprime_dados_finais_aluno(self):    
        print(f'{os.path.basename(self.__codigo_exe)[:-4]}', end=': ') #imprime no terminal o nome do aluno

        with open(f'{self.__resultados}/acertos.txt', 'w') as outs:
            outs.write(f'ACERTOU {self.__contador}/{len(self.__entradas)}\n')
            print(f'ACERTOU {self.__contador}/{len(self.__entradas)}') #imprime no terminal a pct de acertos do aluno

            if len(self.__erros) > 0:
                outs.write('\nERROS: \n')
                outs.write('-------------------\n')
                for j in self.__erros:
                    outs.write(f'test_{j}\n')
                outs.write('-------------------\n')

        os.remove(self.__codigo_exe)
        

#feito por Bernardo Matos, se quiser me chame um dia para visitar o PET, membro do futuro :)
