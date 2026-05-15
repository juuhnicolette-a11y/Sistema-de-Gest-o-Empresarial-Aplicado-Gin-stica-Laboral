from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect("vitalab.db")
    conexao.row_factory = sqlite3.Row
    return conexao

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/cadastros")
def cadastros():
    busca = request.args.get("busca", "")
    tipo = request.args.get("tipo", "")
    status = request.args.get("status", "")

    query = "SELECT * FROM cadastros WHERE 1=1"
    parametros = []

    if busca:
        query += " AND (nome_fantasia LIKE ? OR nome_professor LIKE ?)"
        parametros.extend([f"%{busca}%", f"%{busca}%"])

    if tipo:
        query += " AND tipo = ?"
        parametros.append(tipo)

    if status:
        query += " AND status = ?"
        parametros.append(status)

    conexao = conectar_banco()
    cadastros = conexao.execute(query, parametros).fetchall()
    conexao.close()

    return render_template("cadastros.html", cadastros=cadastros)

@app.route("/visualizacao-cadastro/<int:id>")
def visualizacao_cadastro(id):
    conexao = conectar_banco()
    cadastro = conexao.execute(
        "SELECT * FROM cadastros WHERE id = ?",
        (id,)
    ).fetchone()
    conexao.close()

    return render_template("visualizacao-cadastro.html", cadastro=cadastro)

@app.route("/editar-cadastro/<int:id>", methods=["GET", "POST"])
def editar_cadastro(id):
    conexao = conectar_banco()

    if request.method == "POST":
        print("FORMULÁRIO ENVIADO")
        print(request.form)

        dados = request.form

        conexao.execute("""
            UPDATE cadastros SET
                tipo = ?,
                status = ?,
                razao_social = ?,
                nome_fantasia = ?,
                cnpj = ?,
                inscricao_estadual = ?,
                endereco = ?,
                contato_responsavel = ?,
                email = ?,
                data_inicio_contrato = ?,
                data_renovacao_contrato = ?,
                valor_mensal = ?,
                dia_pagamento = ?,
                horarios_aulas = ?,
                professor_responsavel = ?,
                professor_responsavel_id = ?,
                dados_pagamento = ?,
                quantidade_alunos = ?,
                nome_professor = ?,
                cpf = ?,
                registro_mei = ?,
                registro_cref = ?,
                empresas_vinculadas = ?,
                valor_pagamento = ?
            WHERE id = ?
        """, (
            dados.get("tipo", ""),
    dados.get("status", ""),
    dados.get("razao_social", ""),
    dados.get("nome_fantasia", ""),
    dados.get("cnpj", ""),
    dados.get("inscricao_estadual", ""),
    dados.get("endereco", ""),
    dados.get("contato_responsavel", ""),
    dados.get("email", ""),
    dados.get("data_inicio_contrato", ""),
    dados.get("data_renovacao_contrato", ""),
    dados.get("valor_mensal", ""),
    dados.get("dia_pagamento", ""),
    dados.get("horarios_aulas", ""),
    dados.get("professor_responsavel", ""),
    dados.get("professor_responsavel_id", ""),
    dados.get("dados_pagamento", ""),
    dados.get("quantidade_alunos", ""),
    dados.get("nome_professor", ""),
    dados.get("cpf", ""),
    dados.get("registro_mei", ""),
    dados.get("registro_cref", ""),
    dados.get("empresas_vinculadas", ""),
    dados.get("valor_pagamento", ""),
            id
        ))

        conexao.commit()
        conexao.close()

        return redirect(f"/visualizacao-cadastro/{id}")

    cadastro = conexao.execute(
        "SELECT * FROM cadastros WHERE id = ?",
        (id,)
    ).fetchone()

    professores = conexao.execute("""
    SELECT id, nome_professor 
    FROM cadastros 
    WHERE tipo = 'Professor'
    """).fetchall()

    conexao.close()

    return render_template(
    "editar-cadastro.html",
    cadastro=cadastro,
    professores=professores
)

@app.route("/planejamento")
def planejamento():
    return render_template("planejamento.html")

