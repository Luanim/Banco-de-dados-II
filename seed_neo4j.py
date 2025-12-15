"""
Script para popular o banco de dados Neo4j com dados de pessoas e amizades.
Cria nodes 'Pessoa' e relacionamentos 'AMIGO_DE'.
"""
import os
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j12345")

def seed_neo4j():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    with driver.session() as session:
        # Limpa dados anteriores
        session.run("MATCH (p:Pessoa) DETACH DELETE p")
        print("[Neo4j] Dados anteriores removidos")
        
        # Cria nodes Pessoa
        pessoas = [
            (1, "12345678901", "Ana Silva"),
            (2, "12345678902", "Bruno Costa"),
            (3, "12345678903", "Carlos Oliveira"),
            (4, "12345678904", "Diana Ferreira"),
            (5, "12345678905", "Etienne Morales"),
            (6, "12345678906", "Fernanda Lima"),
        ]
        
        for id_pessoa, cpf, nome in pessoas:
            session.run(
                "CREATE (:Pessoa {id: $id, cpf: $cpf, nome: $nome})",
                id=id_pessoa,
                cpf=cpf,
                nome=nome
            )
        print(f"[Neo4j] Criados {len(pessoas)} nodes Pessoa")
        
        # Cria relacionamentos AMIGO_DE (amizades bidirecionais)
        amizades = [
            (1, 2),  # Ana e Bruno sao amigos
            (1, 3),  # Ana e Carlos sao amigos
            (2, 4),  # Bruno e Diana sao amigos
            (3, 4),  # Carlos e Diana sao amigos
            (3, 5),  # Carlos e Etienne sao amigos
            (4, 6),  # Diana e Fernanda sao amigos
            (5, 6),  # Etienne e Fernanda sao amigos
            (1, 5),  # Ana e Etienne sao amigos
        ]
        
        for id1, id2 in amizades:
            # Cria relacionamento em ambas as direcoes
            session.run(
                "MATCH (p1:Pessoa {id: $id1}), (p2:Pessoa {id: $id2}) "
                "CREATE (p1)-[:AMIGO_DE]->(p2)",
                id1=id1,
                id2=id2
            )
        print(f"[Neo4j] Criados {len(amizades)} relacionamentos AMIGO_DE")
        
        # Verifica dados inseridos
        resultado = session.run("MATCH (p:Pessoa) RETURN COUNT(p) as total")
        total_pessoas = resultado.single()["total"]
        print(f"[Neo4j] Total de pessoas no banco: {total_pessoas}")
        
        resultado = session.run("MATCH ()-[r:AMIGO_DE]->() RETURN COUNT(r) as total")
        total_amizades = resultado.single()["total"]
        print(f"[Neo4j] Total de amizades no banco: {total_amizades}")
    
    driver.close()

if __name__ == "__main__":
    try:
        seed_neo4j()
        print("Sucesso: Neo4j populado com dados de pessoas e amizades!")
    except Exception as e:
        print(f"Erro ao popular Neo4j: {e}")
