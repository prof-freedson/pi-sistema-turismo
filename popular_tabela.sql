INSERT INTO usuarios (nome, email, senha, tipo) VALUES
('João Silva', 'joao@example.com', 'senha123', 'admin'),
('Maria Souza', 'maria@example.com', 'senha456', 'comum'),
('Carlos Lima', 'carlos@example.com', 'senha789', 'comum');


INSERT INTO endereco (rua, numero, bairro, cidade, estado) VALUES
('Rua dos Afogados', '101', 'Centro', 'São Luís', 'MA'),
('Av. Litorânea', '200', 'Calhau', 'São Luís', 'MA'),
('Rua Grande', '321', 'Centro', 'Caxias', 'MA'),
('Travessa das Flores', '87', 'Anil', 'São Luís', 'MA');


INSERT INTO telefone (fone_1, fone_2) VALUES
('98 99123-4567', '98 99234-5678'),
('98 98876-5432', NULL),
('98 98765-4321', '98 99654-3210');

INSERT INTO categorias (nome, descricao) VALUES
('Cultural', 'Eventos culturais e artísticos'),
('Gastronômico', 'Restaurantes e festivais de comida'),
('Música', 'Shows e apresentações musicais');


INSERT INTO eventos (nome, descricao, categoria_id, data_inicio, data_fim, horario, local, id_end, preco, capacidade, organizador, contato, imagem, criado_por)
VALUES
('Festival Folclórico de São Luís', 'Celebração das tradições maranhenses', 1, '2025-08-10', '2025-08-15', '18:00:00', 'Praça Maria Aragão', 1, 0.00, 500, 'Prefeitura de São Luís', '98 98123-1234', 'folclore.jpg', 1),
('Show de Reggae Roots', 'Apresentação com artistas locais', 3, '2025-09-05', '2025-09-05', '20:00:00', 'Espaço Cultural', 2, 50.00, 300, 'Associação Reggae Maranhão', '98 98765-4321', 'reggae.jpg', 2);


INSERT INTO restaurantes (nome, descricao, tipo_cozinha, id_end, id_tel, horario_funcionamento, faixa_preco, capacidade, avaliacao, imagem, reservas, delivery, estacionamento, criado_por)
VALUES
('Sabor Maranhense', 'Culinária típica com ingredientes locais', 'Maranhense', 3, 1, '11:00 às 22:00', 'R$$', 80, 5, 'sabor.jpg', TRUE, TRUE, TRUE, 1),
('Cantina São Luís', 'Especialidades italianas em ambiente familiar', 'Italiana', 4, 2, '12:00 às 23:00', 'R$$$', 100, 4, 'cantina.jpg', TRUE, FALSE, FALSE, 2);


INSERT INTO comentarios (usuario_id, tipo_destino, destino_id, conteudo)
VALUES
(2, 'evento', 1, 'Evento incrível, muito bem organizado!'),
(3, 'restaurante', 1, 'Comida deliciosa, voltarei com certeza.');


INSERT INTO tags (nome) VALUES
('Ao ar livre'),
('Pet friendly'),
('Vegetariano'),
('Gratuito'),
('Familiar');