@app.route("/exercicios")
def exercicios():

    conexao = conectar_banco()

    exercicios = conexao.execute("""
        SELECT * FROM exercicios
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "exercicios.html",
        exercicios=exercicios
    )

@app.route("/cadastro-exercicio", methods=["GET", "POST"])
def cadastro_exercicio():

    conexao = conectar_banco()

    if request.method == "POST":

        dados = request.form

        conexao.execute("""
            INSERT INTO exercicios (
                nome,
                repeticoes,
                tempo,
                adaptacoes,
                imagem,
                video
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            dados.get("nome", ""),
            dados.get("repeticoes", ""),
            dados.get("tempo", ""),
            dados.get("adaptacoes", ""),
            dados.get("imagem", ""),
            dados.get("video", "")
        ))

        conexao.commit()
        conexao.close()

        return redirect("/exercicios")

    conexao.close()

    return render_template("cadastro-exercicio.html")

@app.route("/cronogramas")
def cronogramas():

    conexao = conectar_banco()

    cronogramas = conexao.execute("""
        SELECT
            cronogramas.id,
            cronogramas.insumos,
            empresa.nome_fantasia AS empresa,
            professor.nome_professor AS professor

        FROM cronogramas

        LEFT JOIN cadastros AS empresa
            ON cronogramas.empresa_id = empresa.id

        LEFT JOIN cadastros AS professor
            ON cronogramas.professor_id = professor.id

        ORDER BY empresa.nome_fantasia
    """).fetchall()

    conexao.close()

    return render_template(
        "cronogramas.html",
        cronogramas=cronogramas
    )

@app.route("/cadastro-cronograma", methods=["GET", "POST"])
def cadastro_cronograma():

    conexao = conectar_banco()

    if request.method == "POST":

        dados = request.form

        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO cronogramas (
                empresa_id,
                professor_id,
                insumos
            ) VALUES (?, ?, ?)
        """, (
            dados.get("empresa_id"),
            dados.get("professor_id"),
            dados.get("insumos")
        ))

        cronograma_id = cursor.lastrowid

        exercicios = request.form.getlist("exercicios")

        for exercicio_id in exercicios:

            conexao.execute("""
                INSERT INTO cronograma_exercicios (
                    cronograma_id,
                    exercicio_id
                ) VALUES (?, ?)
            """, (
                cronograma_id,
                exercicio_id
            ))

        conexao.commit()
        conexao.close()

        return redirect("/cronogramas")

    empresas = conexao.execute("""
        SELECT id, nome_fantasia
        FROM cadastros
        WHERE tipo = 'Empresa'
    """).fetchall()

    professores = conexao.execute("""
        SELECT id, nome_professor
        FROM cadastros
        WHERE tipo = 'Professor'
    """).fetchall()

    exercicios = conexao.execute("""
        SELECT id, nome
        FROM exercicios
        ORDER BY nome
    """).fetchall()

    conexao.close()

    return render_template(
        "cadastro-cronograma.html",
        empresas=empresas,
        professores=professores,
        exercicios=exercicios
    )

@app.route("/financeiro")
def financeiro():
    return render_template("financeiro.html")

@app.route("/contas-pagar")
def contas_pagar():

    busca = request.args.get("busca", "")
    classificacao = request.args.get("classificacao", "")
    data_vencimento = request.args.get("data_vencimento", "")

    query = """
        SELECT
            contas_pagar.id,
            contas_pagar.data_vencimento,
            contas_pagar.valor,
            contas_pagar.classificacao,
            contas_pagar.status,
            cadastros.nome_fantasia,
            cadastros.nome_professor

        FROM contas_pagar

        LEFT JOIN cadastros
            ON contas_pagar.cadastro_id = cadastros.id

        WHERE 1=1
    """

    parametros = []

    if busca:
        query += """
            AND (
                cadastros.nome_fantasia LIKE ?
                OR cadastros.nome_professor LIKE ?
            )
        """
        parametros.extend([
            f"%{busca}%",
            f"%{busca}%"
        ])

    if classificacao:
        query += " AND contas_pagar.classificacao = ?"
        parametros.append(classificacao)

    if data_vencimento:
        query += " AND contas_pagar.data_vencimento = ?"
        parametros.append(data_vencimento)

    query += " ORDER BY contas_pagar.data_vencimento"

    conexao = conectar_banco()

    contas = conexao.execute(
        query,
        parametros
    ).fetchall()

    conexao.close()

    return render_template(
        "contas-pagar.html",
        contas=contas
    )

@app.route("/cadastro-conta-pagar", methods=["GET", "POST"])
def cadastro_conta_pagar():
    conexao = conectar_banco()

    if request.method == "POST":
        dados = request.form

        conexao.execute("""
            INSERT INTO contas_pagar (
                data_vencimento,
                valor,
                cadastro_id,
                classificacao,
                status,
                observacoes
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            dados.get("data_vencimento", ""),
            dados.get("valor", ""),
            dados.get("cadastro_id", ""),
            dados.get("classificacao", ""),
            dados.get("status", ""),
            dados.get("observacoes", "")
        ))

        conexao.commit()
        conexao.close()

        return redirect("/contas-pagar")

    cadastros = conexao.execute("""
        SELECT id, tipo, nome_fantasia, nome_professor
        FROM cadastros
        ORDER BY tipo, nome_fantasia, nome_professor
    """).fetchall()

    conexao.close()

    return render_template("cadastro-conta-pagar.html", cadastros=cadastros)

