import pymongo
from decouple import config
from datetime import datetime
from typing import Dict, Any, List

# Carrega todas as configurações do arquivo .env
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017/")
DB_NAME = config("DB_NAME", default="curriculo_ai_logs")
COLLECTION_NAME = config("COLLECTION_NAME", default="requests_log")

try:
    print(f"Tentando conectar a {MONGO_URI}...")
    client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info() # Força a conexão para verificar se está ativa
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    collection.create_index([("request_id", pymongo.ASCENDING)], unique=True)
    collection.create_index([("user_id", pymongo.ASCENDING)])
    print(f"Conexão com MongoDB estabelecida com sucesso na base '{DB_NAME}'.")
except Exception as e:
    print(f"Não foi possível conectar ao MongoDB: {e}")
    collection = None

def save_log(log_data: Dict[str, Any]):
    """
    Salva um dicionário de log na coleção do MongoDB.
    """
    if collection is None:
        print("Log não pôde ser salvo pois a conexão com o banco de dados falhou.")
        return

    try:
        if "results" in log_data:
            for result in log_data.get("results", []):
                if "text" in result:
                    del result["text"] 

        collection.insert_one(log_data)
    except Exception as e:
        print(f"Erro ao salvar log no MongoDB: {e}")