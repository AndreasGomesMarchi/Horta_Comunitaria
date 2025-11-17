from pymongo import MongoClient
from datetime import datetime

# URI do MongoDB (ajuste se colocar usuário e senha)
MONGO_URI = "mongodb://localhost:27017"

# Conexão com o MongoDB
try:
    client = MongoClient(MONGO_URI)
    # Testa conexão
    client.admin.command("ping")
    print("✅ Conectado ao MongoDB!")
except Exception as e:
    print("❌ Falha ao conectar no MongoDB:", e)
    client = None  # Evita erros caso não tenha conexão

# Banco de dados para logs
db_mongo = client["horta_logs"] if client else None

def log_action(collection_name: str, action: str, details: dict, user: str = None):
    """
    Registra uma ação no MongoDB.

    Args:
        collection_name (str): Nome da coleção (ex: "cultivos", "usuarios").
        action (str): Tipo de ação (ex: "create", "update", "delete").
        details (dict): Informações do registro.
        user (str, opcional): Usuário responsável pela ação.
    """
    if db_mongo is None:
        print("⚠️ Não é possível logar: banco MongoDB não conectado.")
        return

    collection = db_mongo[collection_name]
    log_entry = {
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow()
    }
    if user:
        log_entry["user"] = user

    try:
        collection.insert_one(log_entry)
        print(f"📌 Log inserido na coleção '{collection_name}': {action}")
    except Exception as e:
        print("❌ Erro ao inserir log no MongoDB:", e)
