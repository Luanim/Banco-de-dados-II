"""
API FastAPI para consultar dados consolidados.
Endpoints para visualizar clientes, amigos, compras e recomendacoes.
"""
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

app = FastAPI(
    title="API Recomendacao de Compras",
    description="Integra dados de PostgreSQL, MongoDB, Neo4j e Redis",
    version="1.0.0"
)

# Carrega dados do arquivo JSON
def carregar_dados_json():
    """Carrega dados do arquivo JSON se disponivel."""
    if os.path.exists("dados_consolidados.json"):
        with open("dados_consolidados.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.get("/")
def raiz():
    """Endpoint raiz com informacoes sobre a API."""
    return {
        "mensagem": "API de Recomendacao de Compras",
        "versao": "1.0.0",
        "endpoints": {
            "clientes": "/clientes",
            "cliente_detalhe": "/clientes/{id}",
            "cliente_amigos": "/clientes/{id}/amigos",
            "cliente_compras": "/clientes/{id}/compras",
            "cliente_recomendacoes": "/clientes/{id}/recomendacoes",
            "todos": "/todos"
        }
    }

@app.get("/clientes")
def listar_clientes():
    """Lista todos os clientes."""
    dados = carregar_dados_json()
    
    clientes = []
    for cid, payload in dados.items():
        cli = payload.get("cliente", {})
        clientes.append({
            "id": cli.get("id"),
            "nome": cli.get("nome"),
            "cpf": cli.get("cpf"),
            "email": cli.get("email"),
            "cidade": cli.get("cidade")
        })
    
    return {
        "total": len(clientes),
        "clientes": clientes
    }

@app.get("/clientes/{cliente_id}")
def obter_cliente(cliente_id: int):
    """Obtém detalhes de um cliente especifico."""
    dados = carregar_dados_json()
    
    payload = dados.get(str(cliente_id))
    if not payload:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} nao encontrado")
    
    cli = payload.get("cliente", {})
    return {
        "id": cli.get("id"),
        "nome": cli.get("nome"),
        "cpf": cli.get("cpf"),
        "email": cli.get("email"),
        "endereco": cli.get("endereco"),
        "cidade": cli.get("cidade"),
        "uf": cli.get("uf")
    }

@app.get("/clientes/{cliente_id}/amigos")
def obter_amigos(cliente_id: int):
    """Lista amigos de um cliente."""
    dados = carregar_dados_json()
    
    payload = dados.get(str(cliente_id))
    if not payload:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} nao encontrado")
    
    amigos = payload.get("amigos", [])
    
    # Enriquece com dados dos amigos
    amigos_detalhes = []
    for aid in amigos:
        amigo_payload = dados.get(str(aid))
        if amigo_payload:
            amigo_cli = amigo_payload.get("cliente", {})
            amigos_detalhes.append({
                "id": amigo_cli.get("id"),
                "nome": amigo_cli.get("nome"),
                "email": amigo_cli.get("email"),
                "cidade": amigo_cli.get("cidade")
            })
    
    return {
        "cliente_id": cliente_id,
        "total_amigos": len(amigos_detalhes),
        "amigos": amigos_detalhes
    }

@app.get("/clientes/{cliente_id}/compras")
def obter_compras(cliente_id: int):
    """Lista compras de um cliente."""
    dados = carregar_dados_json()
    
    payload = dados.get(str(cliente_id))
    if not payload:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} nao encontrado")
    
    compras = payload.get("compras", [])
    
    compras_formatadas = []
    for compra in compras:
        prod = compra.get("produto", {})
        compras_formatadas.append({
            "id": compra.get("id"),
            "produto": prod.get("produto"),
            "tipo": prod.get("tipo"),
            "valor": prod.get("valor"),
            "data": compra.get("data")
        })
    
    return {
        "cliente_id": cliente_id,
        "total_compras": len(compras_formatadas),
        "valor_total": sum(c.get("valor", 0) for c in compras_formatadas),
        "compras": compras_formatadas
    }

@app.get("/clientes/{cliente_id}/recomendacoes")
def obter_recomendacoes(cliente_id: int):
    """Gera recomendacoes baseado em amigos e interesses."""
    dados = carregar_dados_json()
    
    payload = dados.get(str(cliente_id))
    if not payload:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} nao encontrado")
    
    # Interesses do cliente
    interesses_cli = payload.get("interesses", {}).get("interesses", [])
    
    # Compras dos amigos
    amigos = payload.get("amigos", [])
    produtos_amigos = {}
    
    for aid in amigos:
        amigo_payload = dados.get(str(aid))
        if amigo_payload:
            for compra in amigo_payload.get("compras", []):
                prod = compra.get("produto", {})
                prod_id = prod.get("id")
                if prod_id not in produtos_amigos:
                    produtos_amigos[prod_id] = {
                        "produto": prod.get("produto"),
                        "tipo": prod.get("tipo"),
                        "valor": prod.get("valor"),
                        "comprado_por_amigos": 0,
                        "motivo": ""
                    }
                produtos_amigos[prod_id]["comprado_por_amigos"] += 1
    
    # Filtra recomendacoes por tipo/interesse
    recomendacoes = []
    for prod_id, info in produtos_amigos.items():
        if info["tipo"] in interesses_cli or any(palavra in info["produto"].lower() for palavra in interesses_cli):
            recomendacoes.append({
                "produto": info["produto"],
                "tipo": info["tipo"],
                "valor": info["valor"],
                "motivo": f"Amigos seus compraram. Voce tem interesse em {info['tipo']}",
                "comprado_por": info["comprado_por_amigos"]
            })
    
    return {
        "cliente_id": cliente_id,
        "interesses": interesses_cli,
        "total_recomendacoes": len(recomendacoes),
        "recomendacoes": sorted(recomendacoes, key=lambda x: x["comprado_por"], reverse=True)
    }

@app.get("/todos")
def obter_tudo():
    """Retorna todos os dados consolidados."""
    dados = carregar_dados_json()
    
    resultado = {
        "total_clientes": len(dados),
        "resumo": {}
    }
    
    for cid, payload in dados.items():
        cli = payload.get("cliente", {})
        resultado["resumo"][cid] = {
            "nome": cli.get("nome"),
            "total_compras": len(payload.get("compras", [])),
            "total_amigos": len(payload.get("amigos", [])),
            "interesses": payload.get("interesses", {}).get("interesses", [])
        }
    
    return resultado

@app.get("/health")
def health_check():
    """Verifica saude da API."""
    return {
        "status": "ok",
        "dados_disponiveis": os.path.exists("dados_consolidados.json")
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("API de Recomendacao de Compras")
    print("="*60)
    print("Iniciando servidor...")
    print("Acesse: http://localhost:8000")
    print("Documentacao: http://localhost:8000/docs")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
