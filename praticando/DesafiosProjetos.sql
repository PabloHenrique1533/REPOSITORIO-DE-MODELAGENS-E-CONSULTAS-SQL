create database projetos;
use projetos;

create table cliente (
idCLiente int auto_increment primary key,
nome varchar(100),
email varchar(100),
telefone varchar(100));

create table produtos (
idProduto int auto_increment primary key,
nome varchar(100),
preco decimal(10,2),
estoque int);

create table pedidos (
idPedido int auto_increment primary key,
idCliente int,
data_pedido date,
foreign key (idCliente) references cliente(idCliente));

create table itens_pedido (
idItem int auto_increment primary key,
idPedido int,
idProduto int,
quantidade int,
preco_unitario decimal(10,2),
foreign key (idPedido) references pedidos(idPedido),
foreign key (idProduto) references Produtos(idProduto));

-- INSERÇÃO DE DADOS
Insert Into cliente (nome, email, telefone) values
('Ana Souza', 'ana.souza@email.com', '11999999999'),
('Carlos Lima', 'carlos.lima@email.com', '21988887777'),
('Mariana Alves', 'mariana.alves@email.com', '31977776666'),
('João Pedro', 'joao.pedro@email.com', '11966665555'),
('Fernanda Costa', 'fernanda.costa@email.com', '41955554444');

Insert Into Produtos (nome, preco, estoque) Values
('Notebook Dell Inspiron', 3500.00, 10),
('Mouse Logitech', 120.00, 50),
('Teclado Mecânico Redragon', 250.00, 30),
('Monitor LG 24"', 900.00, 20),
('Headset HyperX', 400.00, 25),
('Cadeira Gamer', 1200.00, 15);

Insert Into Pedidos (idCliente, data_pedido) Values
(1, '2025-10-01'),
(2, '2025-10-02'),
(3, '2025-10-03'),
(1, '2025-10-04'),
(4, '2025-10-05'); 

Insert Into itens_Pedido (idPedido, IdProduto, Quantidade, preco_unitario) Values
-- Pedido 1 - Ana
(1, 1, 1, 3500.00),
(1, 2, 1, 120.00),

-- Pedido 2 - Carlos
(2, 4, 1, 900.00),
(2, 5, 1, 400.00),

-- Pedido 3 - Mariana
(3, 2, 2, 120.00),
(3, 3, 1, 250.00),

-- Pedido 4 - Ana novamente
(4, 6, 1, 1200.00),

-- Pedido 5 - João
(5, 1, 1, 3500.00),
(5, 5, 1, 400.00);

-- Desafio 1 -- Consultas Basicas;
select c.nome, p.data_pedido as Datas_Dos_Pedidos
from cliente c 
join Pedidos p on c.idCliente = p.idCliente;

-- Desafio 2;
select c.nome as CLientes, 
pr.nome as Produtos, 
i.quantidade as Quantidade_Vendida,
 (i.quantidade * i.preco_unitario) AS Total_Item
from cliente c 
join pedidos p on c.idCliente = p.idCliente
join itens_Pedido i on p.idpedido = i.idPedido
join produtos pr on pr.idProduto = i.idProduto
order by c.nome;

-- desafio 3;
select 
c.idCliente as Id_do_Cliente,
c.nome as CLientes,
sum(i.quantidade) as Total_de_Produtos_Comprados_Pelo_CLiente,
sum(i.quantidade * i.preco_unitario) as TotalGasto
from cliente c 
join pedidos p on c.idcliente = p.idcliente
join itens_pedido i on p.idpedido = i.idpedido
group by c.nome
order by c.nome;

-- desafio 4;
select
pr.idProduto as Ids_Produtos,
pr.nome as Produtos,
sum(i.quantidade) as Total_Vendido,
sum(i.quantidade * i.preco_unitario) as TotalGasto
from produtos pr
join itens_Pedido i on pr.idProduto = i.idProduto
group by pr.nome
order by TotalGasto desc;