@app.route("/editar-conta-pagar/<int:id>", methods=["GET", "POST"])
def editar_conta_pagar(id):
    conexao = conectar_banco()

    if request.method == "POST":
        dados = request.form

        conexao.execute("""
            UPDATE contas_pagar SET
                data_vencimento = ?,
                valor = ?,
                cadastro_id = ?,
                classificacao = ?,
                status = ?,
                observacoes = ?
            WHERE id = ?
        """, (
            dados.get("data_vencimento", ""),
            dados.get("valor", ""),
            dados.get("cadastro_id", ""),
            dados.get("classificacao", ""),
            dados.get("status", ""),
            dados.get("observacoes", ""),
            id
        ))

        conexao.commit()
        conexao.close()

        return redirect("/contas-pagar")

    conta = conexao.execute("""
        SELECT *
        FROM contas_pagar
        WHERE id = ?
    """, (id,)).fetchone()

    cadastros = conexao.execute("""
        SELECT id, tipo, nome_fantasia, nome_professor
        FROM cadastros
        ORDER BY tipo, nome_fantasia, nome_professor
    """).fetchall()

    conexao.close()

    return render_template(
        "editar-conta-pagar.html",
        conta=conta,
        cadastros=cadastros
    )

@app.route("/contas-receber")
def contas_receber():

    busca = request.args.get("busca", "")
    classificacao = request.args.get("classificacao", "")
    data_recebimento = request.args.get("data_recebimento", "")

    query = """
        SELECT
            contas_receber.id,
            contas_receber.data_recebimento,
            contas_receber.valor,
            contas_receber.classificacao,
            contas_receber.status,
            cadastros.nome_fantasia,
            cadastros.nome_professor

        FROM contas_receber

        LEFT JOIN cadastros
            ON contas_receber.cadastro_id = cadastros.id

        WHERE 1=1
    """

    parametros = []

    if busca:
        query += """
            AND (
                cadastros.nome_fantasia LIKE ?
                OR cadastros.nome_professor LIKE ?
            )
        """
        parametros.extend([
            f"%{busca}%",
            f"%{busca}%"
        ])

    if classificacao:
        query += " AND contas_receber.classificacao = ?"
        parametros.append(classificacao)

    if data_recebimento:
        query += " AND contas_receber.data_recebimento = ?"
        parametros.append(data_recebimento)

    query += " ORDER BY contas_receber.data_recebimento"

    conexao = conectar_banco()

    contas = conexao.execute(
        query,
        parametros
    ).fetchall()

    conexao.close()

    return render_template(
        "contas-receber.html",
        contas=contas
    )

