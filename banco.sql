-- Banco de dados para o projeto Encantos da Ilha
-- Sistema de eventos e restaurantes do Maranhão

CREATE DATABASE IF NOT EXISTS encantos_da_ilha;
USE encantos_da_ilha;

-- Tabela de Administradores
CREATE TABLE administradores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Eventos
CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_evento VARCHAR(200) NOT NULL,
    tipo ENUM('Show', 'Evento', 'Festival', 'Teatro', 'Exposição') NOT NULL,
    descricao TEXT,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    horario TIME NOT NULL,
    local VARCHAR(200) NOT NULL,
    endereco TEXT NOT NULL,
    preco DECIMAL(10,2),
    capacidade INT,
    organizador VARCHAR(100),
    contato VARCHAR(100),
    url_imagem VARCHAR(500),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Restaurantes
CREATE TABLE restaurantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_restaurante VARCHAR(200) NOT NULL,
    tipo_culinaria ENUM('Brasileira', 'Maranhense', 'Italiana', 'Japonesa', 'Mexicana', 'Francesa') NOT NULL,
    descricao TEXT,
    endereco TEXT NOT NULL,
    bairro VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    horario_funcionamento VARCHAR(100),
    faixa_preco ENUM('$ - Economico', '$$ - Moderado', '$$$ - Caro', '$$$$ - Muito Caro') NOT NULL,
    capacidade INT,
    url_imagem VARCHAR(500),
    aceita_reservas BOOLEAN DEFAULT FALSE,
    tem_delivery BOOLEAN DEFAULT FALSE,
    tem_estacionamento BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Inserir dados de exemplo para administrador
INSERT INTO administradores (nome, email, senha) VALUES 
('Administrador', 'admin@encantosdailha.com', 'admin123');

-- Inserir dados de exemplo para eventos
INSERT INTO eventos (nome_evento, tipo, descricao, data_inicio, data_fim, horario, local, endereco, preco, capacidade, organizador, contato, url_imagem) VALUES 
('Festival de Inverno de São Luís', 'Festival', 'Grande festival de música e cultura maranhense', '2025-08-15', '2025-08-17', '19:00:00', 'Centro Histórico', 'Praça Benedito Leite, Centro, São Luís - MA', 0.00, 5000, 'Prefeitura de São Luís', '(98) 3214-5678', 'https://example.com/festival.jpg'),
('Show de Bumba Meu Boi', 'Show', 'Apresentação tradicional do Bumba Meu Boi', '2025-08-20', '2025-08-20', '20:00:00', 'Teatro Arthur Azevedo', 'Rua do Sol, 180, Centro, São Luís - MA', 25.00, 800, 'Grupo Boi da Maioba', '(98) 99876-5432', 'https://example.com/bumba.jpg');

-- Inserir dados de exemplo para restaurantes
INSERT INTO restaurantes (nome_restaurante, tipo_culinaria, descricao, endereco, bairro, telefone, horario_funcionamento, faixa_preco, capacidade, url_imagem, aceita_reservas, tem_delivery, tem_estacionamento) VALUES 
('Restaurante do Porto', 'Maranhense', 'Especializado em frutos do mar e pratos típicos maranhenses', 'Av. Litorânea, 123', 'Ponta da Areia', '(98) 3235-1234', '11:00 às 23:00', '$$ - Moderado', 120, 'https://example.com/porto.jpg', TRUE, TRUE, TRUE),
('Cantina Italiana', 'Italiana', 'Autêntica culinária italiana no coração de São Luís', 'Rua Grande, 456', 'Centro', '(98) 3232-5678', '18:00 às 00:00', '$$$ - Caro', 80, 'https://example.com/italiana.jpg', TRUE, FALSE, FALSE);

