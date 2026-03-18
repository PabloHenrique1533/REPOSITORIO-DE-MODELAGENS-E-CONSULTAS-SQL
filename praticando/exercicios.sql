use dbpraticando;


-- consultas basicas
-- 1
select livros.nome as Nome_Do_Livro,
generos.nome as Nome_Genero,
livros.data_de_recebimento as DT_Recebimento
from livros
join generos on livros.genero_id = generos.genero_id
where livros.data_de_recebimento >= '2024-07-01';

-- 2
select nome, preco 
from livros
where preco > 40.00
order by preco desc;

-- 3
select livros.nome as Nome_Livro,
generos.nome as Nome_Genero
from livros
join generos on livros.genero_id = generos.genero_id
where generos.nome = 'Biografia';

-- funções agregadas

-- 4 
SELECT generos.nome AS Nome_do_Genero, 
       COUNT(*) AS Quantidade_de_Livros
FROM livros
JOIN generos ON livros.genero_id = generos.genero_id
GROUP BY generos.nome 
union all 
select 'Total dos Livros',
count(livros.nome)
from livros;

-- 5
select generos.nome as Nome_Genero,
avg(livros.preco) as media_Preço
from livros
join generos on livros.genero_id = generos.genero_id
group by generos.nome 
union all 
select 'MEDIA total',
avg(livros.preco)
from livros;

-- 6
select generos.nome as Nome_Genero,
count(livros.nome) as total_estoque
from livros
join generos on livros.genero_id = generos.genero_id
group by generos.nome 
union all 
select 'valor total do preço em estoque',
sum(livros.preco) 
from livros;
--
SELECT generos.nome AS Nome_Genero,
       SUM(livros.preco) AS ValorTotal
FROM livros
JOIN generos ON livros.genero_id = generos.genero_id
GROUP BY generos.nome;
--

-- 7 
select generos.nome as Nome_Genero,
count(livros.nome) as total_estoque
from livros
join generos on livros.genero_id = generos.genero_id
group by generos.nome
having count(*) > 1;

-- atualização e exclusão

-- 8 
delete from livros where livro_id = 25;
-- 9
update livros set preco = 25.00 where livro_id = 23;
select * from livros;

-- subquery + agrupamento

-- 10 
SELECT generos.nome AS NomeGenero,
       AVG(livros.preco) AS MediaPreco
FROM livros
JOIN generos ON livros.genero_id = generos.genero_id
GROUP BY generos.nome
HAVING AVG(livros.preco) > 40;


--

