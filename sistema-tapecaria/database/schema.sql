-- =========================
-- TABELA CLIENTES
-- =========================

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_cliente VARCHAR(20) NOT NULL UNIQUE, -- Código de identificação do cliente CPF ou CNPJ
    nome VARCHAR(120) NOT NULL
);


-- =========================
-- TELEFONES DO CLIENTE
-- =========================

CREATE TABLE telefones_cliente (
    id_telefone INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    telefone VARCHAR(20) NOT NULL,

    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id_cliente)
);


-- =========================
-- ENDEREÇOS DO CLIENTE
-- =========================

CREATE TABLE enderecos_cliente (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,

    rua VARCHAR(150),
    numero VARCHAR(10),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2),
    cep CHAR(8),

    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id_cliente)
);


-- =========================
-- VEÍCULOS
-- =========================

CREATE TABLE veiculos (
    id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,

    id_cliente INTEGER NOT NULL,

    placa CHAR(7) NOT NULL UNIQUE,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(80) NOT NULL,
    ano INTEGER,
    cor VARCHAR(30),

    FOREIGN KEY (id_cliente)
    REFERENCES clientes(id_cliente)
);