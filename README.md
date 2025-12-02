# Banco de Dados II

Este repositório contém o projeto final da disciplina **Banco de Dados II**. O objetivo do projeto é integrar dados estruturados e semiestruturados utilizando PostgreSQL e Python.

## Estrutura do Projeto

- **`integracao.py`**: Script Python responsável por conectar ao banco de dados PostgreSQL, ler os dados da tabela `Peca` e integrar com os dados do arquivo XML `Fornecimento.xml`.
- **`postcriatab.sql`**: Script SQL para criação das tabelas e inserção de dados no banco de dados PostgreSQL.
- **`Fornecimento.xml`**: Arquivo XML contendo dados semiestruturados para integração.

## Como Executar

1. **Configurar o Banco de Dados:**
   - Certifique-se de que o PostgreSQL está instalado e em execução.
   - Execute o script `postcriatab.sql` para criar as tabelas e inserir os dados.

2. **Configurar o Ambiente Python:**
   - Instale as dependências necessárias (como `psycopg2`).
   - Atualize as credenciais de conexão no arquivo `integracao.py`.

3. **Executar o Script:**
   - No terminal, execute:
     ```bash
     python integracao.py
     ```

## Resultado

O script realiza a junção entre os dados da tabela `Peca` e os dados do arquivo `Fornecimento.xml`, exibindo o resultado no terminal.

## Autor

- **Luanim**

---

Este projeto foi desenvolvido como parte da avaliação final da disciplina. Para dúvidas ou sugestões, entre em contato.
