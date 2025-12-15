"""
Script para popular o PostgreSQL com dados de clientes, produtos e compras.
Versao Python - nao requer psql.
"""
import psycopg2
from datetime import datetime
import os

PG_DSN = os.getenv("PG_DSN", "dbname=postgres user=postgres password=postgres host=localhost port=5432")

def seed_postgres():
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    
    try:
        # Limpa dados anteriores
        print("[PostgreSQL] Limpando dados anteriores...")
        cur.execute("DELETE FROM compras")
        cur.execute("DELETE FROM produtos")
        cur.execute("DELETE FROM clientes")
        
        # Insere clientes
        print("[PostgreSQL] Inserindo clientes...")
        clientes = [
            (1, '12345678901', 'Ana Silva', 'Rua A, 100', 'Sao Paulo', 'SP', 'ana@email.com'),
            (2, '12345678902', 'Bruno Costa', 'Rua B, 200', 'Rio de Janeiro', 'RJ', 'bruno@email.com'),
            (3, '12345678903', 'Carlos Oliveira', 'Rua C, 300', 'Belo Horizonte', 'MG', 'carlos@email.com'),
            (4, '12345678904', 'Diana Ferreira', 'Rua D, 400', 'Salvador', 'BA', 'diana@email.com'),
            (5, '12345678905', 'Etienne Morales', 'Rua E, 500', 'Curitiba', 'PR', 'etienne@email.com'),
            (6, '12345678906', 'Fernanda Lima', 'Rua F, 600', 'Brasilia', 'DF', 'fernanda@email.com'),
        ]
        
        for id_cli, cpf, nome, endereco, cidade, uf, email in clientes:
            cur.execute(
                "INSERT INTO clientes (id, cpf, nome, endereco, cidade, uf, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (id_cli, cpf, nome, endereco, cidade, uf, email)
            )
        print(f"[PostgreSQL] {len(clientes)} clientes inseridos")
        
        # Insere produtos
        print("[PostgreSQL] Inserindo produtos...")
        produtos = [
            (1, 'Notebook Dell', 3500.00, 50, 'eletronico'),
            (2, 'Teclado Mecanico', 450.00, 100, 'eletronico'),
            (3, 'Mouse Wireless', 150.00, 150, 'eletronico'),
            (4, 'Livro Clean Code', 85.00, 80, 'livro'),
            (5, 'Fone Bluetooth', 250.00, 120, 'eletronico'),
            (6, 'Monitor 27"', 1200.00, 40, 'eletronico'),
            (7, 'Cadeira Gamer', 950.00, 60, 'mobiliario'),
            (8, 'Bola de Basquete', 120.00, 200, 'esportes'),
            (9, 'Bola de Futebol', 95.00, 250, 'esportes'),
            (10, 'Filme DVD - Matrix', 45.00, 30, 'midia'),
        ]
        
        for id_prod, produto, valor, quantidade, tipo in produtos:
            cur.execute(
                "INSERT INTO produtos (id, produto, valor, quantidade, tipo) VALUES (%s, %s, %s, %s, %s)",
                (id_prod, produto, valor, quantidade, tipo)
            )
        print(f"[PostgreSQL] {len(produtos)} produtos inseridos")
        
        # Insere compras
        print("[PostgreSQL] Inserindo compras...")
        compras = [
            (1, 1, datetime(2024, 1, 15), 1),   # Ana comprou Notebook
            (2, 2, datetime(2024, 1, 20), 1),   # Ana comprou Teclado
            (3, 5, datetime(2024, 2, 1), 1),    # Ana comprou Fone
            (4, 4, datetime(2024, 1, 18), 2),   # Bruno comprou Livro
            (5, 8, datetime(2024, 2, 5), 2),    # Bruno comprou Bola Basquete
            (6, 3, datetime(2024, 1, 25), 3),   # Carlos comprou Mouse
            (7, 6, datetime(2024, 2, 10), 3),   # Carlos comprou Monitor
            (8, 7, datetime(2024, 1, 30), 4),   # Diana comprou Cadeira
            (9, 9, datetime(2024, 2, 8), 4),    # Diana comprou Bola Futebol
            (10, 10, datetime(2024, 2, 12), 5), # Etienne comprou Filme
            (11, 1, datetime(2024, 2, 15), 6),  # Fernanda comprou Notebook
            (12, 2, datetime(2024, 2, 18), 6),  # Fernanda comprou Teclado
        ]
        
        for id_comp, id_prod, data, id_cli in compras:
            cur.execute(
                "INSERT INTO compras (id, id_produto, data, id_cliente) VALUES (%s, %s, %s, %s)",
                (id_comp, id_prod, data, id_cli)
            )
        print(f"[PostgreSQL] {len(compras)} compras inseridas")
        
        # Verifica dados
        cur.execute("SELECT COUNT(*) FROM clientes")
        total_cli = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM produtos")
        total_prod = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM compras")
        total_comp = cur.fetchone()[0]
        
        print(f"[PostgreSQL] Total clientes: {total_cli}")
        print(f"[PostgreSQL] Total produtos: {total_prod}")
        print(f"[PostgreSQL] Total compras: {total_comp}")
        
        conn.commit()
        print("[PostgreSQL] Dados comitados com sucesso!")
        
    except Exception as e:
        conn.rollback()
        print(f"[PostgreSQL] Erro: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    try:
        seed_postgres()
        print("\nSucesso: PostgreSQL populado com dados!")
    except Exception as e:
        print(f"\nErro ao popular PostgreSQL: {e}")
