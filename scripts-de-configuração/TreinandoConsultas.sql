use dbpraticando;


create table generos(
genero_id int auto_increment,
nome varchar(100),
PRIMARY KEY (genero_id) 
);


create table livros (
livro_id int auto_increment,
genero_id int,
nome varchar(100),
preco decimal (10,2),
data_de_recebimento date,
PRIMARY KEY (livro_id),
FOREIGN KEY (genero_id) references generos (genero_id)
);

insert into generos (nome) 
values ('Romance'), 
('Ficção Cientifica'), 
('Suspense'), 
('Fantasia'), 
('Não Ficção');

insert into livros (genero_id, nome, preco, data_de_recebimento) 
values (1,'Amor nas Estrelas', 29.90, '2024-01-15'),
(3, 'Misterio na Floresta', 34.50, '2024-02-10'),
(2, 'Viagem ao Espaço', 45.00, '2024-03-05'),
(4, 'Reinos Perdido', 39.99, '2024-04-20'),
(5, 'Historia do Brasil', 50.00, '2024-05-01');


-- selcet onde mostra o nome do livro e do generos;
select livros.nome as Nome_do_Livro, 
generos.nome as Nome_do_Genero
from livros
join generos on livros.genero_id = generos.genero_id;

-- select onde mostra o nome e generos acima de 40$;
select livros.nome as Nome_do_Livro,
generos.nome as Nome_do_Genero
from livros
join generos on livros.genero_id = generos.genero_id
where preco > 40;

-- select onde mostra a mesma coisa do de cima so que com os preços mostrando;
select livros.nome as Nome_do_Livro,
generos.nome as Nome_do_Genero, livros.preco
from livros
join generos on livros.genero_id = generos.genero_id
where preco > 40;

-- ordenando com filtro os livros acima de 40 em ordem desc;
select livros.nome, livros.preco
from livros
where preco > 40
order by preco desc;

-- msm coisa do de cima so que agora com o gneros;
select livros.nome, livros.preco, generos.nome
from livros
join generos on livros.genero_id = generos.genero_id
where preco > 40
order by preco desc;

-- mostrando o nome do livro e generos e filtrando para mostra so de uma data adiante com ordenação crescente;
select livros.nome as Nome_do_Livro, 
generos.nome as Nome_do_genero, 
livros.data_de_recebimento
from livros
join generos on livros.genero_id = generos.genero_id
where data_de_recebimento > '2024-03-01'
order by data_de_recebimento asc;

-- filtrando pelo nome do generos;
select livros.nome as Nome_do_Livro, 
generos.nome as Nome_do_genero
from livros
join generos on livros.genero_id = generos.genero_id
where generos.nome = 'Fantasia';

-- msm coisa, so muda a busca que não diferencia as maiusculas e minusculas;
select livros.nome as Nome_do_Livro, 
generos.nome as Nome_do_genero
from livros
join generos on livros.genero_id = generos.genero_id
where lower(generos.nome)  = 'fantasia';

-- retorna com filtra apensa frase com certa palavra;
select livros.nome as Nome_do_Livro, 
generos.nome as Nome_do_genero
from livros
join generos on livros.genero_id = generos.genero_id
where lower(generos.nome) like '%ficção%';

-- filtrando os preços entre um valor a outro;
select livros.nome as Nome_do_Livro, 
generos.nome as Nome_do_genero,
livros.preco as Preço_do_Livro
from livros
join generos on livros.genero_id = generos.genero_id
where preco between 30.00 and 46.00;

-- usando o count para saber quantos livros tem por genero;
select generos.nome as Nome_do_Genero,
count(*) as Quantidade_de_Livros
from livros
join generos on livros.genero_id = generos.genero_id
group by generos.nome;

-- aqui estou filtrando apos um agrupamento
SELECT generos.nome AS Nome_do_Genero, 
       COUNT(*) AS Quantidade_de_Livros
FROM livros
JOIN generos ON livros.genero_id = generos.genero_id
GROUP BY generos.nome
HAVING COUNT(*) >= 1;

-- aqui mostrando apenas um livro cadastrado
SELECT generos.nome AS Nome_do_Genero, 
       COUNT(*) AS Quantidade_de_Livros
FROM livros
JOIN generos ON livros.genero_id = generos.genero_id
GROUP BY generos.nome
HAVING COUNT(*) = 1;


-- subconsulta usando o where in ;
SELECT livros.nome AS Nome_do_Livro, 
       generos.nome AS Nome_do_Genero, 
       livros.preco AS Preço_do_Livro,
       livros.data_de_recebimento
FROM livros
JOIN generos ON livros.genero_id = generos.genero_id
WHERE livros.preco BETWEEN 30.00 AND 50.00
  AND livros.data_de_recebimento < '2024-04-01'
  AND livros.genero_id IN (
      SELECT genero_id
      FROM livros
      GROUP BY genero_id
      HAVING COUNT(*) >= 1
  )
ORDER BY livros.preco DESC;


-- subconsulta usando join;
SELECT livros.nome AS Nome_do_Livro, 
       generos.nome AS Nome_do_Genero, 
       livros.preco AS Preço_do_Livro,
       livros.data_de_recebimento
FROM livros
JOIN generos ON livros.genero_id = generos.genero_id
JOIN (
    SELECT genero_id, COUNT(*) AS qtd_livros
    FROM livros
    GROUP BY genero_id
) AS contagem ON livros.genero_id = contagem.genero_id
WHERE livros.preco BETWEEN 30.00 AND 50.00
  AND livros.data_de_recebimento < '2024-04-01'
  AND contagem.qtd_livros > 1
ORDER BY livros.preco DESC;















