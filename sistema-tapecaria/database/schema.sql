-- =========================
-- TABELA CLIENTES
-- =========================
CREATE TABLE clientes (
    id_cliente  INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_cliente VARCHAR(20) NOT NULL UNIQUE,
    nome        VARCHAR(120) NOT NULL
);

-- =========================
-- TELEFONES DO CLIENTE
-- =========================
CREATE TABLE telefones_cliente (
    id_telefone INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente  INTEGER NOT NULL,
    telefone    VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- =========================
-- ENDEREÇOS DO CLIENTE
-- =========================
CREATE TABLE enderecos_cliente (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente  INTEGER NOT NULL,
    rua         VARCHAR(150),
    numero      VARCHAR(10),
    bairro      VARCHAR(100),
    cidade      VARCHAR(100),
    estado      CHAR(2),
    cep         CHAR(8),
    complemento VARCHAR(100),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- =========================
-- VEÍCULOS
-- =========================
CREATE TABLE veiculos (
    id_veiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    placa   CHAR(7) NOT NULL UNIQUE,
    marca   VARCHAR(50) NOT NULL,
    modelo  VARCHAR(80) NOT NULL,
    ano     INTEGER,
    cor     VARCHAR(30),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
--------------------------------------------------------------------
-- =========================
-- CATÁLOGO DE ITENS
-- =========================
-- TECIDO/REVESTIMENTO
CREATE TABLE tecido (
    id_tecido VARCHAR(100) NOT NULL UNIQUE,
    material VARCHAR(50) NOT NULL,
    descricao TEXT
);
-- ESPUMA
CREATE TABLE espuma (   
    id_espuma VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL,
    densidade VARCHAR(20),
    descricao TEXT
);
-- COSTURA
CREATE TABLE costura (
    id_costura VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL,
    descricao TEXT
);
-- COR DA LINHA
CREATE TABLE cor (
    id_cor VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT
);

-- =========================
-- 'SUBTABELAS' DE ORÇAMENTO (ITENS DO ORÇAMENTO)
-- =========================
-- ESPUMA
CREATE TABLE orcamento_espuma (
    id_orcamento INT,
    id_espuma INT,
    obs_item TEXT,
    PRIMARY KEY (id_orcamento, id_espuma),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id_orcamento),
    FOREIGN KEY (id_espuma) REFERENCES espuma(id_espuma)
);
-- COSTURA
CREATE TABLE orcamento_costura (
    id_orcamento INT,
    id_costura INT,
    obs_item TEXT,
    PRIMARY KEY (id_orcamento, id_costura),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id_orcamento),
    FOREIGN KEY (id_costura) REFERENCES costura(id_costura)
);
-- COR DA LINHA
CREATE TABLE orcamento_cor (
    id_orcamento INT,
    id_cor INT,
    obs_item TEXT,
    PRIMARY KEY (id_orcamento, id_cor),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id_orcamento),
    FOREIGN KEY (id_cor) REFERENCES cor(id_cor)
);
-- TECIDO/REVESTIMENTO
CREATE TABLE orcamento_tecido (
    id_orcamento INT,
    id_tecido INT,
    obs_item TEXT,
    PRIMARY KEY (id_orcamento, id_tecido),
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id_orcamento),
    FOREIGN KEY (id_tecido) REFERENCES tecido(id_tecido)
);

-- Tabela principal de orçamentos
CREATE TABLE orcamento (
    id_orcamento INT PRIMARY KEY AUTO_INCREMENT,
    id_veiculo INT NOT NULL,
    dat_orcamento DATE NOT NULL,
    bool_original BOOLEAN DEFAULT FALSE,
    bool_logo_prensada BOOLEAN DEFAULT FALSE,
    qtd_bancos INT DEFAULT 0,
    qtd_apoio_cabeca INT DEFAULT 0,
    bool_espuma BOOLEAN DEFAULT FALSE,
    valor DECIMAL(10,2) NOT NULL,
    obs TEXT
);
-- =========================
-- PEDIDOS (REGISTRO DE SERVIÇOS INICIADOS)
-- =========================
CREATE TABLE pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    id_orcamento INTEGER NOT NULL,
    boolean_aceite_cliente BOOLEAN DEFAULT FALSE,
    dat_aceite_cliente DATE,
    data_inicio DATE,
    data_conclusao DATE,
    observacoes_pedido TEXT,
    aceite_cliente BOOLEAN,
    status TEXT,
    valor_total REAL,
    metodo_pagamento TEXT,
    FOREIGN KEY (id_orcamento) REFERENCES orcamento(id_orcamento)
);
