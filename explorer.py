import os
import shutil
import re
import random
from utils import *
import juiz


class Explorer:
    def __init__(self):
        self.__diretorio_atual = os.listdir()
        self.__gabaritos = FOLDER_GABARITOS
        self.__faluno = FOLDER_ALUNOS
        self.__childrens_gabaritos = []
        self.__childrens_alunos = []
        self.__lista_limites_max = []
        self.__lucky = None
        self.__ocultos = (0,0)
        self.__separador = None

    def update_childrens(self):
        create(self.__gabaritos)
        self.__childrens_gabaritos = gera_caminho(self.__gabaritos)
        create(self.__faluno)
        self.__childrens_alunos = gera_caminho(self.__faluno)
        self.__lista_limites_max = []
        self.__diretorio_atual = os.listdir()

    def calculate_last_indice(self, array_testes : list) -> int:
        if (not array_testes):
            indice_final = 0

        else:
            def ordenar_pelo_ultimo_numero(caminho):
                numeros = re.findall(r'\d+', caminho)
                ultimo_numero = int(numeros[-1]) if numeros else 0
                texto_base = re.sub(r'\d+$|\d+(?=\D*$)', '', caminho).lower()
                return (ultimo_numero, texto_base)

            array_testes = sorted(array_testes, key=ordenar_pelo_ultimo_numero, reverse=True)
            last_test = next(test for test in array_testes if (re.findall(r'\d+', test))) #pego o ultimo caso de test que contem numero no nome
            indice_final = int(re.findall(r'\d+', last_test)[-1]) #pega o ultimo conjunto de numero e transforma em int

        return indice_final

    def push_back_test(self, teste_novo : str, pasta_desejada : str):
        if not os.path.exists(teste_novo):
            raise FileNotFoundError(f"O arquivo {teste_novo} não existe")
        
        array_testes = gera_caminho(pasta_desejada) #array com todos os testes
        indice_final = self.calculate_last_indice(array_testes)

        print(f"Arquivo {teste_novo} sendo movido para pasta {pasta_desejada}")

        teste_novo = rename_and_update(teste_novo, "name_temp") #evita nome igual dentro da pasta de destino 
        teste_novo = move_and_update(teste_novo, pasta_desejada)
        novo_nome = os.path.join(pasta_desejada, f'test_{indice_final + 1}.txt') #adiciona ao novo teste da pasta o indice_final + 1

        os.rename(teste_novo, novo_nome) 

    def adiciona_teste(self, pasta_desejada : str, files_src : list | None = None):
        pasta_desejada = os.path.join(self.__gabaritos, pasta_desejada)

        if os.path.exists(pasta_desejada):
            if files_src is None:
                for file in self.__diretorio_atual:
                    if file.endswith('.txt'): #arquivos para gerar testes (ex.: Input, Output)
                        self.push_back_test(file, pasta_desejada)
            else:
                for file in files_src:
                    self.push_back_test(file, pasta_desejada)
        
        else:
            print(f"Pasta {pasta_desejada} não existe")
        
    def le_txt_e_gera_casos_de_teste(self, arquivo_base_txt : str) -> list:
        testes = []
        string_base = arquivo_base_txt.read() #pega tudo do .txt

        if (self.__separador is not None):
            self.__separador = self.__separador.encode().decode('unicode_escape')
            testes = string_base.split(self.__separador) #separa conforme separador

            if (self.__lucky is tuple):  #avalia necessidade de lucky
                self.randomriza_qtd_testes(len(testes))
                lista_sorted = []
                i = 0
                j = 0
                while j < len(testes):
                    lista_sorted.append("".join(testes[j:j+self.__lista_limites_max[i]]))
                    j += self.__lista_limites_max[i]
                    i += 1
    
                return lista_sorted

        else:
            testes.append(string_base) #caso contrario pega tudo

        return testes


    def gera_testes(self, file_src : str):
        if not os.path.exists(file_src): #so eh pra gerar testes se o arquivo de In_Out.txt existir
            raise FileNotFoundError(f"Arquivo {file_src} não encontrado")
        
        in_out = file_src.strip('.txt') #pega só o nome
        diretorio = os.path.join(self.__gabaritos, in_out)  #cria pasta de Input or Output
        create_if_not_exist(diretorio)

        ocultos = []
        diretorio_casos_ocultos = os.path.join(diretorio, FOLDER_CASOS_OCULTOS)  #cria if precisar a pasta ocultos
       
        with open(file_src, 'r') as arq:
            testes = self.le_txt_e_gera_casos_de_teste(arq)

            if (self.__ocultos != (0,0)):
                create_if_not_exist(diretorio_casos_ocultos)
                start, end = self.__ocultos
                ocultos = testes[start - 1 : end]
                del testes[start - 1 : end]
    
            else:
                remove_if_exist(diretorio_casos_ocultos)
            
            for i, grupo in enumerate(ocultos):
                caminho_oculto = os.path.join(diretorio_casos_ocultos, f'oculto_{i+1}.txt')
                escreve_binario(caminho_oculto, cifra_codigo(grupo, 42))

            for i, grupo in enumerate(testes):
                caminho_visivel = os.path.join(diretorio, f'test_{i+1}.txt')
                
                with open(caminho_visivel, 'w', encoding='utf-8', newline='\n') as test:
                    test.write(grupo)                    

        os.remove(file_src) #remove o .txt base    

    def randomriza_qtd_testes(self, qtd_max_testes : int):
        soma = 0
        while (soma < qtd_max_testes):
            limite = random.randint(self.__lucky[0], self.__lucky[1])
            self.__lista_limites_max.append(limite)
            soma += limite

    def pastifica(self):
        for arquivos in self.__diretorio_atual:
            if arquivos.endswith('.txt'): #arquivos para gerar testes (ex.: Input, Output)
                self.gera_testes(arquivos)

            elif arquivos.endswith('.c'): #codigos dos alunos
                caminho_do_c = os.path.join(self.__faluno, arquivos.strip('.c'))
                if not os.path.exists(caminho_do_c):
                    os.mkdir(caminho_do_c)
                    shutil.move(arquivos, caminho_do_c)  

    def organiza_testes(self, in_out : str): #organiza os testes em ordem, caso estejam não tenha um deles (test_1, test_2, test_4) -> (test_1, test_2, test_3)
        casos = gera_caminho(in_out)
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
