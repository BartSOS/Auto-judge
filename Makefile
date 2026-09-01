EXE ?= main
SCRIPT ?= main.py
ICO ?= icone.ico

all : build

build :
	@echo "Compilando o script ${SCRIPT} para Linux e Windows..."
	docker build \
	--build-arg SCRIPT_NAME=${SCRIPT} \
	--build-arg EXE_NAME=${EXE} \
	--build-arg ICO_NAME=${ICO} \
	--output type=local,dest=./executaveis .
	@echo "Compilação concluída. Os executáveis estão disponíveis na pasta 'executaveis'."


clean :
	@echo "Limpando arquivos temporários..."
	rm -rf executaveis
	@echo "Arquivos temporários removidos."