# Estágio 1: Build com dependências de compilação e download de modelos
FROM python:3.9-slim as builder

WORKDIR /usr/src/app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python
COPY requirements.txt ./
RUN pip wheel --no-cache-dir --wheel-dir /usr/src/app/wheels -r requirements.txt

# --- Baixa os modelos de LLM durante o build ---
COPY download_models.py ./
# Instala as dependências e executa o script de download
RUN pip install --no-cache /usr/src/app/wheels/* && \
    python download_models.py


# Estágio 2: Imagem final de produção
FROM python:3.9-slim

WORKDIR /usr/src/app

# Define o diretório de cache do Hugging Face para que seja consistente
ENV TRANSFORMERS_CACHE="/usr/src/app/huggingface_cache"

# Instala dependências de sistema para runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpoppler-cpp0v5 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copia as dependências Python pré-compiladas do estágio de build
COPY --from=builder /usr/src/app/wheels /wheels
RUN pip install --no-cache /wheels/*

# --- Copia o cache dos modelos baixados no estágio anterior ---
COPY --from=builder /root/.cache/huggingface ${TRANSFORMERS_CACHE}

# Copia o código da aplicação
COPY ./app ./app
COPY ./.env ./.env
COPY main.py .

# Expõe a porta e define o comando de execução
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]