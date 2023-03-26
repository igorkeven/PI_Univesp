

from flask import Flask, render_template

app = Flask(__name__)


# acesso a pagina inicial
@app.route("/")
def index():
    return render_template("html/home.html")


# acesso a pagina produtos
@app.route("/produtos")
def produtos():
    return render_template('html/produtos.html')


# acesso a pagina de login do cliente para liberar as compras
@app.route("/login")
def login():
    return render_template('html/login.html')

# acesso a pagina de login do artesão
@app.route("/loginArtesao")
def loginArtesao():
    return render_template('html/loginArtesao.html')

# acesso a pagina do artesão onde ele fara upload dos artesanatos
@app.route("/artesao")
def artesao():
    return render_template('html/artesao.html')



if __name__ in '__main__':
    app.run( debug=True )
