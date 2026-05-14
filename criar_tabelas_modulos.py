import sqlite3

conexao = sqlite3.connect("vitalab.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    repeticoes TEXT,
    tempo TEXT,
    adaptacoes TEXT,
    imagem TEXT,
    video TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cronogramas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER,
    professor_id INTEGER,
    exercicios_dia TEXT,
    insumos TEXT,
    FOREIGN KEY (empresa_id) REFERENCES cadastros(id),
    FOREIGN KEY (professor_id) REFERENCES cadastros(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contas_pagar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_vencimento TEXT,
    valor TEXT,
    cadastro_id INTEGER,
    classificacao TEXT,
    status TEXT,
    observacoes TEXT,
    FOREIGN KEY (cadastro_id) REFERENCES cadastros(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contas_receber (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_recebimento TEXT,
    valor TEXT,
    cadastro_id INTEGER,
    classificacao TEXT,
    status TEXT,
    observacoes TEXT,
    FOREIGN KEY (cadastro_id) REFERENCES cadastros(id)
)
""")

conexao.commit()
conexao.close()

print("Tabelas dos módulos criadas com sucesso!")