@app.route("/cadastro-conta-receber", methods=["GET", "POST"])
def cadastro_conta_receber():
    conexao = conectar_banco()

    if request.method == "POST":
        dados = request.form

        conexao.execute("""
            INSERT INTO contas_receber (
                data_recebimento,
                valor,
                cadastro_id,
                classificacao,
                status,
                observacoes
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            dados.get("data_recebimento", ""),
            dados.get("valor", ""),
            dados.get("cadastro_id", ""),
            dados.get("classificacao", ""),
            dados.get("status", ""),
            dados.get("observacoes", "")
        ))

        conexao.commit()
        conexao.close()

        return redirect("/contas-receber")

    cadastros = conexao.execute("""
        SELECT id, tipo, nome_fantasia, nome_professor
        FROM cadastros
        ORDER BY tipo, nome_fantasia, nome_professor
    """).fetchall()

    conexao.close()

    return render_template("cadastro-conta-receber.html", cadastros=cadastros)

@app.route("/relatorios")
def relatorios():
    return render_template("relatorios.html")

@app.route("/relatorio-cadastros")
def relatorio_cadastros():
    tipo = request.args.get("tipo", "")
    status = request.args.get("status", "")
    busca = request.args.get("busca", "")

    query = """
        SELECT *
        FROM cadastros
        WHERE 1=1
    """

    parametros = []

    if tipo:
        query += " AND tipo = ?"
        parametros.append(tipo)

    if status:
        query += " AND status = ?"
        parametros.append(status)

    if busca:
        query += """
            AND (
                nome_fantasia LIKE ?
                OR nome_professor LIKE ?
                OR email LIKE ?
            )
        """
        parametros.extend([
            f"%{busca}%",
            f"%{busca}%",
            f"%{busca}%"
        ])

    query += " ORDER BY tipo, nome_fantasia, nome_professor"

    conexao = conectar_banco()
    cadastros = conexao.execute(query, parametros).fetchall()
    conexao.close()

    return render_template(
        "relatorio-cadastros.html",
        cadastros=cadastros
    )

@app.route("/relatorio-cronogramas")
def relatorio_cronogramas():
    professor_id = request.args.get("professor_id", "")
    empresa = request.args.get("empresa", "")
    insumos = request.args.get("insumos", "")

    query = """
        SELECT
            cronogramas.id,
            cronogramas.insumos,
            empresa.nome_fantasia AS empresa,
            professor.nome_professor AS professor,
            GROUP_CONCAT(exercicios.nome, ', ') AS exercicios

        FROM cronogramas

        LEFT JOIN cadastros AS empresa
            ON cronogramas.empresa_id = empresa.id

        LEFT JOIN cadastros AS professor
            ON cronogramas.professor_id = professor.id

        LEFT JOIN cronograma_exercicios
            ON cronogramas.id = cronograma_exercicios.cronograma_id

        LEFT JOIN exercicios
            ON cronograma_exercicios.exercicio_id = exercicios.id

        WHERE 1=1
    """

    parametros = []

    if professor_id:
        query += " AND cronogramas.professor_id = ?"
        parametros.append(professor_id)

    if empresa:
        query += " AND empresa.nome_fantasia LIKE ?"
        parametros.append(f"%{empresa}%")

    if insumos:
        query += " AND cronogramas.insumos LIKE ?"
        parametros.append(f"%{insumos}%")

    query += """
        GROUP BY
            cronogramas.id,
            cronogramas.insumos,
            empresa.nome_fantasia,
            professor.nome_professor

        ORDER BY empresa.nome_fantasia
    """

    conexao = conectar_banco()

    cronogramas = conexao.execute(query, parametros).fetchall()

    professores = conexao.execute("""
        SELECT id, nome_professor
        FROM cadastros
        WHERE tipo = 'Professor'
        ORDER BY nome_professor
    """).fetchall()

    conexao.close()

    return render_template(
        "relatorio-cronogramas.html",
        cronogramas=cronogramas,
        professores=professores
    )

@app.route("/relatorio-contas-pagar")
def relatorio_contas_pagar():
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")
    classificacao = request.args.get("classificacao", "")

    query = """
        SELECT
            contas_pagar.data_vencimento,
            contas_pagar.valor,
            contas_pagar.classificacao,
            contas_pagar.status,
            cadastros.nome_fantasia,
            cadastros.nome_professor

        FROM contas_pagar

        LEFT JOIN cadastros
            ON contas_pagar.cadastro_id = cadastros.id

        WHERE 1=1
    """

    parametros = []

    if data_inicio:
        query += " AND contas_pagar.data_vencimento >= ?"
        parametros.append(data_inicio)

    if data_fim:
        query += " AND contas_pagar.data_vencimento <= ?"
        parametros.append(data_fim)

    if classificacao:
        query += " AND contas_pagar.classificacao = ?"
        parametros.append(classificacao)

    query += " ORDER BY contas_pagar.data_vencimento"

    conexao = conectar_banco()
    contas = conexao.execute(query, parametros).fetchall()
    conexao.close()

    return render_template(
        "relatorio-contas-pagar.html",
        contas=contas
    )

@app.route("/relatorio-contas-receber")
def relatorio_contas_receber():
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")
    classificacao = request.args.get("classificacao", "")

    query = """
        SELECT
            contas_receber.data_recebimento,
            contas_receber.valor,
            contas_receber.classificacao,
            contas_receber.status,
            cadastros.nome_fantasia,
            cadastros.nome_professor

        FROM contas_receber

        LEFT JOIN cadastros
            ON contas_receber.cadastro_id = cadastros.id

        WHERE 1=1
    """

    parametros = []

    if data_inicio:
        query += " AND contas_receber.data_recebimento >= ?"
        parametros.append(data_inicio)

    if data_fim:
        query += " AND contas_receber.data_recebimento <= ?"
        parametros.append(data_fim)

    if classificacao:
        query += " AND contas_receber.classificacao = ?"
        parametros.append(classificacao)

    query += " ORDER BY contas_receber.data_recebimento"

    conexao = conectar_banco()
    contas = conexao.execute(query, parametros).fetchall()
    conexao.close()

    return render_template(
        "relatorio-contas-receber.html",
        contas=contas
    )

@app.route("/novo-cadastro", methods=["GET", "POST"])
def novo_cadastro():
    conexao = conectar_banco()

    if request.method == "POST":
        dados = request.form

        conexao.execute("""
            INSERT INTO cadastros (
                tipo,
                status,
                razao_social,
                nome_fantasia,
                cnpj,
                inscricao_estadual,
                endereco,
                contato_responsavel,
                email,
                data_inicio_contrato,
                data_renovacao_contrato,
                valor_mensal,
                dia_pagamento,
                horarios_aulas,
                professor_responsavel_id,
                dados_pagamento,
                quantidade_alunos,
                nome_professor,
                cpf,
                registro_mei,
                registro_cref,
                empresas_vinculadas,
                valor_pagamento
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados.get("tipo", ""),
            dados.get("status", ""),
            dados.get("razao_social", ""),
            dados.get("nome_fantasia", ""),
            dados.get("cnpj", ""),
            dados.get("inscricao_estadual", ""),
            dados.get("endereco", ""),
            dados.get("contato_responsavel", ""),
            dados.get("email", ""),
            dados.get("data_inicio_contrato", ""),
            dados.get("data_renovacao_contrato", ""),
            dados.get("valor_mensal", ""),
            dados.get("dia_pagamento", ""),
            dados.get("horarios_aulas", ""),
            dados.get("professor_responsavel_id", ""),
            dados.get("dados_pagamento", ""),
            dados.get("quantidade_alunos", ""),
            dados.get("nome_professor", ""),
            dados.get("cpf", ""),
            dados.get("registro_mei", ""),
            dados.get("registro_cref", ""),
            dados.get("empresas_vinculadas", ""),
            dados.get("valor_pagamento", "")
        ))

        conexao.commit()
        conexao.close()

        return redirect("/cadastros")

    professores = conexao.execute("""
        SELECT id, nome_professor
        FROM cadastros
        WHERE tipo = 'Professor'
    """).fetchall()

    conexao.close()

    return render_template("novo-cadastro.html", professores=professores)

