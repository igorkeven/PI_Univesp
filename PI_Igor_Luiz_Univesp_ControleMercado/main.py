

from flask import Flask, render_template,request,redirect,flash,session, url_for
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = "IGORKEVEN-M-S"


# acesso a pagina inicial
@app.route("/")
def index():
        with open('artesao.json') as TodosArtesao:  # abertura do arquivo JSON
            listaArtesao = json.load(TodosArtesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

            
            
                    

        return render_template('html/home.html',artesao=listaArtesao)


    


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
    email = request.form.get('EmailCliente') # pegando o email do formulario
    senha = request.form.get('SenhaCliente') # pegando a senha do formulario


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
    print(email)
    session['nomeUsuarioLogado'] = email
    with open('artesao.json') as artesao:  # abertura do arquivo JSON
        listaArtesao = json.load(artesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao
        cont = 0
        for artesao in listaArtesao:  # loop para separar os dados 
            cont +=1
            print(artesao['email'])
            if email == artesao['email'] and senha == artesao['senha']:#verificação se os dados escrito pelo usuario são iguais os salvos 
                return redirect('/artesao')
            if cont >= len(listaArtesao):
                flash('Email ou senha incorretos')
                return redirect('/loginArtesao')


# pagina de recuperação de senha 
@app.route('/esqueceuSenha')
def esqueceuSenha():
    return render_template('html/esqueceuSenha.html')




# função para enviar o email 
def enviar_email(destinatario, senha):
    remetente = "seu_email@gmail.com"
    senha_remetente = "sua_senha"

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = "Recuperação de senha"

    texto = f"Sua senha é {senha}."
    mensagem.attach(MIMEText(texto, 'plain'))

    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remetente, senha_remetente)
    servidor_smtp.sendmail(remetente, destinatario, mensagem.as_string())
    servidor_smtp.quit()


# verificação de email ja cadastrado e envio de email com a senha
@app.route('/enviarEmail', methods=['POST'])
def enviarEmail():
    email = request.form.get('emailArtesao')
    with open('artesao.json' and 'clientes.json') as clientesEartesao:  # abertura do arquivo JSON
        listaCadastrados = json.load(clientesEartesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

        for usuario in listaCadastrados:  # loop para separar os dados 

            if email == usuario['nome'] :#verificação se os dados escrito pelo usuario são iguais os salvos 
                enviar_email(email, usuario['senha'])
                # flash(f'Senha enviada para seu Email {email} ')
                return redirect('/esqueceuSenha') # codigo para enviar o email com a senha

            else:
              #  flash('Email não cadastrado')
                return redirect('/cadastro')


    
    


# acesso a pagina do artesão onde ele fara upload dos artesanatos
@app.route("/artesao")
def artesao():
    email = session['nomeUsuarioLogado'] 
    with open('artesao.json') as TodosArtesao:  # abertura do arquivo JSON
        listaArtesao = json.load(TodosArtesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

        for artesao in listaArtesao:  # loop para separar os dados 
            if email == artesao['email']:
                
                nome = artesao['nome']
                foto = artesao['foto']

                return render_template('html/artesao.html',artesao=artesao,nome=nome,foto=foto)


# rota e função para envio de foto de perfil
@app.route('/enviar_foto', methods=['POST'])
def enviar_foto():
    foto = request.files.get('foto')
    dadosUsuario_str = request.form.get('dadosUsuario')
    # substitui as aspas simples por aspas duplas
    dadosUsuario_str = dadosUsuario_str.replace("'", "\"")
    dadosUsuario = json.loads(dadosUsuario_str)
    nome_arquivo = f"fotoPerfil_{dadosUsuario['nome']}_id_{dadosUsuario['id']}"
    nome_arquivo = secure_filename(nome_arquivo) # obtém a extensão do arquivo carregado e adiciona ao nome do arquivo
    nome_arquivo = f"{nome_arquivo}.{foto.filename.split('.')[-1]}"
    foto.save(os.path.join('static/fotoPerfil', nome_arquivo))
    
    cont = 0
    with open('artesao.json') as TodosArtesao:  # abertura do arquivo JSON
        listaArtesao = json.load(TodosArtesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

        for artesao in listaArtesao:  # loop para separar os dados 
            cont +=1
            if dadosUsuario['email'] == artesao['email']:
                artesao['foto'] = nome_arquivo # atualiza o nome do arquivo no dicionário correspondente
                with open('artesao.json', 'w') as TodosArtesao:  # abre o arquivo JSON em modo de escrita
                    json.dump(listaArtesao, TodosArtesao, indent=4) # escreve a lista atualizada de volta no arquivo JSON
                return redirect('/artesao')



# rota que renderiza a pagina de cadastro
@app.route("/cadastrar")
def cadastrar():

    return render_template('html/cadastrar.html')


#rota para cadastrar artesao
@app.route("/cadastrarArtesao", methods=['POST'])
def cadastrarArtesao():
    # pegando os dados que o usuario digitou no formulario de cadastro de artesão
    email = request.form.get('emailArtesaoCadastro')
    senha = request.form.get('senhaArtesaoCadastro')
    nome = request.form.get('nomeCadastroartesao')
    chavepix = request.form.get('chavePIX')
    id = 0 # definindo um valor iniciar para o ID
    with open('artesao.json') as artesao_json: # abrindo o arquivo onde tem todos os usuarios ja cadastrados
        listaArtesao = json.load(artesao_json)# colocando todo arquivo dentro da variavel
    for artesao in listaArtesao: # fazend o laço em todos os usuarios salvos
        id = artesao['id'] +1 # pegando o ultimo ID e adicionando 1 para o novo ID
        if email == artesao['email']:# verificando se o novo usuario ja não esta cadastrado atravez do email
            flash('opa parece que esse email ja esta cadastrado, se caso tenha esquecido a senha click em esqueci minha senha!')
            return redirect('/cadastrar')# se ja tiver um email cadastrado ele redireciona e da essa menssagem
# criando um novo  usuario com os dados obitidos do formulario html
    user = [    
        {
        "email": email,
        "senha": senha,
        "nome": nome,
        "chavePIX": chavepix,
        "id": id ,
        "foto": ""}] # a foto de perfil sempre inicia vazia, depois o usuario pode adicionar uma...
    novaListaArtesao = listaArtesao + user # concatenando todos usuarios ja salvos com o novo e colocando em uma variavel
    with open('artesao.json', 'w') as artesao_json:# abrindo o arquivo JSON em mode de escrita(para edições)
        json.dump(novaListaArtesao,artesao_json, indent=4 )# salvando todos incluindo o novo usuario no arquivo JSON
    flash('Usuario cadastrado com sucesso!! BOAS VENDAS !!')
    return redirect('/loginArtesao') # redireciona para o login junto com a menssagem flash






if __name__ in '__main__':
    app.run( debug=True )
