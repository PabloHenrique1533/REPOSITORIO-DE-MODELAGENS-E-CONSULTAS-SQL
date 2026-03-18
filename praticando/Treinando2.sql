create database lojasonline;
use lojasonline;

create table  cliente(
idCliente int auto_increment Primary Key,
nome varchar(100),
email varchar(100),
telefone varchar(100),
cidade varchar(100));

create Table Produto(
IdProduto int auto_increment Primary Key,
nome varchar(100),
categoria varchar(100),
preco decimal(10,2) not null,
estoque int default 0);

create table pedido(
idPedido int auto_increment primary key,
idcliente int,
datePedido date not null,
status varchar(20) default 'pedente',
Foreign key (idcliente) references cliente(idCliente));

create table ItemPedido(
IdItem int auto_increment primary key,
idPedido int,
IdProduto int,
quantidade int not null,
precoUnitario decimal(10,2) not null,
foreign key (idPedido) references pedido(idPedido),
foreign key (IdProduto) references Produto(IdProduto));

INSERT INTO Cliente (nome, email, telefone, cidade) VALUES
('João Silva', 'joao@email.com', '119999999', 'São Paulo'),
('Maria Souza', 'maria@email.com', '219888888', 'Rio de Janeiro'),
('Carlos Lima', 'carlos@email.com', '319777777', 'Belo Horizonte');

-- Produtos
INSERT INTO Produto (nome, categoria, preco, estoque) VALUES
('Notebook Dell', 'Eletrônicos', 3500.00, 10),
('Smartphone Samsung', 'Eletrônicos', 2500.00, 20),
('Camisa Polo', 'Vestuário', 120.00, 50),
('Cadeira Gamer', 'Móveis', 900.00, 15);

-- Pedidos
INSERT INTO Pedido (idCliente, datePedido, status) VALUES
(1, '2025-09-01', 'Concluído'),
(2, '2025-09-05', 'Pendente'),
(1, '2025-09-10', 'Concluído');

-- Itens do pedido
INSERT INTO ItemPedido (idPedido, idProduto, quantidade, precoUnitario) VALUES
(1, 1, 1, 3500.00),   -- João comprou 1 Notebook
(1, 3, 2, 120.00),    -- João comprou 2 Camisas
(2, 2, 1, 2500.00),   -- Maria comprou 1 Smartphone
(3, 4, 1, 900.00);    -- João comprou 1 Cadeira Gamer

-- NIVEL1

-- Listando Todos os Clientes;
select * from cliente;

-- Mostrando apenas nomes e cidades do clientes;
select nome, cidade from cliente;

-- listando todos os produtos da categoria eletronica;
select nome, categoria from Produto
where categoria = 'Eletrônicos';

-- listando os pedido realizados no mes de setembro
select idPedido, datePedido from Pedido
where datePedido >= '2025-09-01' and '2025-09-30';

-- listando os nome e produtos maiores q 10;
select nome, preco from Produto
where estoque > 10;


-- NIVEL 2;

-- Listando Nome Cliente e Data De Pedido (join);
select cliente.nome, pedido.datePedido 
from cliente 
join pedido on (cliente.idCliente=pedido.idCliente);

-- mostrando todos produtos do pedido 1;
select  produto.nome, ItemPedido.precoUnitario, itemPedido.quantidade
from ItemPedido
join produto on (produto.idProduto=itemPedido.idProduto)
where IdPedido = 1;

-- listando pedidos do joao;
select c.nome, p.IdCliente, 
p.datePedido, p.status
from cliente c
inner join Pedido p on c.idcliente = p.idcliente
where c.nome = 'João Silva';

-- calcular o valor total de cada pedido;
select p.idpedido, sum(i.quantidade) as TotalQuantidade, 
sum(i.quantidade * i.precoUnitario) as TotalPedido
from pedido p
inner join itemPedido i on p.idpedido = i.idpedido
group by p.idpedido;

-- exibir soma total das vendas;
SELECT SUM(i.quantidade * i.precoUnitario) AS ValorTotalVendas
FROM Pedido p
JOIN ItemPedido i ON p.idPedido = i.idPedido
WHERE p.status = 'Concluído';

-- NIVEL 3;
select c.nome, p.idPedido,
i.quantidade , count(distinct i.idProduto)
from cliente c 
inner join pedido p on c.idcliente = p.idcliente
inner join itemPedido i on i.idPedido = p.idPedido
group by c.nome
having count(distinct i.idproduto) > 1;

SELECT categoria, AVG(preco) AS PrecoMedio
FROM Produto
GROUP BY categoria;






