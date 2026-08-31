import os
import shutil
import subprocess
import random
from utils import *
import juiz

class Explorer:
    def __init__(self):
        self.__diretorio_atual = os.listdir()
        self.__gabaritos = "Gabaritos"
        self.__casos = "Casos"
        self.__faluno = 'Alunos'
        self.__lista_limites_max = []
        self.__lucky = 1
        self.__ocultos = (0,0)
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
            self.__separador = self.__separador.encode().decode('unicode_escape')
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
            diretorio_casos_ocultos = os.path.join(diretorio, "Casos_Ocultos")
            create(diretorio_casos_ocultos)
            
            with open(arquivos, 'r') as arq:
                testes = self.le_txt_e_gera_casos_de_teste(arq)
                start, end = self.__ocultos
                ocultos = testes[start - 1 : end]
                
                for i, grupo in enumerate(ocultos, start - 1):
                    caminho_oculto = os.path.join(diretorio_casos_ocultos, f'oculto_{i+1}.txt')
                    escreve_binario(caminho_oculto, cifra_codigo(grupo, 42))

                for i, grupo in enumerate(testes):
                    caminho_visivel = os.path.join(self.__gabaritos, in_out, f'test_{i+1}.txt')
                    
                    with open(caminho_visivel, 'w', encoding='utf-8', newline='\n') as test:
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
            aluno = juiz.Aluno(pastas)
            aluno.compilar()
            aluno.executar()
            aluno.imprime_dados_finais_aluno()
                
    def set_lucky(self, lucky : int):
        self.__lucky = lucky

    def set_separador(self, separador : str):
        self.__separador = separador

    def set_oculto(self, oculto : tuple[int, int]):
        self.__ocultos = oculto

#feito por Bernardo Matos, se quiser me chame um dia para visitar o PET, membro do futuro :)
