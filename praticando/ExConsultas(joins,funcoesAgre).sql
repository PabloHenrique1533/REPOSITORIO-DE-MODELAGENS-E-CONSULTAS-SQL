create database ecommerce;
use ecommerce;

CREATE TABLE clientes (
    cliente_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    cidade VARCHAR(50),
    estado VARCHAR(2),
    data_cadastro DATE
    );

CREATE TABLE categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE produtos (
    produto_id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT DEFAULT 0,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
);

CREATE TABLE pedidos (
    pedido_id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pendente',
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);

CREATE TABLE itens_pedido (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    produto_id INT,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id),
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
);

CREATE TABLE pagamentos (
    pagamento_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    valor_pago DECIMAL(10,2) NOT NULL,
    metodo VARCHAR(20) CHECK (metodo IN ('Cartão', 'Boleto', 'Pix')),
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id)
);

CREATE TABLE entregas (
    entrega_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    endereco VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'Em Separação',
    data_envio DATE,
    data_entrega DATE,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id)
);

-----------------------------------------------------------------------------
INSERT INTO clientes (nome, email, telefone, cidade, estado)
VALUES
('João Silva', 'joao@email.com', '1199999999', 'São Paulo', 'SP'),
('Maria Souza', 'maria@email.com', '2198888888', 'Rio de Janeiro', 'RJ'),
('Pedro Santos', 'pedro@email.com', '3197777777', 'Belo Horizonte', 'MG'),
('Ana Costa', 'ana@email.com', '4196666666', 'Curitiba', 'PR'),
('Lucas Lima', 'lucas@email.com', '5195555555', 'Porto Alegre', 'RS'),
('Fernanda Alves', 'fernanda@email.com', '6194444444', 'Brasília', 'DF'),
('Carlos Mendes', 'carlos@email.com', '7193333333', 'Salvador', 'BA'),
('Patrícia Rocha', 'patricia@email.com', '8192222222', 'Recife', 'PE'),
('Rafael Oliveira', 'rafael@email.com', '8591111111', 'Fortaleza', 'CE'),
('Juliana Martins', 'juliana@email.com', '6790000000', 'Campo Grande', 'MS');

INSERT INTO categorias (nome)
VALUES
('Eletrônicos'),
('Roupas'),
('Livros'),
('Brinquedos');

INSERT INTO produtos (nome, preco, estoque, categoria_id)
VALUES
('Smartphone', 1500.00, 20, 1),
('Notebook', 3500.00, 10, 1),
('Camiseta', 50.00, 100, 2),
('Calça Jeans', 120.00, 60, 2),
('Livro SQL', 80.00, 40, 3),
('Livro Redes', 100.00, 30, 3),
('Boneca', 70.00, 25, 4),
('Carrinho', 90.00, 20, 4),
('Tablet', 1200.00, 15, 1),
('Fone Bluetooth', 250.00, 50, 1);

INSERT INTO pedidos (cliente_id, data_pedido, status)
VALUES
(1, '2025-09-01 10:00:00', 'Pago'),
(2, '2025-09-02 14:30:00', 'Enviado'),
(3, '2025-09-03 09:15:00', 'Pendente'),
(4, '2025-09-04 16:45:00', 'Pago'),
(5, '2025-09-05 11:20:00', 'Entregue');

INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
VALUES
(1, 1, 1, 1500.00),
(1, 10, 2, 250.00),
(2, 2, 1, 3500.00),
(3, 3, 3, 50.00),
(4, 5, 2, 80.00),
(5, 4, 1, 120.00),
(5, 6, 1, 100.00);

INSERT INTO pagamentos (pedido_id, valor_pago, metodo, data_pagamento)
VALUES
(1, 2000.00, 'Cartão', '2025-09-01 12:00:00'),
(2, 3500.00, 'Pix', '2025-09-02 15:00:00'),
(4, 160.00, 'Boleto', '2025-09-04 17:00:00'),
(5, 220.00, 'Cartão', '2025-09-05 12:00:00');

INSERT INTO entregas (pedido_id, endereco, status, data_envio, data_entrega)
VALUES
(1, 'Rua A, 123 - São Paulo/SP', 'Em Transporte', '2025-09-02', '2025-09-05'),
(2, 'Av. B, 456 - Rio de Janeiro/RJ', 'Entregue', '2025-09-03', '2025-09-07'),
(4, 'Rua C, 789 - Curitiba/PR', 'Em Transporte', '2025-09-05', NULL),
(5, 'Av. D, 321 - Porto Alegre/RS', 'Entregue', '2025-09-06', '2025-09-10');
---------------------------------------------------------------------------------

-- Basico;
-- 1;
select 
c.nome as NomeCliente
from Clientes c
order by c.nome;

-- 2;
select 
p.nome, p.preco, c.nome
from produtos p
inner join categorias c on p.categoria_id = c.categoria_id
where c.nome = 'Eletrônicos'
order by p.nome;

-- 3
select 
pedido_id, data_pedido
from pedidos
where data_pedido between '2025-09-01' and '2025-09-30';

-- 4;
select 
nome, estado, cidade
from clientes
where estado = 'SP';

-- intermediario;
-- 5;
select
nome, pedido_id, status
from clientes 
join pedidos on clientes.cliente_id = pedidos.pedido_id;

-- 6;
select 
pr.nome, i.quantidade,(i.quantidade * i.preco_unitario) as PreçoTotal
from produtos pr
inner join itens_pedido i on pr.produto_id = i.produto_id
where i.pedido_id = 1
order by pr.nome;

-- 7;
select 
p.pedido_id, p.status, pag.valor_pago
from pedidos p 
left join pagamentos pag on p.pedido_id = pag.pedido_id
where pag.valor_pago is null;

-- 8;
select
c.nome, p.pedido_id,sum(i.quantidade * preco_unitario) as TotalGasto
from clientes c
join pedidos p 
on c.cliente_id = p.cliente_id
join itens_pedido i on p.pedido_id = i.pedido_id
group by c.nome;

-- 9;
SELECT p.produto_id, p.nome, sum(i.quantidade) as quantidades_Vendidas
from produtos p
join itens_pedido i on p.produto_id = i.produto_id
group by i.produto_id, p.nome
order by quantidades_Vendidas desc
limit 5;

-- 10;
select c.cliente_id, c.nome, p.pedido_id
from clientes c
left join pedidos p on c.cliente_id = p.cliente_id
where p.pedido_id is null
order by c.nome;

-- 11;
select sum(pag.valor_pago) as Faturamento_Total
from pagamentos pag;

-- 12;
select avg(pag.valor_pago) as valor_medio_pago
from pagamentos pag;

-- 13;
select c.cliente_id,  c.nome,
count(p.pedido_id) as numero_total_pedidos 
from clientes c 
inner join pedidos p on c.cliente_id = p.cliente_id
 group by c.cliente_id, c.nome 
order by p.pedido_id desc;

-- 14;
select p.pedido_id, e.endereco, e.status
from pedidos p 
inner join entregas e on p.pedido_id = e.pedido_id;
 
SELECT 
    e.status,
    COUNT(e.pedido_id) AS quantidade_pedidos
FROM entregas e
GROUP BY e.status
ORDER BY quantidade_pedidos DESC;

-- 15;
select c.cliente_id, c.nome, p.pedido_id, max(pag.valor_pago) as Maior_ValorPago
from clientes c 
join pedidos p on c.cliente_id = p.cliente_id
join pagamentos pag on p.pedido_id = pag.pedido_id
group by c.cliente_id, c.nome
order by Maior_ValorPago desc
limit 1;

select * from pagamentos;