@app.route("/editar-exercicio/<int:id>", methods=["GET", "POST"])
def editar_exercicio(id):
    conexao = conectar_banco()

    if request.method == "POST":
        dados = request.form

        conexao.execute("""
            UPDATE exercicios SET
                nome = ?,
                repeticoes = ?,
                tempo = ?,
                adaptacoes = ?,
                imagem = ?,
                video = ?
            WHERE id = ?
        """, (
            dados.get("nome", ""),
            dados.get("repeticoes", ""),
            dados.get("tempo", ""),
            dados.get("adaptacoes", ""),
            dados.get("imagem", ""),
            dados.get("video", ""),
            id
        ))

        conexao.commit()
        conexao.close()

        return redirect("/exercicios")

    exercicio = conexao.execute(
        "SELECT * FROM exercicios WHERE id = ?",
        (id,)
    ).fetchone()

    conexao.close()

    return render_template("editar-exercicio.html", exercicio=exercicio)

@app.route("/editar-cronograma/<int:id>", methods=["GET", "POST"])
def editar_cronograma(id):

    conexao = conectar_banco()

    if request.method == "POST":

        dados = request.form

        conexao.execute("""
            UPDATE cronogramas SET
                empresa_id = ?,
                professor_id = ?,
                insumos = ?
            WHERE id = ?
        """, (
            dados.get("empresa_id"),
            dados.get("professor_id"),
            dados.get("insumos"),
            id
        ))

        conexao.execute("""
            DELETE FROM cronograma_exercicios
            WHERE cronograma_id = ?
        """, (id,))

        exercicios = request.form.getlist("exercicios")

        for exercicio_id in exercicios:

            conexao.execute("""
                INSERT INTO cronograma_exercicios (
                    cronograma_id,
                    exercicio_id
                ) VALUES (?, ?)
            """, (
                id,
                exercicio_id
            ))

        conexao.commit()

        return redirect("/cronogramas")

    cronograma = conexao.execute("""
        SELECT *
        FROM cronogramas
        WHERE id = ?
    """, (id,)).fetchone()

    empresas = conexao.execute("""
        SELECT id, nome_fantasia
        FROM cadastros
        WHERE tipo = 'Empresa'
    """).fetchall()

    professores = conexao.execute("""
        SELECT id, nome_professor
        FROM cadastros
        WHERE tipo = 'Professor'
    """).fetchall()

    exercicios = conexao.execute("""
        SELECT id, nome
        FROM exercicios
        ORDER BY nome
    """).fetchall()

    exercicios_selecionados = conexao.execute("""
        SELECT exercicio_id
        FROM cronograma_exercicios
        WHERE cronograma_id = ?
    """, (id,)).fetchall()

    conexao.close()

    exercicios_ids = [
        item["exercicio_id"]
        for item in exercicios_selecionados
    ]

    return render_template(
        "editar-cronograma.html",
        cronograma=cronograma,
        empresas=empresas,
        professores=professores,
        exercicios=exercicios,
        exercicios_ids=exercicios_ids
    )

