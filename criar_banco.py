import sqlite3

conexao = sqlite3.connect("vitalab.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cadastros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    status TEXT NOT NULL,

    razao_social TEXT,
    nome_fantasia TEXT,
    cnpj TEXT,
    inscricao_estadual TEXT,
    endereco TEXT,
    contato_responsavel TEXT,
    email TEXT,
    data_inicio_contrato TEXT,
    data_renovacao_contrato TEXT,
    valor_mensal TEXT,
    dia_pagamento TEXT,
    horarios_aulas TEXT,
    professor_responsavel TEXT,
    dados_pagamento TEXT,
    quantidade_alunos TEXT,

    nome_professor TEXT,
    cpf TEXT,
    registro_mei TEXT,
    registro_cref TEXT,
    empresas_vinculadas TEXT,
    valor_pagamento TEXT
)
""")

conexao.commit()
conexao.close()

print("Banco de dados criado com sucesso!")