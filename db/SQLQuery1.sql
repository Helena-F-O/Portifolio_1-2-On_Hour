CREATE DATABASE onhour1;

USE onhour1;

CREATE TABLE usuarios(
    cpf NUMERIC(15, 0) NOT NULL PRIMARY KEY, 
    usuario VARCHAR(45) NOT NULL, 
    email VARCHAR(45) NOT NULL, 
    senha VARCHAR(100) NOT NULL, 
    horas_exigidas FLOAT NOT NULL
);

CREATE TABLE categorias(
    id_categoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    categoria VARCHAR(45) NOT NULL, 
    horas_maximas FLOAT NOT NULL
);

CREATE TABLE certificados(
    id_certificado INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    certificado VARCHAR(45) NOT NULL,
    horas FLOAT NOT NULL,
    data_emissao DATE NOT NULL,
    categoria_id INT NOT NULL,
    usuario_cpf NUMERIC(15, 0) NOT NULL,
    CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES categorias (id_categoria),
    CONSTRAINT fk_usuario_cpf FOREIGN KEY (usuario_cpf) REFERENCES usuarios (cpf)
);

INSERT INTO usuarios(cpf, usuario, email, senha, horas_exigidas)
VALUES (12345678900, 'helena', 'helena@gmail.com', '1234', 234), (98765432100, 'antonio', 'antonio@gmail.com', '1234', 200);

INSERT INTO categorias(id_categoria, categoria, horas_maximas)
VALUES 
(1, 'Disciplinas Isoladas', 60),
(2, 'Participação Conferencias', 60),
(3, 'Participação como Ouvinte de Defesa', 15),
(4, 'Disciplinas de Programas de Extensao', 30),
(5, 'Cursos e Atividades de Extensao', 60),
(6, 'Visitas Tecnicas e Viagens de Estudo', 20),
(7, 'Viagens de Intercambio', 90),
(8, 'Exercicio de Monitoria', 30),
(9, 'Participacao em Pesquisas Institucionais', 30),
(10, 'Participacao em Iniciacao Cientifica', 40),
(11, 'Projetos Sociais e Comunitarios', 40),
(12, 'Artigos Cientificos Publicados da Area', 60),
(13, 'Apresentacao de Pesquisa em Evento Cientifico', 60),
(14, 'Participacao em Concursos de Monografias', 60),
(15, 'Representante de Turma ou Estudantil', 10),
(16, 'Mesario de Eleicoes e Desfiles Civicos', 15);

INSERT INTO certificados(id_certificado, certificado, horas, data_emissao, categoria_id, usuario_cpf)
VALUES 
(1, 'Curso Udemy', 25, '2024-07-30', 5, 12345678900),
(2, 'Disciplinas Isoladas', 25, '2024-07-30', 5, 12345678900),
(3, 'Viagem Intercambio', 25, '2024-07-30', 5, 12345678900),
(4, 'Monitoria', 25, '2024-07-30', 5, 12345678900),
(5, 'Ouvinte Defesa', 25, '2024-07-30', 5, 12345678900);


select * from usuarios;

select * from certificados;

select * from categorias;