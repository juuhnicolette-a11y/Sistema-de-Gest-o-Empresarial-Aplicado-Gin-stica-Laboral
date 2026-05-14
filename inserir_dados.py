import sqlite3

conexao = sqlite3.connect("vitalab.db")
cursor = conexao.cursor()

cursor.execute("""
INSERT INTO cadastros (
    tipo,
    status,
    nome_fantasia,
    nome_professor
)
VALUES (?, ?, ?, ?)
""", (
    "Empresa",
    "Ativo",
    "Empresa Saúde Ativa",
    ""
))

cursor.execute("""
INSERT INTO cadastros (
    tipo,
    status,
    nome_fantasia,
    nome_professor
)
VALUES (?, ?, ?, ?)
""", (
    "Professor",
    "Ativo",
    "",
    "João Silva"
))

conexao.commit()
conexao.close()

print("Dados inseridos com sucesso!")