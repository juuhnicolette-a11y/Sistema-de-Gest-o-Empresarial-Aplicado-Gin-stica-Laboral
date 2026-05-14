from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/cadastros")
def cadastros():
    return render_template("cadastros.html")

@app.route("/visualizacao-cadastro")
def visualizacao_cadastro():
    return render_template("visualizacao-cadastro.html")

@app.route("/editar-cadastro")
def editar_cadastro():
    return render_template("editar-cadastro.html")

@app.route("/planejamento")
def planejamento():
    return render_template("planejamento.html")

@app.route("/exercicios")
def exercicios():
    return render_template("exercicios.html")

@app.route("/cadastro-exercicio")
def cadastro_exercicio():
    return render_template("cadastro-exercicio.html")

@app.route("/cronogramas")
def cronogramas():
    return render_template("cronogramas.html")

@app.route("/cadastro-cronograma")
def cadastro_cronograma():
    return render_template("cadastro-cronograma.html")

@app.route("/financeiro")
def financeiro():
    return render_template("financeiro.html")

@app.route("/contas-pagar")
def contas_pagar():
    return render_template("contas-pagar.html")

@app.route("/cadastro-conta-pagar")
def cadastro_conta_pagar():
    return render_template("cadastro-conta-pagar.html")

@app.route("/editar-conta-pagar")
def editar_conta_pagar():
    return render_template("editar-conta-pagar.html")

@app.route("/contas-receber")
def contas_receber():
    return render_template("contas-receber.html")

@app.route("/cadastro-conta-receber")
def cadastro_conta_receber():
    return render_template("cadastro-conta-receber.html")

@app.route("/editar-conta-receber")
def editar_conta_receber():
    return render_template("editar-conta-receber.html")

@app.route("/relatorios")
def relatorios():
    return render_template("relatorios.html")

@app.route("/relatorio-cadastros")
def relatorio_cadastros():
    return render_template("relatorio-cadastros.html")

@app.route("/relatorio-cronogramas")
def relatorio_cronogramas():
    return render_template("relatorio-cronogramas.html")

@app.route("/relatorio-contas-pagar")
def relatorio_contas_pagar():
    return render_template("relatorio-contas-pagar.html")

@app.route("/relatorio-contas-receber")
def relatorio_contas_receber():
    return render_template("relatorio-contas-receber.html")

if __name__ == "__main__":
    app.run(debug=True)