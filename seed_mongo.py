"""
Script para popular o banco de dados MongoDB com dados de interesses dos clientes.
Colecao: 'interesses'
"""
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "bd2")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "interesses")

def seed_mongo():
    cliente = MongoClient(MONGO_URI)
    db = cliente[MONGO_DB]
    colecao = db[MONGO_COLLECTION]
    
    # Limpa dados anteriores
    colecao.delete_many({})
    
    # Documentos com interesses dos clientes
    interesses_docs = [
        {
            "id_cliente": 1,
            "nome": "Ana Silva",
            "interesses": ["tecnologia", "programacao", "leitura", "games"],
            "resumo": "Profissional de TI apaixonada por inovacao"
        },
        {
            "id_cliente": 2,
            "nome": "Bruno Costa",
            "interesses": ["esportes", "basquete", "fitness", "tecnologia"],
            "resumo": "Atleta amador e entusiasta de esportes"
        },
        {
            "id_cliente": 3,
            "nome": "Carlos Oliveira",
            "interesses": ["tecnologia", "design", "games", "cinema"],
            "resumo": "Designer grafico e gamer casual"
        },
        {
            "id_cliente": 4,
            "nome": "Diana Ferreira",
            "interesses": ["games", "esportes", "streaming", "fitness"],
            "resumo": "Streamer de games e fitness enthusiast"
        },
        {
            "id_cliente": 5,
            "nome": "Etienne Morales",
            "interesses": ["cinema", "leitura", "musica", "artes"],
            "resumo": "Cinefilo e apreciador de artes"
        },
        {
            "id_cliente": 6,
            "nome": "Fernanda Lima",
            "interesses": ["tecnologia", "programacao", "leitura", "negocios"],
            "resumo": "Entrepreneur focada em tech startups"
        }
    ]
    
    # Insere os documentos
    resultado = colecao.insert_many(interesses_docs)
    print(f"[MongoDB] Inseridos {len(resultado.inserted_ids)} documentos de interesses")
    
    # Verifica os dados inseridos
    total = colecao.count_documents({})
    print(f"[MongoDB] Total de interesses no banco: {total}")
    
    cliente.close()

if __name__ == "__main__":
    try:
        seed_mongo()
        print("Sucesso: MongoDB populado com dados de interesses!")
    except Exception as e:
        print(f"Erro ao popular MongoDB: {e}")
