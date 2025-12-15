"""
Integracao de quatro bases (PostgreSQL, MongoDB, Neo4j e Redis).
Fluxo: ler dados das fontes, consolidar em memoria e gravar no Redis para consulta.
A API pode chamar a funcao main() ou reaproveitar as funcoes abaixo.
"""
import json
import os
from typing import Dict, List, Any

import psycopg2
from neo4j import GraphDatabase
from pymongo import MongoClient
import redis

# Configuracoes via variaveis de ambiente (ajuste conforme seu ambiente)
PG_DSN = os.getenv("PG_DSN", "dbname=postgres user=postgres password=postgres host=localhost port=5432")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "bd2")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "interesses")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j12345")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))


def obter_conexao_postgres():
    try:
        return psycopg2.connect(PG_DSN)
    except Exception as exc:
        raise RuntimeError(f"Falha ao conectar ao PostgreSQL: {exc}") from exc


def obter_cliente_mongo():
    try:
        return MongoClient(MONGO_URI)
    except Exception as exc:
        raise RuntimeError(f"Falha ao conectar ao MongoDB: {exc}") from exc


def obter_driver_neo4j():
    try:
        return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    except Exception as exc:
        raise RuntimeError(f"Falha ao conectar ao Neo4j: {exc}") from exc


def obter_cliente_redis():
    try:
        return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    except Exception as exc:
        raise RuntimeError(f"Falha ao conectar ao Redis: {exc}") from exc


def buscar_postgres() -> Dict[str, Any]:
    """Coleta clientes, compras e produtos no relacional."""
    try:
        with obter_conexao_postgres() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, cpf, nome, endereco, cidade, uf, email FROM clientes;")
                clientes = cur.fetchall()
                cur.execute("SELECT id, id_produto, data, id_cliente FROM compras;")
                compras = cur.fetchall()
                cur.execute("SELECT id, produto, valor, quantidade, tipo FROM produtos;")
                produtos = cur.fetchall()

        dados = {
            "clientes": [
                {
                    "id": row[0],
                    "cpf": row[1],
                    "nome": row[2],
                    "endereco": row[3],
                    "cidade": row[4],
                    "uf": row[5],
                    "email": row[6],
                }
                for row in clientes
            ],
            "compras": [
                {
                    "id": row[0],
                    "id_produto": row[1],
                    "data": row[2].isoformat() if row[2] else None,
                    "id_cliente": row[3],
                }
                for row in compras
            ],
            "produtos": [
                {
                    "id": row[0],
                    "produto": row[1],
                    "valor": float(row[2]),
                    "quantidade": row[3],
                    "tipo": row[4],
                }
                for row in produtos
            ],
        }
        return dados
    except Exception as exc:
        print(f"[ERRO] PostgreSQL indisponivel: {exc}")
        raise RuntimeError("PostgreSQL eh obrigatorio. Nao foi possivel continuar.") from exc


def buscar_mongo() -> Dict[int, Dict[str, Any]]:
    """Retorna interesses por id_cliente."""
    try:
        cliente = obter_cliente_mongo()
        colecao = cliente[MONGO_DB][MONGO_COLLECTION]
        docs = colecao.find({})
        interesses = {}
        for doc in docs:
            cid = int(doc.get("id_cliente")) if doc.get("id_cliente") is not None else None
            if cid is None:
                continue
            interesses[cid] = {
                "nome": doc.get("nome"),
                "interesses": doc.get("interesses", []),
                "resumo": doc.get("resumo"),
            }
        cliente.close()
        return interesses
    except Exception as exc:
        print(f"[AVISO] MongoDB indisponivel: {exc}")
        print("[AVISO] Continuando sem dados de interesses...")
        return {}


def buscar_neo4j() -> Dict[int, List[int]]:
    """Retorna amigos por cliente (id -> lista de ids de amigos)."""
    try:
        driver = obter_driver_neo4j()
        amigos: Dict[int, List[int]] = {}
        consulta = (
            "MATCH (c:Pessoa)-[:AMIGO_DE]->(a:Pessoa) "
            "RETURN c.id AS id_cliente, a.id AS id_amigo"
        )
        with driver.session() as session:
            for record in session.run(consulta):
                cid = int(record["id_cliente"])
                aid = int(record["id_amigo"])
                amigos.setdefault(cid, []).append(aid)
        driver.close()
        return amigos
    except Exception as exc:
        print(f"[AVISO] Neo4j indisponivel: {exc}")
        print("[AVISO] Continuando sem dados de amigos...")
        return {}


