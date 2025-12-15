# Scripts de Populacao de Dados

Estes scripts criam as tabelas e populam os bancos de dados com dados de exemplo para o projeto de recomendacao de compras.

## Arquivos

### 1. `criar_tabelas_postgres.py`
Cria as tabelas no PostgreSQL:
- `clientes`: dados dos clientes
- `produtos`: catalogo de produtos
- `compras`: historico de compras dos clientes

**Executar:**
```powershell
C:/Users/luant/AppData/Local/Python/pythoncore-3.14-64/python.exe criar_tabelas_postgres.py
```

### 2. `seed_postgres.sql`
Insere dados de exemplo no PostgreSQL.
- 6 clientes
- 10 produtos (eletronicos, livros, esportes, midia)
- 12 compras

**Executar com psql:**
```powershell
psql -U postgres -d postgres -f seed_postgres.sql
```

Ou use um cliente SQL (pgAdmin, DBeaver) para executar o arquivo.

### 3. `seed_mongo.py`
Popula a colecao `interesses` no MongoDB com:
- interesses de cada cliente (tecnologia, esportes, games, leitura, etc)
- resumo/descricao de cada cliente
- 6 documentos (um por cliente)

**Executar:**
```powershell
C:/Users/luant/AppData/Local/Python/pythoncore-3.14-64/python.exe seed_mongo.py
```

### 4. `seed_neo4j.py`
Cria nodes e relacionamentos no Neo4j:
- 6 nodes `Pessoa` (id, cpf, nome)
- 8 relacionamentos `AMIGO_DE` (rede de amigos)

**Executar:**
```powershell
C:/Users/luant/AppData/Local/Python/pythoncore-3.14-64/python.exe seed_neo4j.py
```

### 5. `seed_all.py` (Orquestrador)
Executa todos os scripts em sequencia (opcional).

**Executar:**
```powershell
C:/Users/luant/AppData/Local/Python/pythoncore-3.14-64/python.exe seed_all.py
```

## Ordem de Execucao Recomendada

1. **Criar tabelas no PostgreSQL:**
   ```powershell
   python criar_tabelas_postgres.py
   ```

2. **Popular PostgreSQL com dados:**
   ```powershell
   psql -U postgres -d postgres -f seed_postgres.sql
   ```

3. **Popular MongoDB:**
   ```powershell
   python seed_mongo.py
   ```

4. **Popular Neo4j:**
   ```powershell
   python seed_neo4j.py
   ```

5. **Rodar integracao (consolida no Redis):**
   ```powershell
   python integracao.py
   ```

## Variaveis de Ambiente

Configure antes de rodar os scripts:

```powershell
# PostgreSQL
$env:PG_DSN="dbname=postgres user=postgres password=postgres host=localhost port=5432"

# MongoDB
$env:MONGO_URI="mongodb://localhost:27017"
$env:MONGO_DB="bd2"
$env:MONGO_COLLECTION="interesses"

# Neo4j
$env:NEO4J_URI="bolt://localhost:7687"
$env:NEO4J_USER="neo4j"
$env:NEO4J_PASSWORD="neo4j"

# Redis
$env:REDIS_HOST="localhost"
$env:REDIS_PORT="6379"
$env:REDIS_DB="0"
```

## Verificacao apos Populacao

### PostgreSQL
```sql
SELECT COUNT(*) FROM clientes;   -- Deve retornar 6
SELECT COUNT(*) FROM produtos;   -- Deve retornar 10
SELECT COUNT(*) FROM compras;    -- Deve retornar 12
```

### MongoDB
```javascript
db.interesses.countDocuments({})  // Deve retornar 6
```

### Neo4j
```cypher
MATCH (p:Pessoa) RETURN COUNT(p)  // Deve retornar 6
MATCH ()-[r:AMIGO_DE]->() RETURN COUNT(r)  // Deve retornar 8
```

### Redis (apos rodar integracao.py)
```
KEYS cliente:*           -- Lista todas as chaves
HGETALL cliente:1        -- Dados do cliente 1
LRANGE cliente:1:amigos 0 -1     -- Amigos do cliente 1
LRANGE cliente:1:compras 0 -1    -- Compras do cliente 1
```

## Notas

- Os scripts podem ser executados multiplas vezes (dados sao limpos antes de popular)
- Para reset completo, remova os arquivos e execute novamente
- Para dados diferentes, edite os scripts e customize conforme necessario
