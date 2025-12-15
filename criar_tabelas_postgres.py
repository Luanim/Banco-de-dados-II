"""
Script para criar as tabelas no PostgreSQL.
Execute este script antes de usar seed_postgres.sql
"""
import psycopg2
import os

PG_DSN = os.getenv("PG_DSN", "dbname=postgres user=postgres password=postgres host=localhost port=5432")

def criar_tabelas():
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    
    # Drops anteriores (opcional - comentar se quiser preservar dados)
    try:
        cur.execute("DROP TABLE IF EXISTS compras CASCADE")
        cur.execute("DROP TABLE IF EXISTS produtos CASCADE")
        cur.execute("DROP TABLE IF EXISTS clientes CASCADE")
        print("[PostgreSQL] Tabelas antigas removidas")
    except Exception as e:
        print(f"[PostgreSQL] Aviso ao remover tabelas: {e}")
    
    # Cria tabela clientes
    cur.execute("""
    CREATE TABLE clientes (
        id SERIAL PRIMARY KEY,
        cpf VARCHAR(11) UNIQUE NOT NULL,
        nome VARCHAR(100) NOT NULL,
        endereco VARCHAR(150),
        cidade VARCHAR(50),
        uf VARCHAR(2),
        email VARCHAR(100)
    )
    """)
    print("[PostgreSQL] Tabela 'clientes' criada")
    
    # Cria tabela produtos
    cur.execute("""
    CREATE TABLE produtos (
        id SERIAL PRIMARY KEY,
        produto VARCHAR(100) NOT NULL,
        valor DECIMAL(10, 2) NOT NULL,
        quantidade INTEGER,
        tipo VARCHAR(50)
    )
    """)
    print("[PostgreSQL] Tabela 'produtos' criada")
    
    # Cria tabela compras
    cur.execute("""
    CREATE TABLE compras (
        id SERIAL PRIMARY KEY,
        id_produto INTEGER NOT NULL REFERENCES produtos(id),
        data DATE NOT NULL,
        id_cliente INTEGER NOT NULL REFERENCES clientes(id)
    )
    """)
    print("[PostgreSQL] Tabela 'compras' criada")
    
    conn.commit()
    cur.close()
    conn.close()
    print("[PostgreSQL] Tabelas criadas com sucesso!")

if __name__ == "__main__":
    try:
        criar_tabelas()
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