def consolidar(dpg: Dict[str, Any], interesses: Dict[int, Dict[str, Any]], amigos: Dict[int, List[int]]):
    """Une dados das 3 fontes em um dicionario por cliente."""
    produtos_idx = {p["id"]: p for p in dpg["produtos"]}
    compras_por_cliente: Dict[int, List[Dict[str, Any]]] = {}
    for compra in dpg["compras"]:
        item = compra.copy()
        prod = produtos_idx.get(compra["id_produto"])
        if prod:
            item["produto"] = prod
        compras_por_cliente.setdefault(compra["id_cliente"], []).append(item)

    consolidados = {}
    for cli in dpg["clientes"]:
        cid = cli["id"]
        consolidados[cid] = {
            "cliente": cli,
            "interesses": interesses.get(cid, {}),
            "amigos": amigos.get(cid, []),
            "compras": compras_por_cliente.get(cid, []),
        }
    return consolidados


def gravar_redis(cache: redis.Redis, consolidados: Dict[int, Dict[str, Any]]):
    """Grava no Redis usando hashes e listas; limpa chaves do namespace cliente:* antes."""
    try:
        # Teste de conectividade
        cache.ping()
        
        for key in cache.scan_iter(match="cliente:*"):
            cache.delete(key)

        for cid, payload in consolidados.items():
            base_key = f"cliente:{cid}"
            cli = payload["cliente"]
            
            # Grava dados do cliente como hash (formato chave-valor individual)
            cache.hset(base_key, "id", str(cli.get("id", "")))
            cache.hset(base_key, "cpf", str(cli.get("cpf", "")))
            cache.hset(base_key, "nome", str(cli.get("nome", "")))
            cache.hset(base_key, "cidade", str(cli.get("cidade", "")))
            cache.hset(base_key, "uf", str(cli.get("uf", "")))
            cache.hset(base_key, "email", str(cli.get("email", "")))

            # Grava amigos como lista
            cache.delete(f"{base_key}:amigos")
            amigos = payload.get("amigos", [])
            if amigos:
                for a in amigos:
                    cache.rpush(f"{base_key}:amigos", str(a))

            # Grava compras como lista JSON
            cache.delete(f"{base_key}:compras")
            compras = payload.get("compras", [])
            if compras:
                for c in compras:
                    cache.rpush(f"{base_key}:compras", json.dumps(c, default=str))

            # Grava interesses como string JSON
            cache.set(f"{base_key}:interesses", json.dumps(payload.get("interesses", {})))
            
            # Grava recomendações como string JSON
            cache.set(f"{base_key}:recs", json.dumps(payload.get("recs", [])))
        
        print(f"[Redis] {len(consolidados)} clientes gravados com sucesso!")
        return True
    except Exception as exc:
        print(f"[AVISO] Redis indisponivel: {exc}")
        print("[AVISO] Salvando dados em arquivo JSON em vez de Redis...")
        return False


def salvar_json(consolidados: Dict[int, Dict[str, Any]]):
    """Salva os dados consolidados em um arquivo JSON para consulta."""
    try:
        arquivo = "dados_consolidados.json"
        
        # Converte para formato serializavel
        dados_json = {}
        for cid, payload in consolidados.items():
            dados_json[str(cid)] = {
                "cliente": payload["cliente"],
                "interesses": payload["interesses"],
                "amigos": payload["amigos"],
                "compras": payload["compras"],
            }
        
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_json, f, ensure_ascii=False, indent=2)
        
        print(f"[JSON] Dados consolidados salvos em '{arquivo}'")
        print(f"[JSON] {len(consolidados)} clientes salvos")
        return True
    except Exception as exc:
        print(f"[ERRO] Falha ao salvar JSON: {exc}")
        return False


def main():
    print("[1/5] Lendo PostgreSQL...")
    dpg = buscar_postgres()

    print("[2/5] Lendo MongoDB...")
    interesses = buscar_mongo()

    print("[3/5] Lendo Neo4j...")
    amigos = buscar_neo4j()

    print("[4/5] Consolidando dados...")
    consolidados = consolidar(dpg, interesses, amigos)

    print("[5/5] Gravando dados...")
    cache = obter_cliente_redis()
    redis_ok = gravar_redis(cache, consolidados)
    
    # Sempre salva em JSON como backup
    salvar_json(consolidados)
    
    print("\n" + "="*60)
    print("INTEGRACAO CONCLUIDA COM SUCESSO!")
    print("="*60)
    
    if redis_ok:
        print("✓ Dados gravados no Redis")
        print("\nConsulte com:")
        print("  redis-cli")
        print("  KEYS cliente:*")
        print("  HGETALL cliente:1")
    else:
        print("✓ Dados salvos em JSON: dados_consolidados.json")
        print("  (Redis nao esta disponivel)")
    
    print("\nProximas etapas:")
    print("  1. Visualizar dados: python visualizar_dados.py")
    print("  2. Iniciar API:      python api.py")
    print("  3. Consultar em:     http://localhost:8000")


if __name__ == "__main__":
    main()