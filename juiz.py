from utils import *
import subprocess

class Aluno:
    def __init__(self, diretorio_do_aluno : str):
        self.__diretorio_atual = gera_caminho(diretorio_do_aluno)
        self.__codigo_c = next((tem_c for tem_c in self.__diretorio_atual if tem_c.endswith('.c')), "NULL")  #pega o primeiro cod.c do aluno
        self.__fresultados = "Resultados"

        if (self.__codigo_c != "NULL"):
            self.__resultados = os.path.join(diretorio_do_aluno, self.__fresultados)
            create_new_path(self.__resultados)

            self.__codigo_exe = os.path.basename(self.__codigo_c[:-2]) + '.exe'
            self.__codigo_exe = os.path.join(self.__resultados, self.__codigo_exe)
            os.mkdir(os.path.join(self.__resultados, "Casos"))

        self.__contador = 0
        self.__erros = []
        self.__respostas = gera_caminho("Gabaritos/Output")
        self.__entradas = gera_caminho("Gabaritos/Input")

    def compilar(self):
        if (self.__codigo_c != "NULL"):
            comando = ['gcc', '-o', self.__codigo_exe, self.__codigo_c, '-lm']
                    
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