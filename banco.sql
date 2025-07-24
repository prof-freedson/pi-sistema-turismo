-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS encantos_db;
USE encantos_db;

-- add Tabela Endereço
CREATE TABLE endereco (
    id_end INT AUTO_INCREMENT PRIMARY KEY,
    rua VARCHAR(100),
    numero VARCHAR(10),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    estado CHAR(2)
);

-- add Tabela Telefone
CREATE TABLE telefone (
	id_tel INT AUTO_INCREMENT PRIMARY KEY,
    fone_1 VARCHAR(20),
    fone_2 VARCHAR(20)
);

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'comum') DEFAULT 'comum',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de categorias (para eventos e restaurantes)

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT
);

-- Tabela de eventos

CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    categoria_id INT,
    data_inicio DATE,
    data_fim DATE,
    horario TIME,
    local VARCHAR(255),
    id_end INT,
    preco DECIMAL(10,2),
    capacidade INT,
    organizador VARCHAR(255),
    contato VARCHAR(100),
    imagem TEXT,
    criado_por INT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (criado_por) REFERENCES usuarios(id),
    FOREIGN KEY (id_end) REFERENCES endereco(id_end)
);

-- Tabela de restaurantes
CREATE TABLE restaurantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    tipo_cozinha ENUM('Brasileira','Maranhense','Italiana','Japonesa','Mexicana','Francesa') NOT NULL,
    id_end INT,
    id_tel INT,
    horario_funcionamento VARCHAR(100),
    faixa_preco ENUM('R$', 'R$$', 'R$$$', 'R$$$$'),
    capacidade INT,
    avaliacao INT CHECK (avaliacao BETWEEN 1 AND 5),
    imagem TEXT,
    reservas BOOLEAN,
    delivery BOOLEAN,
    estacionamento BOOLEAN,
    criado_por INT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (criado_por) REFERENCES usuarios(id),
    FOREIGN KEY (id_end) REFERENCES endereco(id_end),
    FOREIGN KEY (id_tel) REFERENCES telefone(id_tel)
);

-- Tabela de comentários (para eventos e restaurantes)
CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo_destino ENUM('evento', 'restaurante') NOT NULL,
    destino_id INT NOT NULL,
    conteudo TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabela de tags
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- Relacionamento entre eventos e tags
CREATE TABLE eventos_tags (
    evento_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (evento_id, tag_id),
    FOREIGN KEY (evento_id) REFERENCES eventos(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

-- Relacionamento entre restaurantes e tags
CREATE TABLE restaurantes_tags (
    restaurante_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (restaurante_id, tag_id),
    FOREIGN KEY (restaurante_id) REFERENCES restaurantes(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);