@app.route("/editar-conta-receber/<int:id>", methods=["GET", "POST"])
def editar_conta_receber(id):
    conexao = conectar_banco()

    if request.method == "POST":
        dados = request.form

        conexao.execute("""
            UPDATE contas_receber SET
                data_recebimento = ?,
                valor = ?,
                cadastro_id = ?,
                classificacao = ?,
                status = ?,
                observacoes = ?
            WHERE id = ?
        """, (
            dados.get("data_recebimento", ""),
            dados.get("valor", ""),
            dados.get("cadastro_id", ""),
            dados.get("classificacao", ""),
            dados.get("status", ""),
            dados.get("observacoes", ""),
            id
        ))

        conexao.commit()
        conexao.close()

        return redirect("/contas-receber")

    conta = conexao.execute("""
        SELECT *
        FROM contas_receber
        WHERE id = ?
    """, (id,)).fetchone()

    cadastros = conexao.execute("""
        SELECT id, tipo, nome_fantasia, nome_professor
        FROM cadastros
        ORDER BY tipo, nome_fantasia, nome_professor
    """).fetchall()

    conexao.close()

    return render_template(
        "editar-conta-receber.html",
        conta=conta,
        cadastros=cadastros
    )


if __name__ == "__main__":
    app.run(debug=True)