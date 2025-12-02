CREATE TABLE IF NOT EXISTS persistencia (
    id SERIAL PRIMARY KEY,
    mensagem VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO persistencia (mensagem) VALUES ('Dado persistente inserido na primeira inicialização.');