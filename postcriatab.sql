drop table if exists fornecimento cascade;
drop table if exists peca cascade;
drop table if exists fornecedor cascade;
drop table if exists projeto cascade;

create table Peca
(cod_peca numeric(4) not null,
pnome varchar(15),
cor varchar(15),
peso decimal(6,2),
cdade varchar(20),
constraint pk_peca primary key (cod_peca));

create table Fornecedor
(cod_fornec numeric(4),
fnome varchar(15),
status numeric(4),
cidade varchar(20));

alter table Fornecedor add constraint pk_fornec primary key (cod_fornec);

create table Projeto (
cod_proj numeric(4),
jnome varchar(20),
cidade varchar(20),
constraint pk_proj primary key (cod_proj));

create table Fornecimento (
codigo serial NOT NULL PRIMARY KEY,
cod_fornec  numeric(4),
cod_peca  numeric(4),
cod_proj  numeric(4),
quantidade numeric(4),
valor numeric(10,2),
constraint fk_forneci foreign key (cod_fornec) references Fornecedor (cod_fornec),
constraint fk_pecai foreign key (cod_peca) references Peca (cod_peca) ,
constraint fk_proji foreign key (cod_proj) references Projeto (cod_proj));

insert into Peca values (1,'NULT','VERMELHO', 12, 'LONDRES');
insert into Peca values (2,'BOLT','VERDE', 17, 'PARIS');
insert into Peca values (3,'SCREW','AZUL', 17, 'ROMA');
insert into Peca values (4,'SCREW','VERMELHO', 14, 'LONDRES');
insert into Peca values (5,'CAM','AZUL', 12, 'PARIS');
insert into Peca values (6,'COG','VERMELHO', 19, 'LONDRES');

INSERT INTO FORNECEDOR VALUES (1, 'SMITH',20, 'LONDRES');
INSERT INTO FORNECEDOR VALUES (2, 'JONES',10, 'PARIS');
INSERT INTO FORNECEDOR VALUES (3, 'BLAKE',30, 'PARIS');
INSERT INTO FORNECEDOR VALUES (4, 'CLARK',20, 'ATENAS');
INSERT INTO FORNECEDOR VALUES (5, 'ADAMS',30, 'ATENAS');

INSERT INTO PROJETO VALUES (1,'SORTER', 'PARIS');
INSERT INTO PROJETO VALUES (2,'PUNCH', 'ROMA');
INSERT INTO PROJETO VALUES (3,'READER', 'ATENAS');
INSERT INTO PROJETO VALUES (4,'CONSOLE', 'ATENAS');
INSERT INTO PROJETO VALUES (5,'COLLATOR', 'LONDRES');
INSERT INTO PROJETO VALUES (6,'TERMINAL', 'OSLO');
INSERT INTO PROJETO VALUES (7,'TAPE', 'LONDRES');


ALTER TABLE FORNECIMENTO ADD DATAF DATE;
UPDATE FORNECIMENTO SET DATAF = current_date;
UPDATE FORNECIMENTO SET DATAF = '10/10/2022' WHERE COD_PECA = 1;
INSERT INTO FORNECIMENTO VALUES (default, 1,1,1,200,1000);
INSERT INTO FORNECIMENTO VALUES (default, 1,1,4,700,5000);
INSERT INTO FORNECIMENTO VALUES (default, 2,3,1,400,2000);
INSERT INTO FORNECIMENTO VALUES (default, 2,3,2,200,1000);
INSERT INTO FORNECIMENTO VALUES (default, 2,3,3,200,1000);
INSERT INTO FORNECIMENTO VALUES (default, 2,3,4,500,3000);
INSERT INTO FORNECIMENTO VALUES (default, 2,3,5,600,4000);
INSERT INTO FORNECIMENTO VALUES (default, 2,3,6,400,2000);
INSERT INTO FORNECIMENTO VALUES (default, 2,3,7,800,8000);
INSERT INTO FORNECIMENTO VALUES (default, 2,5,2,100,500);
INSERT INTO FORNECIMENTO VALUES (default, 3,3,1,200,1200);
INSERT INTO FORNECIMENTO VALUES (default, 3,4,2,500,900);
INSERT INTO FORNECIMENTO VALUES (default, 4,1,4,100,1000);
INSERT INTO FORNECIMENTO VALUES (default, 4,6,3,300,2000);
INSERT INTO FORNECIMENTO VALUES (default, 4,6,7,300,2000);
INSERT INTO FORNECIMENTO VALUES (default, 5,2,2,200,1200);
INSERT INTO FORNECIMENTO VALUES (default, 5,2,4,100,900);
INSERT INTO FORNECIMENTO VALUES (default, 5,3,4,200,1000);
INSERT INTO FORNECIMENTO VALUES (default, 5,4,4,800,7000);
INSERT INTO FORNECIMENTO VALUES (default, 5,5,4,400,5000);
INSERT INTO FORNECIMENTO VALUES (default, 5,5,5,500,6000);
INSERT INTO FORNECIMENTO VALUES (default, 5,5,7,100,1000);
INSERT INTO FORNECIMENTO VALUES (default, 5,6,2,200,1200);
INSERT INTO FORNECIMENTO VALUES (default, 5,6,4,500,3000);
UPDATE FORNECIMENTO SET DATAF = '30/10/2020' WHERE COD_FORNEC = 5;
UPDATE FORNECIMENTO SET DATAF = '05/05/2021' WHERE COD_PROJ = 4;