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

-- =========================
-- ORDENS DE SERVIÇO
-- =========================
CREATE TABLE ordens_servico (
    id_os INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veiculo INTEGER NOT NULL,
    data_abertura DATE,
    quantidade_bancos INTEGER,
    padrao_veiculo BOOLEAN,
    personalizacao_igual BOOLEAN,
    observacoes TEXT,
    FOREIGN KEY (id_veiculo) REFERENCES veiculos(id_veiculo)
);

-- =========================
-- ESPUMAS
-- =========================
CREATE TABLE espumas (
    id_espuma INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    densidade TEXT,
    descricao TEXT
);

-- =========================
-- BANCOS
-- =========================
CREATE TABLE bancos (
    id_banco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_os INTEGER NOT NULL,
    posicao TEXT,
    troca_espuma BOOLEAN,
    id_espuma INTEGER,
    FOREIGN KEY (id_os) REFERENCES ordens_servico(id_os),
    FOREIGN KEY (id_espuma) REFERENCES espumas(id_espuma)
);

-- =========================
-- COSTURAS
-- =========================
CREATE TABLE costuras (
    id_costura INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    descricao TEXT
);

-- =========================
-- CORES
-- =========================
CREATE TABLE cores (
    id_cor INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
);

-- =========================
-- PERSONALIZAÇÕES
-- =========================
CREATE TABLE personalizacoes (
    id_personalizacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_banco INTEGER NOT NULL,
    id_costura INTEGER,
    id_cor_linha INTEGER,
    FOREIGN KEY (id_banco) REFERENCES bancos(id_banco),
    FOREIGN KEY (id_costura) REFERENCES costuras(id_costura),
    FOREIGN KEY (id_cor_linha) REFERENCES cores(id_cor)
);

-- =========================
-- TECIDOS
-- =========================
CREATE TABLE tecidos (
    id_tecido INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    material TEXT,
    fornecedor TEXT
);

-- =========================
-- BANCO_TECIDOS
-- =========================
CREATE TABLE banco_tecidos (
    id_banco INTEGER,
    id_tecido INTEGER,
    id_cor INTEGER,
    parte_banco TEXT,
    PRIMARY KEY (id_banco, id_tecido, parte_banco),
    FOREIGN KEY (id_banco) REFERENCES bancos(id_banco),
    FOREIGN KEY (id_tecido) REFERENCES tecidos(id_tecido),
    FOREIGN KEY (id_cor) REFERENCES cores(id_cor)
);
