import subprocess
import os
import platform
from pathlib import PurePosixPath, PureWindowsPath

sistema = platform.system()
nome_venv_win = 'venv_win'
nome_venv_lin = 'venv_lin'
pyinstaller_win = os.path.join('venv_win', 'Scripts', 'pyinstaller.exe')
pyinstaller_lin = os.path.join('venv_lin', 'bin', 'pyinstaller')

def troca_pyinstaller_by_python(caminho_str):
    return caminho_str.replace('pyinstaller', 'python')

def verifica_pyinstaller(caminho_pyinstaller):
    if not os.path.exists(caminho_pyinstaller):
        print('Não encontrado pyinstaller, estamos instalando...')

        print(caminho_pyinstaller)
        print('-' * 50)
        try:
            subprocess.run(['pip', 'install', 'pyinstaller'], capture_output=True, check=True)
            print('Instalado com sucesso')

        except subprocess.CalledProcessError as e:
            print(e.stderr.decode())
            exit(1)

        except Exception as e:
            print(e)
            exit(1)

        print('-' * 50)

def build_windows(arquivo):
    global pyinstaller_win

    print("--- Iniciando build para windows ---")

    verifica_pyinstaller(pyinstaller_win)

    pyinstaller_win = troca_pyinstaller_by_python(pyinstaller_win) #troca para rodar de fato pyinstaller
    comando_win = [str(PureWindowsPath(pyinstaller_win)), '-m', 'PyInstaller', '--onefile', arquivo, '--icon=icone.ico']
    print(comando_win)

    if sistema == 'Linux':
        subprocess.run(['cmd.exe', '/c'] + comando_win)

    elif sistema == 'Windows':
        subprocess.run(comando_win)

def build_linux(arquivo):
    global pyinstaller_lin

    print("--- Iniciando build para linux ---")

    verifica_pyinstaller(pyinstaller_lin)

    pyinstaller_lin = troca_pyinstaller_by_python(pyinstaller_lin)
    comando_lin = [str(PurePosixPath(pyinstaller_lin)), '-m', 'PyInstaller', '--onefile', arquivo]
        
    if sistema == 'Windows':
        subprocess.run(['wsl'] + comando_lin)

    elif sistema == 'Linux':
        subprocess.run(comando_lin)

if __name__ == "__main__":
    arquivo = input('Informe o arquivo a ser transformado em executavel\n')

    if (not arquivo.endswith('.py')):
        print('O arquivo deve ser do tipo .py')
        exit(1)

    lista_caminhos = os.listdir()

    if not nome_venv_win in lista_caminhos:
        print(f'Não encontrada a vm (nome correto {nome_venv_win})  para windows')

    else:
        build_windows(arquivo)
        

    if not nome_venv_lin in lista_caminhos:
        print(f'Não encontrada a vm (nome correto {nome_venv_lin})  para Linux')

    else:
        build_linux(arquivo)    


#feito by Bernardo Matos : GitHub (BartSOS)