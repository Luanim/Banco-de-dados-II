"""
Script para visualizar os dados consolidados.
Funciona com Redis ou com o arquivo JSON de fallback.
"""
import json
import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

def visualizar_redis():
    """Exibe dados do Redis."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        r.ping()
        
        print("\n" + "="*60)
        print("DADOS NO REDIS")
        print("="*60)
        
        chaves_cliente = r.keys("cliente:*")
        
        for chave in sorted(chaves_cliente):
            if ":" in chave and chave.count(":") == 1:  # Apenas cliente:id
                cid = chave.split(":")[1]
                
                print(f"\n--- Cliente {cid} ---")
                
                # Dados basicos
                dados = r.hgetall(chave)
                for k, v in dados.items():
                    print(f"  {k}: {v}")
                
                # Amigos
                amigos = r.lrange(f"cliente:{cid}:amigos", 0, -1)
                if amigos:
                    print(f"  amigos: {amigos}")
                
                # Interesses
                interesses = r.get(f"cliente:{cid}:interesses")
                if interesses:
                    int_dict = json.loads(interesses)
                    if int_dict:
                        print(f"  interesses: {int_dict.get('interesses', [])}")
                
                # Compras (resumo)
                compras = r.lrange(f"cliente:{cid}:compras", 0, -1)
                if compras:
                    print(f"  total de compras: {len(compras)}")
                    for i, comp_json in enumerate(compras[:2], 1):  # Mostra apenas as 2 primeiras
                        comp = json.loads(comp_json)
                        print(f"    {i}. {comp.get('produto', {}).get('produto')} - R$ {comp.get('produto', {}).get('valor')}")
                    if len(compras) > 2:
                        print(f"    ... e mais {len(compras) - 2} compra(s)")
        
        return True
    except Exception as e:
        print(f"[AVISO] Redis nao disponivel: {e}")
        return False

def visualizar_json():
    """Exibe dados do arquivo JSON."""
    try:
        if not os.path.exists("dados_consolidados.json"):
            print("[ERRO] Arquivo 'dados_consolidados.json' nao encontrado.")
            print("Execute 'python integracao.py' primeiro para gerar o arquivo.")
            return False
        
        print("\n" + "="*60)
        print("DADOS NO ARQUIVO JSON")
        print("="*60)
        
        with open("dados_consolidados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        for cid, payload in dados.items():
            print(f"\n--- Cliente {cid} ---")
            
            cli = payload.get("cliente", {})
            print(f"  Nome: {cli.get('nome')}")
            print(f"  CPF: {cli.get('cpf')}")
            print(f"  Email: {cli.get('email')}")
            print(f"  Cidade: {cli.get('cidade')}")
            
            # Amigos
            amigos = payload.get("amigos", [])
            if amigos:
                print(f"  Amigos: {amigos}")
            else:
                print(f"  Amigos: Nenhum")
            
            # Interesses
            interesses = payload.get("interesses", {})
            if interesses.get("interesses"):
                print(f"  Interesses: {interesses.get('interesses')}")
            else:
                print(f"  Interesses: Nenhum registrado")
            
            # Compras
            compras = payload.get("compras", [])
            print(f"  Total de compras: {len(compras)}")
            for i, comp in enumerate(compras[:2], 1):
                prod = comp.get("produto", {})
                print(f"    {i}. {prod.get('produto')} - R$ {prod.get('valor')}")
            if len(compras) > 2:
                print(f"    ... e mais {len(compras) - 2} compra(s)")
        
        return True
    except Exception as e:
        print(f"[ERRO] Ao ler JSON: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("VISUALIZADOR DE DADOS CONSOLIDADOS")
    print("="*60)
    
    # Tenta primeiro Redis, se nao disponivel, usa JSON
    sucesso = visualizar_redis()
    
    if not sucesso:
        sucesso = visualizar_json()
    
    if sucesso:
        print("\n" + "="*60)
        print("Visualizacao concluida!")
        print("="*60)
    else:
        print("\nNenhuma fonte de dados disponivel.")
        print("Execute 'python integracao.py' para gerar os dados.")

if __name__ == "__main__":
    main()
