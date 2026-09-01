# Dockerfile para compilar um executável Python para Linux e Windows usando PyInstaller

# Build para Linux
FROM python:3.11-slim AS linux
WORKDIR /dir

ARG SCRIPT_NAME=main.py
ARG EXE_NAME=main
ARG ICO_NAME=icone.ico

COPY . .

RUN apt-get update && apt-get install -y binutils
RUN pip install --no-cache-dir pyinstaller pipreqs
RUN pipreqs . --force
RUN sed -i 's/==.*//' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pyinstaller --onefile ${SCRIPT_NAME} --icon=${ICO_NAME} --name=${EXE_NAME}


# Build para Windows
FROM tobix/pywine:3.10 AS windows
WORKDIR /dir

ARG SCRIPT_NAME=main.py
ARG EXE_NAME=main
ARG ICO_NAME=icone.ico

COPY . .

RUN wine pip install --no-cache-dir pyinstaller pipreqs
RUN wine pipreqs . --force
RUN sed -i 's/==.*//' requirements.txt
RUN wine pip install --no-cache-dir "numpy<1.24.0" "scipy<1.10.0"
RUN wine pip install --no-cache-dir -r requirements.txt
RUN wine pyinstaller --onefile ${SCRIPT_NAME} --icon=${ICO_NAME} --name=${EXE_NAME}

# Destino final
FROM scratch AS destino

ARG EXE_NAME=main

COPY --from=linux /dir/dist/${EXE_NAME} /linux_build/${EXE_NAME}
COPY --from=windows /dir/dist/${EXE_NAME}.exe /windows_build/${EXE_NAME}.exe