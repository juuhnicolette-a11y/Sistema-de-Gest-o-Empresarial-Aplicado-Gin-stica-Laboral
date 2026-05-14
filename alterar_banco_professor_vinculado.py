import sqlite3

conexao = sqlite3.connect("vitalab.db")
cursor = conexao.cursor()

try:
    cursor.execute("""
        ALTER TABLE cadastros
        ADD COLUMN professor_responsavel_id INTEGER
    """)
    print("Campo professor_responsavel_id criado com sucesso!")
except sqlite3.OperationalError:
    print("O campo professor_responsavel_id já existe.")

conexao.commit()
conexao.close()