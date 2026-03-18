-- Desafio: Funções agregadas e agrupamento
select livros.nome as NomeLivro,
generos.nome as NomeGenero,
count(*) as Quantidade_de_Livro
from livros
join generos on livros.genero_id = generos.genero_id
group by livros.nome;

-- desafio 2 (subquery)
select generos.nome as NomeGenero,
	   SUM(livros.preco) as Preço
from livros
join generos on generos.genero_id = livros.genero_id
group by generos.nome 
union all 
select 'total',
sum(Preco) as PreçoTotal
from livros;

-- desafio 2 (com with rollup)
select generos.nome as NomeGenero,
	   sum(livros.preco) as PreçoLivro
from generos
join livros on generos.genero_id = livros.genero_id
group by generos.nome with rollup;

-- desafio 3 (with rollup)
select generos.nome as NomeGenero,
	   avg(livros.preco) as Preço
from livros
join generos on generos.genero_id = livros.genero_id
group by generos.nome with rollup;

-- desafio 3 ( com subqueRY)
select generos.nome as NomeGenero,
	   avg(livros.preco) as Preço
from livros
join generos on generos.genero_id = livros.genero_id
group by generos.nome
union all
select 'media total',
 avg(preco) as MediaTotal
from livros;

-- desafio 4
select 
generos.nome as GeneroNome,
min(livros.preco) as PrecoMIN, max(livros.preco) as PrecoMax
from livros
join generos on livros.genero_id = generos.genero_id
group by generos.nome;

-- desafio 5
select generos.nome as NomeGenero,
livros.nome as NomeLivro
from livros
join generos on livros.genero_id = generos.genero_id
group by generos.nome
having count(generos.nome)> 1;
