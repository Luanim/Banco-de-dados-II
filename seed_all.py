"""
Script orquestrador para popular todos os bancos de dados em sequencia.
Execute este script apos ter criado as tabelas e configurado as conexoes.
"""
import subprocess
import sys
import os

def executar_script(descricao, comando):
    print(f"\n{'='*60}")
    print(f"Executando: {descricao}")
    print(f"{'='*60}")
    try:
        if descricao.startswith("PostgreSQL (SQL)"):
            # Para script SQL, usa psql
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        else:
            # Para scripts Python
            resultado = subprocess.run([sys.executable] + comando.split(), capture_output=True, text=True)
        
        print(resultado.stdout)
        if resultado.stderr:
            print("Erros:", resultado.stderr)
        if resultado.returncode == 0:
            print(f"✓ {descricao} - Sucesso!")
        else:
            print(f"✗ {descricao} - Falhou!")
        return resultado.returncode == 0
    except Exception as e:
        print(f"✗ Erro ao executar {descricao}: {e}")
        return False

def main():
    print("Populador de Bancos de Dados - Projeto Recomendacao de Compras")
    print("="*60)
    
    # Define os scripts e comandos na ordem correta
    scripts = [
        ("PostgreSQL (Criar Tabelas)", "criar_tabelas_postgres.py"),
        ("PostgreSQL (Inserir Dados)", "seed_postgres.sql"),  # Sera executado com psql
        ("MongoDB", "seed_mongo.py"),
        ("Neo4j", "seed_neo4j.py"),
    ]
    
    sucessos = 0
    
    for descricao, script in scripts:
        if descricao == "PostgreSQL (Inserir Dados)":
            # Para SQL, usa psql
            pg_dsn = os.getenv("PG_DSN", "dbname=postgres user=postgres password=postgres host=localhost port=5432")
            # Tenta executar com psql (funciona melhor em PowerShell)
            cmd = f"psql \"{pg_dsn}\" -f {script}"
        else:
            cmd = script
        
        if executar_script(descricao, cmd):
            sucessos += 1
    
    print(f"\n{'='*60}")
    print(f"Resumo: {sucessos}/{len(scripts)} scripts executados com sucesso")
    print(f"{'='*60}")
    
    if sucessos == len(scripts):
        print("\n✓ Todos os bancos foram populados com sucesso!")
        print("\nAgora voce pode executar: python integracao.py")
    else:
        print("\n✗ Alguns scripts falharam. Verifique as mensagens de erro acima.")

if __name__ == "__main__":
    main()
