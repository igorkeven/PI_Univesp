

from flask import Flask, render_template,request,redirect,flash,session
import json

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
    return render_template('html/loginCliente.html')


# validação de login para liberar acesso ao cliente
@app.route("/acessoCliente", methods=['POST'])
def acessoCliente():
    email = request.form.get('') # pegando o email do formulario
    senha = request.form.get('') # pegando a senha do formulario


    with open('clientes.json') as clientes:  # abertura do arquivo JSON
        listaCliente = json.load(clientes) # colocando os dados do arquivo JSON dentro da variavel 

        for cliente in listaCliente:  # loop para separar os dados 

            if email == cliente['nome'] and senha == cliente['senha']:#verificação se os dados escrito pelo usuario são iguais os salvos 
                return render_template('html/cliente.html')
            else:
               # flash('Email ou senha incorretos')
                return redirect('/login')



# acesso a pagina de login do artesão
@app.route("/loginArtesao")
def loginArtesao():

    return render_template('html/loginArtesao.html')


# validação de login para liberar acesso ao artesao
@app.route("/acessoArtesao", methods=['POST'])
def acessoArtesao():
    email = request.form.get('emailArtesao') # pegando o email do formulario
    senha = request.form.get('senhaArtesao') # pegando a senha do formulario


    with open('artesao.json') as artesao:  # abertura do arquivo JSON
        listaArtesao = json.load(artesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

        for artesao in listaArtesao:  # loop para separar os dados 

            if email == artesao['nome'] and senha == artesao['senha']:#verificação se os dados escrito pelo usuario são iguais os salvos 
                return render_template('html/artesao.html')
            else:
              #  flash('Email ou senha incorretos')
                return redirect('/loginArtesao')


# pagina de recuperação de senha 
@app.route('/esqueceuSenha')
def esqueceuSenha():
    return render_template('html/esqueceuSenha.html')



# verificação de email ja cadastrado e envio de email com a senha
@app.route('/enviarEmail', methods=['POST'])
def enviarEmail():
    email = request.form.get('emailArtesao')
    with open('artesao.json' and 'clientes.json') as clientesEartesao:  # abertura do arquivo JSON
        listaCadastrados = json.load(clientesEartesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

        for usuario in listaCadastrados:  # loop para separar os dados 

            if email == usuario['nome'] :#verificação se os dados escrito pelo usuario são iguais os salvos 

                # flash(f'Senha enviada para seu Email {email} ')
                print(usuario['nome'])
                print(usuario['senha'])
                return redirect('/esqueceuSenha') # codigo para enviar o email com a senha

            else:
              #  flash('Email não cadastrado')
                return redirect('/cadastro')


    
    


# acesso a pagina do artesão onde ele fara upload dos artesanatos
@app.route("/artesao")
def artesao():
    return render_template('html/artesao.html')



if __name__ in '__main__':
    app.run( debug=True )
