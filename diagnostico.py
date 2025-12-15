"""
Script para diagnosticar e corrigir problemas de conexao com os bancos de dados.
Testa cada banco individualmente e fornece recomendacoes.
"""
import os
import sys

def testar_postgres():
    print("\n" + "="*60)
    print("Testando PostgreSQL...")
    print("="*60)
    try:
        import psycopg2
        pg_dsn = os.getenv("PG_DSN", "dbname=postgres user=postgres password=postgres host=localhost port=5432")
        conn = psycopg2.connect(pg_dsn)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM clientes;")
        total = cur.fetchone()[0]
        cur.close()
        conn.close()
        print(f"✓ PostgreSQL conectado com sucesso!")
        print(f"  Total de clientes: {total}")
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar ao PostgreSQL: {e}")
        print("  Certifique-se de que PostgreSQL esta rodando")
        print("  Verifique as credenciais no arquivo integracao.py")
        return False

def testar_mongo():
    print("\n" + "="*60)
    print("Testando MongoDB...")
    print("="*60)
    try:
        from pymongo import MongoClient
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        mongo_db = os.getenv("MONGO_DB", "bd2")
        mongo_coll = os.getenv("MONGO_COLLECTION", "interesses")
        
        cliente = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Testa a conexao
        cliente.admin.command('ismaster')
        
        colecao = cliente[mongo_db][mongo_coll]
        total = colecao.count_documents({})
        cliente.close()
        
        print(f"✓ MongoDB conectado com sucesso!")
        print(f"  Total de documentos em '{mongo_coll}': {total}")
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar ao MongoDB: {e}")
        print("  Certifique-se de que MongoDB esta rodando")
        print("  URI padrao: mongodb://localhost:27017")
        return False

def testar_neo4j():
    print("\n" + "="*60)
    print("Testando Neo4j...")
    print("="*60)
    try:
        from neo4j import GraphDatabase
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_pass = os.getenv("NEO4J_PASSWORD", "neo4j")
        
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
        
        with driver.session() as session:
            resultado = session.run("MATCH (p:Pessoa) RETURN COUNT(p) as total")
            total = resultado.single()["total"] if resultado else 0
        
        driver.close()
        
        print(f"✓ Neo4j conectado com sucesso!")
        print(f"  Total de nodos Pessoa: {total}")
        print(f"  URI: {neo4j_uri}")
        print(f"  Usuario: {neo4j_user}")
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar ao Neo4j: {e}")
        print("\n  SOLUCOES:")
        print("  1. Verifique se Neo4j esta rodando (porta 7687 ou 7688)")
        print("  2. Tente resetar a senha padrao do Neo4j:")
        print("     - Acesse: http://localhost:7474")
        print("     - Usuario/Senha padrao: neo4j/neo4j")
        print("     - Se pedido para mudar a senha, use nova senha")
        print("  3. Atualize as variaveis de ambiente:")
        print(f"     $env:NEO4J_URI=\"bolt://localhost:7687\"")
        print(f"     $env:NEO4J_USER=\"neo4j\"")
        print(f"     $env:NEO4J_PASSWORD=\"sua_senha\"")
        print("\n  NOTA: Se ainda nao populou dados no Neo4j, execute:")
        print("     C:/Users/luant/AppData/Local/Python/pythoncore-3.14-64/python.exe seed_neo4j.py")
        return False

def testar_redis():
    print("\n" + "="*60)
    print("Testando Redis...")
    print("="*60)
    try:
        import redis
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_db = int(os.getenv("REDIS_DB", "0"))
        
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        r.ping()
        
        total_keys = len(r.keys("cliente:*"))
        
        print(f"✓ Redis conectado com sucesso!")
        print(f"  Host: {redis_host}:{redis_port}")
        print(f"  Chaves 'cliente:*': {total_keys}")
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar ao Redis: {e}")
        print("  Certifique-se de que Redis esta rodando")
        print("  URI padrao: localhost:6379")
        return False

def main():
    print("\n" + "="*60)
    print("DIAGNOSTICO DE CONEXAO COM BANCOS DE DADOS")
    print("="*60)
    
    resultados = {
        "PostgreSQL": testar_postgres(),
        "MongoDB": testar_mongo(),
        "Neo4j": testar_neo4j(),
        "Redis": testar_redis(),
    }
    
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    
    for banco, ok in resultados.items():
        status = "✓ OK" if ok else "✗ ERRO"
        print(f"{banco}: {status}")
    
    total_ok = sum(resultados.values())
    total = len(resultados)
    
    print(f"\n{total_ok}/{total} bancos conectados com sucesso")
    
    if total_ok == total:
        print("\n✓ Todos os bancos estao prontos!")
        print("  Proxima etapa: python integracao.py")
    elif total_ok >= 3:
        print("\n⚠ Nem todos os bancos estao conectados.")
        print("  A integracao continuara mesmo com bancos indisponiveis.")
    else:
        print("\n✗ Multiplos bancos com erro. Resolva os problemas antes de continuar.")
        sys.exit(1)

if __name__ == "__main__":
    main()
