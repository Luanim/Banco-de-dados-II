-- Script para popular o banco de dados PostgreSQL
-- Tabelas: clientes, produtos, compras

-- Limpa dados anteriores (opcional)
DELETE FROM compras;
DELETE FROM produtos;
DELETE FROM clientes;

-- Insere clientes
INSERT INTO clientes (id, cpf, nome, endereco, cidade, uf, email) VALUES
(1, '12345678901', 'Ana Silva', 'Rua A, 100', 'Sao Paulo', 'SP', 'ana@email.com'),
(2, '12345678902', 'Bruno Costa', 'Rua B, 200', 'Rio de Janeiro', 'RJ', 'bruno@email.com'),
(3, '12345678903', 'Carlos Oliveira', 'Rua C, 300', 'Belo Horizonte', 'MG', 'carlos@email.com'),
(4, '12345678904', 'Diana Ferreira', 'Rua D, 400', 'Salvador', 'BA', 'diana@email.com'),
(5, '12345678905', 'Etienne Morales', 'Rua E, 500', 'Curitiba', 'PR', 'etienne@email.com'),
(6, '12345678906', 'Fernanda Lima', 'Rua F, 600', 'Brasilia', 'DF', 'fernanda@email.com');

-- Insere produtos
INSERT INTO produtos (id, produto, valor, quantidade, tipo) VALUES
(1, 'Notebook Dell', 3500.00, 50, 'eletronico'),
(2, 'Teclado Mecanico', 450.00, 100, 'eletronico'),
(3, 'Mouse Wireless', 150.00, 150, 'eletronico'),
(4, 'Livro Clean Code', 85.00, 80, 'livro'),
(5, 'Fone Bluetooth', 250.00, 120, 'eletronico'),
(6, 'Monitor 27"', 1200.00, 40, 'eletronico'),
(7, 'Cadeira Gamer', 950.00, 60, 'mobiliario'),
(8, 'Bola de Basquete', 120.00, 200, 'esportes'),
(9, 'Bola de Futebol', 95.00, 250, 'esportes'),
(10, 'Filme DVD - Matrix', 45.00, 30, 'midia');

-- Insere compras (cada cliente tem ao menos 1-3 compras)
INSERT INTO compras (id, id_produto, data, id_cliente) VALUES
(1, 1, '2024-01-15', 1),  -- Ana comprou Notebook
(2, 2, '2024-01-20', 1),  -- Ana comprou Teclado
(3, 5, '2024-02-01', 1),  -- Ana comprou Fone
(4, 4, '2024-01-18', 2),  -- Bruno comprou Livro Clean Code
(5, 8, '2024-02-05', 2),  -- Bruno comprou Bola de Basquete
(6, 3, '2024-01-25', 3),  -- Carlos comprou Mouse
(7, 6, '2024-02-10', 3),  -- Carlos comprou Monitor
(8, 7, '2024-01-30', 4),  -- Diana comprou Cadeira Gamer
(9, 9, '2024-02-08', 4),  -- Diana comprou Bola de Futebol
(10, 10, '2024-02-12', 5), -- Etienne comprou Filme DVD
(11, 1, '2024-02-15', 6),  -- Fernanda comprou Notebook
(12, 2, '2024-02-18', 6);  -- Fernanda comprou Teclado

-- Verifica os dados inseridos
SELECT COUNT(*) as total_clientes FROM clientes;
SELECT COUNT(*) as total_produtos FROM produtos;
SELECT COUNT(*) as total_compras FROM compras;
