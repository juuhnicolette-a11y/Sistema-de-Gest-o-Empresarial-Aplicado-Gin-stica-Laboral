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

if __name__ == "__main__":
    app.run(debug=True)
