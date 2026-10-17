# Juiz Local em C — Automatizador de Testes e Correção

Ferramenta interativa via linha de comando (CLI) desenvolvida em Python para automatizar a criação de casos de teste (`Input` e `Output`), organização de submissões de alunos em linguagem **C** e correção automática comparando as saídas geradas com os gabaritos.

---

## Sumário

- [Como o Script Funciona](#como-o-script-funciona)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
- [Comandos e Flags](#comandos-e-flags)
  - [Comandos Disponíveis](#comandos-disponíveis)
  - [Flags Opcionais](#flags-opcionais)
- [Fluxo de Uso (Passo a Passo)](#fluxo-de-uso-passo-a-passo)
- [Build de Executáveis (Docker & Make)](#build-de-executáveis-docker--make)

---

## Como o Script Funciona

O sistema é dividido em quatro módulos principais que trabalham em conjunto:

1. **Interface e Parsing (`main.py`)**:
   - Exibe o menu interativo em loop e lê os comandos e flags inseridos pelo usuário (`folder`, `test`, `add`, `del`, `judge`, `quit`/`q`).
   - Valida os argumentos e intervalos passados para as flags `-s` (separador), `-o` (casos ocultos) e `-l` (agrupamento aleatório / *lucky*), tratando erros com exceções customizadas (`ArgumentFlagError` e `IntervalIndefinedError`).

2. **Gerenciamento de Arquivos e Casos de Teste (`explorer.py`)**:
   - **Pastificação (`folder`)**: Varre o diretório raiz. Para cada arquivo `.c` encontrado (ex.: `JoaoSilva.c`), cria uma pasta individual em `Alunos/JoaoSilva/` e move o código-fonte para lá. Para cada arquivo `.txt` na raiz (ex.: `Input.txt`, `Output.txt`), gera automaticamente a estrutura correspondente dentro de `Gabaritos/`.
   - **Geração de Testes (`test`)**: Lê um arquivo `.txt` base, divide os casos de teste utilizando o separador configurado (`-s`), separa eventuais casos ocultos (`-o`) codificando-os em formato ofuscado dentro da subpasta `Casos Ocultos/`, grava os casos visíveis como `test_1.txt`, `test_2.txt`, ..., e remove o arquivo `.txt` base original.
   - **Adição (`add`) e Remoção (`del`)**: Permite adicionar novos arquivos `.txt` ao final da fila de uma pasta de gabarito (calculando automaticamente o próximo índice `test_N.txt`) ou remover casos específicos simultaneamente de `Gabaritos/Input` e `Gabaritos/Output`, reordenando a numeração dos arquivos restantes para evitar saltos nos índices.

3. **Compilação e Correção Automática (`juiz.py`)**:
   - Para cada pasta de aluno dentro de `Alunos/`:
     - Localiza o arquivo `.c` e cria a subpasta `Resultados/` e `Resultados/Casos/`.
     - **Compilação**: Compila o código-fonte com `gcc -o <executavel> <codigo.c> -lm` (com *timeout* de 15 segundos). O status da compilação (`COMPILADO`, `ERRO DE COMPILACAO` + *stderr*, ou `TEMPO DE COMPILACAO EXCEDIDO`) é salvo em `Resultados/resumo.txt`.
     - **Execução**: Executa o binário compilado para cada entrada de `Gabaritos/Input` (decodificando automaticamente entradas `oculto_*.txt` quando presentes), com *timeout* de 5 segundos por caso de teste.
     - **Avaliação**: Salva a saída produzida pelo programa do aluno em `Resultados/Casos/test_i.txt` e compara (ignorando espaços/quebras de linha nas extremidades com `.strip()`) com a saída esperada em `Gabaritos/Output`.
     - **Relatório**: Exibe no terminal o total de acertos (`<Aluno>: ACERTOU X/Y`), gera o arquivo `Resultados/acertos.txt` listando a pontuação e os testes em que houve erro, e remove o executável temporário ao final.

4. **Utilitários e Ofuscação (`utils.py`)**:
   - Funções auxiliares de manipulação de diretórios, ordenação natural de arquivos (`test_1.txt`, `test_2.txt`, ..., `test_10.txt`) e ofuscação de casos ocultos combinando cifra XOR (`chave = 42`) com deslocamento de código Unicode (`+1425`).

---

## Estrutura do Projeto

```text
.
├── main.py          # Ponto de entrada, CLI interativa e validação de comandos/flags
├── explorer.py      # Classe Explorer: organização de pastas e manipulação de testes
├── juiz.py          # Classe Aluno: compilação via GCC, execução e julgamento
├── utils.py         # Funções utilitárias, cifra de casos ocultos e exceções
├── Dockerfile       # Build multi-stage (Linux e Windows via Wine + PyInstaller)
├── Makefile         # Automação do build dos executáveis com Docker
├── icone.ico        # Ícone utilizado na geração dos executáveis
├── Gabaritos/       # (Gerado) Contém as pastas Input/ e Output/ com os casos de teste
│   ├── Input/
│   │   ├── test_1.txt
│   │   └── Casos Ocultos/
│   └── Output/
│       └── test_1.txt
└── Alunos/          # (Gerado) Contém uma pasta para cada aluno avaliado
    └── NomeDoAluno/
        ├── NomeDoAluno.c
        └── Resultados/
            ├── resumo.txt
            ├── acertos.txt
            └── Casos/
                └── test_1.txt
```

---

## Pré-requisitos

- **Python 3.10+**
- **GCC** instalado e disponível no `PATH` do sistema (necessário para o comando `judge` compilar os arquivos `.c` com a flag `-lm`).
- *(Opcional)* **Docker** e **Make**, caso deseje gerar os executáveis standalone para Linux e Windows.

---

## Como Executar

No diretório raiz do projeto, execute:

```bash
python3 main.py
```

O menu interativo será exibido no terminal aguardando um comando.

---

## Comandos e Flags

### Comandos Disponíveis

| Comando | Sintaxe | Descrição |
| :--- | :--- | :--- |
| **`folder`** | `folder [flags]` | Move todos os arquivos `.c` da raiz para pastas individuais em `Alunos/<Nome>/` e gera casos de teste em `Gabaritos/` a partir de todos os arquivos `.txt` na raiz. |
| **`test`** | `test <arquivo.txt> [flags]` | Gera casos de teste em `Gabaritos/<arquivo>/` a partir do arquivo `.txt` especificado (ex.: `test Input.txt -s \n`) e remove o `.txt` original da raiz. |
| **`add`** | `add <pasta> <arq1.txt ... \| .>` | Move os arquivos `.txt` informados (ou `.` para todos os `.txt` da raiz) para dentro de `Gabaritos/<pasta>/`, numerando-os sequencialmente após o último teste existente. |
| **`del`** | `del <test_1.txt> [test_2.txt ...]` | Apaga os casos de teste especificados simultaneamente de `Gabaritos/Input` e `Gabaritos/Output` e renumera os casos restantes em ordem sequencial. |
| **`judge`** | `judge` | Compila os códigos `.c` de todos os alunos em `Alunos/`, executa-os contra os casos de `Gabaritos/Input`, compara com `Gabaritos/Output` e gera os relatórios em `Resultados/`. |
| **`quit` / `q`** | `quit` ou `q` | Encerra a execução do programa. |

### Flags Opcionais

Podem ser utilizadas em conjunto com os comandos `folder` e `test`:

- **`-s <separador>`**: Define o caractere ou sequência que separa cada caso de teste dentro do arquivo `.txt` base (suporta sequências de escape como `\n`). Caso omitida, todo o conteúdo do arquivo será tratado como um único caso de teste.
  - *Exemplo*: `test Input.txt -s \n`
- **`-o <inicio>-<fim>`**: Define um intervalo (1-indexado, inclusivo) de casos de teste que serão armazenados de forma ofuscada na subpasta `Casos Ocultos/oculto_i.txt`.
  - *Exemplo*: `test Input.txt -s \n -o 1-3`
- **`-l <min>-<max>`**: Define um intervalo para agrupar subcasos de forma aleatória ao gerar os testes.
  - *Exemplo*: `test Input.txt -s \n -l 1-5`

---

## Fluxo de Uso (Passo a Passo)

1. **Preparação dos arquivos na raiz**:
   Coloque na pasta raiz do projeto os arquivos `Input.txt` e `Output.txt` (contendo as entradas e saídas separadas, por exemplo, por quebra de linha ou outro delimitador) e os códigos `.c` dos alunos (ex.: `Maria.c`, `Joao.c`).

2. **Organização e geração dos testes**:
   Inicie o script (`python3 main.py`) e utilize o comando `folder` informando o separador:
   ```text
   folder -s \n
   ```
   Isso criará `Gabaritos/Input/test_*.txt`, `Gabaritos/Output/test_*.txt` e moverá os códigos para `Alunos/Maria/Maria.c` e `Alunos/Joao/Joao.c`.

3. **Manutenção de casos de teste (Opcional)**:
   - Para adicionar novos testes a `Input`:
     ```text
     add Input novo_in.txt
     ```
   - Para remover um caso de teste problemático (ex.: `test_3.txt`) tanto de `Input` quanto de `Output`:
     ```text
     del test_3.txt
     ```

4. **Julgamento das submissões**:
   Execute o corretor:
   ```text
   judge
   ```
   O terminal exibirá a pontuação de cada aluno e os detalhes ficarão salvos em `Alunos/<Nome>/Resultados/` (`resumo.txt`, `acertos.txt` e `Casos/`).

---

## Build de Executáveis (Docker & Make)

O projeto conta com um `Dockerfile` multi-stage e um `Makefile` para empacotar o script Python em executáveis standalone para **Linux** e **Windows** utilizando `PyInstaller`:

- **Gerar executáveis**:
  ```bash
  make
  ```
  Os binários gerados serão exportados para:
  - `executaveis/linux_build/main`
  - `executaveis/windows_build/main.exe`

- **Limpar pasta de executáveis**:
  ```bash
  make clean
  ```

---

## Autor

Desenvolvido por **Bernardo Matos** ([@BartSOS](https://github.com/BartSOS)).

