CREATE DATABASE DBPRATICANDO;
USE DBPRATICANDO;

CREATE TABLE pacientes (
    PACIENTEID INT AUTO_INCREMENT,
    NOME VARCHAR(100),
    CPF VARCHAR(14),
    DATA_DE_NASCIMENTO DATE,
    EMAIL VARCHAR(100),
    ENDERECO VARCHAR(150),
    PRIMARY KEY (PACIENTEID)
);

-- parte 4 relação
create table Consultas(
consultasID int auto_increment,
pacienteid_FK int,
data_da_consulta date,
observações varchar(140),
PRIMARY KEY (consultasID),
foreign key (pacienteid_FK) references pacientes (pacienteid)
);

create table medicos(
medicoid int auto_increment,
nome varchar(140),
especialidade varchar(140),
primary key (medicoid)
);

alter table consultas
add column medicoid_fk int;

alter table consultas
add constraint fk_medico
foreign key (medicoid_fk) references medicos(medicoid);


INSERT INTO medicos (nome, especialidade) VALUES
('Dr. Carlos Souza', 'Cardiologia'),
('Dra. Marina Alves', 'Pediatria'),
('Dr. João Pereira', 'Ortopedia');


INSERT INTO consultas (PACIENTEID_FK, DATA_DA_CONSULTA, OBSERVAçõES) VALUES
(3, '2025-06-01', 'Retorno de exame de sangue.'),
(4, '2025-06-10', 'Consulta de rotina.'),
(5, '2025-07-05', 'Dor de cabeça e tontura.'),
(6, '2025-07-12', 'Pós-operatório.'),
(7, '2025-07-20', 'Check-up anual.');

INSERT INTO pacientes(NOME, CPF, DATA_DE_NASCIMENTO, EMAIL, ENDERECO) 
VALUES ('Gabriel', '48450352156', '2005-06-04', 'gabriel@gmail.com', 'rua goias 83'),
('Ana Silva', '12345678901', '1985-10-12', 'ana.silva@email.com', 'Rua das Flores, 100'),
('Bruno Costa', '23456789012', '1992-07-05', 'bruno.costa@email.com', 'Avenida Brasil, 456'),
('Carla Mendes', '34567890123', '2001-02-20', 'carla.mendes@email.com', 'Travessa Azul, 78'),
('Daniel Oliveira', '45678901234', '1978-11-30', 'daniel.oliveira@email.com', 'Praça Central, 23'),
('Elisa Pereira', '56789012345', '1999-06-15', 'elisa.pereira@email.com', 'Alameda Verde, 12');

----------------------------------------------------------------
select nome, data_de_nascimento from pacientes
where data_de_nascimento > '2000-01-01'; -- filtrando dados 

select nome, email from pacientes
order by nome ; -- ordenando resultados

select count(*) from pacientes;
---------------------------------------------------------------------
-- Parte 1 - consultas com where
select nome , endereco
from pacientes
where Nome like 'C%';

select nome, data_de_nascimento from pacientes
where data_de_nascimento < '1990-01-01';

select nome, email from pacientes
where email like '%gmail%';
----------------------------------
-- Parte 2 ordenação com order by
select nome, email from pacientes
order by nome desc;

select nome, data_de_nascimento from pacientes
order by data_de_nascimento desc;
-----------------------------------
-- parte 3 funções agregadas
select count(*) as totaldepacientes
from PACIENTES	;

select min(data_de_nascimento) as paciente_maisVelho
from pacientes;

select max(data_de_nascimento) as paciente_maisNovo
from pacientes;
-------------------------------------------------
-- parte5 joins 
SELECT 
  pacientes.nome,
  consultas.data_da_consulta,
  consultas.observações
FROM consultas
INNER JOIN pacientes
  ON consultas.pacienteid_fk = pacientes.pacienteid;
  
  select
  pacientes.nome,
  pacientes.email,
  consultas.data_da_consulta
  from consultas
  inner join pacientes
  on consultas.pacienteid_fk = pacientes.pacienteid;

SELECT
  pacientes.nome,
  consultas.data_da_consulta,
  consultas.observações
FROM pacientes
left JOIN consultas
  ON pacientes.pacienteid = consultas.pacienteid_fk;
 ----------------------------------------------------- 
UPDATE pacientes
SET email = 'ana.silva@outlook.com'
WHERE pacienteid = 3;

DELETE FROM pacientes
WHERE pacienteid = 6;

DELETE FROM consultas
WHERE pacienteid_FK = 6;

select * from pacientes;


