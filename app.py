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

<<<<<<< HEAD
@app.route("/planejamento")
def planejamento():
    return render_template("planejamento.html")

@app.route("/financeiro")
def financeiro():
    return render_template("financeiro.html")

@app.route("/relatorios")
def relatorios():
    return render_template("relatorios.html")

if __name__ == "__main__":
    app.run(debug=True)
=======
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 57f539c90048fc28c25a199aacff999dda80cb03