-- desafio 5;
select 
c.idCliente,
c.nome as Clientes,
p.data_pedido as Data_Do_Pedido,
sum(i.quantidade * preco_unitario) as Total_Gasto
from cliente c
join pedidos p on c.idcliente = p.idcliente
join itens_Pedido i on p.idpedido = i.idpedido
group by c.idcliente, c.nome, year(p.data_pedido), month(p.data_pedido)
order by total_gasto desc;

-- Desafio 6;
select 
pr.idProduto as Ids_Produtos,
DATE_FORMAT(p.data_pedido, '%Y-%m') as Mes_Ano,
pr.nome as Produtos,
sum(i.quantidade) as Total_Vendida,
sum(i.quantidade * i.preco_unitario) as Faturamento_Do_Produto
from produtos pr
join itens_pedido i on pr.idProduto = i.idProduto
join pedidos p on p.idPedido = i.idPedido
GROUP BY YEAR(p.data_pedido), MONTH(p.data_pedido), pr.idProduto, pr.nome
order by mes_ano, Total_Vendida desc;

-- desafio 7;
SELECT
  pr.idProduto,
  pr.nome AS Produto,
  c.nome AS Cliente,
  SUM(i.quantidade) AS Total_Comprado,
  SUM(i.quantidade * i.preco_unitario) AS Total_Faturado
FROM produtos pr
JOIN itens_pedido i   ON pr.idProduto = i.idProduto
JOIN pedidos p        ON p.idPedido   = i.idPedido
JOIN cliente c        ON c.idCliente  = p.idCliente
GROUP BY pr.idProduto, pr.nome, c.idCliente, c.nome
HAVING SUM(i.quantidade) >= ALL (
  SELECT SUM(i2.quantidade)
  FROM itens_pedido i2
  JOIN pedidos p2 ON i2.idPedido = p2.idPedido
  WHERE i2.idProduto = pr.idProduto
  GROUP BY p2.idCliente
)
ORDER BY pr.nome;

-- desafio 8;
select 
	Mes_ano,
    max(faturamento_total) as Maior_Faturamento
from (
		select 
		p.idpedido as id_DO_PEDIDO,
		DATE_FORMAT(p.data_pedido, '%Y-%m') as Mes_Ano,
		pr.nome as Produto,
		sum(i.quantidade * i.preco_unitario) as Faturamento_total
		from pedidos p
		join itens_pedido i on p.idpedido = i.idpedido
		join produtos pr on pr.idProduto = i.idproduto
		group by year(p.data_pedido), month(p.data_pedido), pr.nome
) as Resumo
group by Mes_ano 
order by mes_ano asc;


-- Subquery com faturamento por produto e mês
SELECT r.Mes_Ano, r.Produto, r.Faturamento_Total
FROM (
    SELECT 
        DATE_FORMAT(p.data_pedido, '%Y-%m') AS Mes_Ano,
        pr.nome AS Produto,
        SUM(i.quantidade * i.preco_unitario) AS Faturamento_Total
    FROM pedidos p
    JOIN itens_pedido i ON p.idpedido = i.idpedido
    JOIN produtos pr ON pr.idProduto = i.idProduto
    GROUP BY YEAR(p.data_pedido), MONTH(p.data_pedido), pr.nome
) AS r
JOIN (
    -- Subquery que pega o maior faturamento de cada mês
    SELECT Mes_Ano, MAX(Faturamento_Total) AS Maior_Faturamento
    FROM (
        SELECT 
            DATE_FORMAT(p.data_pedido, '%Y-%m') AS Mes_Ano,
            pr.nome AS Produto,
            SUM(i.quantidade * i.preco_unitario) AS Faturamento_Total
        FROM pedidos p
        JOIN itens_pedido i ON p.idpedido = i.idpedido
        JOIN produtos pr ON pr.idProduto = i.idProduto
        GROUP BY YEAR(p.data_pedido), MONTH(p.data_pedido), pr.nome
    ) AS temp
    GROUP BY Mes_Ano
) AS m
ON r.Mes_Ano = m.Mes_Ano AND r.Faturamento_Total = m.Maior_Faturamento
ORDER BY r.Mes_Ano;







