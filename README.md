# Currículo AI - API de OCR e LLM

## Visão Geral

Esta é uma API RESTful construída com Python e FastAPI que automatiza a análise de currículos. A aplicação extrai texto de múltiplos documentos (PDF, JPG, PNG) via OCR, e utiliza modelos de LLM da Hugging Face para:
1. Gerar resumos concisos de cada currículo.
2. Responder a perguntas específicas sobre o conteúdo dos documentos, retornando os candidatos mais relevantes com justificativas.

O projeto é totalmente containerizado com Docker para garantir um setup simples e consistente.

## Tech Stack
- **Backend:** Python 3.9, FastAPI
- **OCR:** PaddleOCR
- **IA / LLM:** Hugging Face Transformers (DistilBERT, DistilBART)
- **Banco de Dados:** MongoDB (para logs de auditoria)
- **Containerização:** Docker, Docker Compose

## Pré-requisitos
- Docker
- Docker Compose (geralmente já vem com o Docker Desktop)
- **Python 3.10** (caso queira rodar localmente sem Docker)

### Instalando o Python 3.10

Baixe e instale o Python 3.10 em https://www.python.org/downloads/release/python-3100/

> **Atenção:** Recomenda-se usar exatamente a versão 3.10 para evitar incompatibilidades.

## Como Executar (Método Recomendado)

Com o Docker em execução, siga estes 3 passos simples para ter todo o ambiente (API + Banco de Dados) rodando em menos de um minuto.

### 1. Clone o Repositório

```bash
git clone <url-do-seu-repositorio>
cd <nome-do-repositorio>
```

### 2. Crie o Arquivo de Ambiente (.env)

Crie um arquivo chamado `.env` na raiz do projeto com o seguinte conteúdo. É assim que a API saberá o endereço do banco de dados na rede Docker.

```env
MONGO_URI=mongodb://mongodb:27017/
DB_NAME=curriculo_ai_logs
COLLECTION_NAME=requests_log
```

### 3. Suba os Containers com Docker Compose

Este único comando irá construir a imagem da API, criar a rede e iniciar os containers da API e do MongoDB na ordem correta.

```bash
docker-compose up --build
```

Aguarde o processo terminar. Você verá os logs da API no seu terminal.

Pronto! A API está rodando e acessível.

- **Documentação Interativa (Swagger):** http://localhost:8000/docs
- **Endpoint Principal:** `POST /api/v1/process`

Para parar todo o ambiente, pressione `CTRL+C` no terminal e depois execute:

```bash
docker-compose down
```

---

## Como Executar Localmente (Sem Docker)

1. **Crie e ative um ambiente virtual:**

```bash
python3.10 -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Configure o arquivo `.env`** (conforme instruções acima).

4. **Inicie a API:**

```bash
uvicorn app.main:app --reload
```

---

## Comandos Úteis do Docker

- **Buildar manualmente a imagem da API:**

```bash
docker build -t curriculo-ai-api .
```

- **Rodar o container manualmente:**

```bash
docker run -p 8000:8000 --env-file .env curriculo-ai-api
```

- **Parar todos os containers:**

```bash
docker-compose down
```