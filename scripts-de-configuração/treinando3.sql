use lojasonline;

-- ex1;
select c.nome as Nome_Cliente,
p.idpedido as Pedidos, p.datePedido as Data_Pedido
from cliente c
left join pedido p on c.idcliente = p.idcliente;

-- ex2 errado;
select pr.nome as Produtos, p.status, count(distinct i.idPedido)
from produto pr
inner join pedido p on pr.idProduto=p.idpedido 
inner join itempedido i on i.idPedido=p.idpedido;

-- ex2 corrigido;
SELECT 
    pr.nome AS Produto,
    p.status,
    COUNT(DISTINCT i.idPedido) AS TotalPedidos
FROM Produto pr
INNER JOIN ItemPedido i 
    ON pr.idProduto = i.idProduto
INNER JOIN Pedido p 
    ON i.idPedido = p.idPedido
GROUP BY pr.nome, p.status;

-- ex3;
select pr.nome as Produto,
coalesce(sum(i.quantidade), 0) as QuantidadeVendida -- COALESCE(..., 0) → substitui NULL por 0, caso o produto não tenha sido vendido.
from Produto pr
left join ItemPedido i on pr.idProduto = i.idProduto
group by pr.idProduto, pr.Nome;

-- ex4;
select c.nome as NomeCliente,
count(distinct p.idpedido) as PedidoCliente,
sum(i.quantidade) as Total
from cliente c
left join pedido p on c.idcliente = p.idcliente
left join itemPedido i on p.idpedido = i.idpedido
group by c.idCliente, c.nome;

-- ex5;
select pr.nome as Produtos,
count(distinct i.idPedido) as Num_Pedidos
from produto pr
left join itemPedido i on pr.idProduto = i.idProduto
group by pr.nome, i.idPedido; 

-- ex6;
select c.nome as Nome_Cliente,
sum(i.precoUnitario * i.quantidade) as ValorTotal
from cliente c
left join pedido p on c.idcliente = p.idcliente
left join itemPedido i on p.idpedido = i.idPedido
group by c.nome, c.idCliente;

-- ex7;
select p.idPedido as Pedidos,sum( i.quantidade) as Quantidade_Produtos,
sum(i.quantidade * i.precounitario) as ValorTotal
from pedido p
left join itemPedido i on p.idPedido = i.idPedido
group by p.idPedido


