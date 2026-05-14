import sqlite3

conexao = sqlite3.connect("vitalab.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cronograma_exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cronograma_id INTEGER,
    exercicio_id INTEGER,
    dia_semana TEXT,
    ordem INTEGER,

    FOREIGN KEY (cronograma_id)
        REFERENCES cronogramas(id),

    FOREIGN KEY (exercicio_id)
        REFERENCES exercicios(id)
)
""")

conexao.commit()
conexao.close()

print("Tabela cronograma_exercicios criada!")