

from flask import Flask, render_template,request,redirect,flash,session, url_for
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SECRET_KEY'] = "IGORKEVEN-M-S"


# rota para fazer logout
@app.route('/sair')
def logout():
    session.clear() # Limpa a sessão
    return redirect('/') # Redireciona para a página inicial





# acesso a pagina inicial
@app.route("/")
def index():
    with open('clientes.json') as f:
        usuarios = json.load(f)

    with open('artesao.json') as TodosArtesao:  # abertura do arquivo JSON
        listaArtesao = json.load(TodosArtesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao
    if 'clienteLogado' in session:
        carrinho = 'click para ver seu carrinho'
        rotaCarrinho = '/cliente'
        btnCompra = 'Adicionar no Carrinho'
        rotaCompra = '/adicionarCarrinho'
        logado = True
        usuarioLogado = session['clienteLogado']
    else:
        carrinho = 'Faça Login'
        rotaCarrinho = '/login'
        btnCompra = 'Faça login para comprar'
        rotaCompra = '/login'
        usuarioLogado =''
        logado = False

    return render_template('html/home.html',usuarioLogado=usuarioLogado,usuarios=usuarios,artesao=listaArtesao,carrinho=carrinho,rotaCarrinho=rotaCarrinho,btnCompra=btnCompra,rotaCompra=rotaCompra,logado=logado)



@app.route('/adicionarCarrinho', methods=['POST'])
def adicionarCarrinho():
    imagem = request.form.get('imagem')
    descricao = request.form.get('descricao')
    preco = float(request.form.get('preco'))
    nome_produto = request.form.get('nome_produto')
    id_vendedor = int(request.form.get('id_vendedor'))
    pagina = request.form.get('pagina')
    with open('clientes.json') as f:
        usuarios = json.load(f)
    # Encontrar o usuário correto pelo seu ID
    for usuario in usuarios:
        if usuario['email'] == session['clienteLogado']:

            # Verificar se o produto já está no carrinho
            if nome_produto in usuario['carrinho']:
                # Incrementar a quantidade do produto em 1
                usuario['carrinho'][nome_produto]['quantidade'] += 1
            else:
                # Adicionar um novo produto ao carrinho
                usuario['carrinho'][nome_produto] = {
                    'imagem': imagem,
                    'descricao': descricao,
                    'preco': preco,
                    'id_vendedor': id_vendedor,
                    'quantidade': 1
                }
            # Somar os preços dos produtos no carrinho do usuário
            total_preco = sum([produto['preco'] * produto['quantidade'] for produto in usuario['carrinho'].values()])
            usuario['total_preco'] = total_preco
            # Salvar o conteúdo atualizado de volta no arquivo JSON
            with open('clientes.json', 'w') as f:
                json.dump(usuarios, f, indent=4)
            break  # sair do loop depois de encontrar o usuário correto


    if pagina == 'paginaCliente':
        return redirect('/cliente')
    return redirect('/')






@app.route('/excluirItemCarrinho', methods=['POST'])
def excluirItemCarrinho():
    nome_produto = request.form.get('nome_produto')
    id_vendedor = int(request.form.get('id_vendedor'))
    pagina = request.form.get('pagina')
    with open('clientes.json') as f:
        usuarios = json.load(f)
    
    # Encontrar o usuário correto pelo seu ID
        for usuario in usuarios:
            if id_vendedor == usuario['id']:
                if usuario['carrinho'][nome_produto] :
                    # Subtrair o valor do item do total_preco
                    usuario['total_preco'] -= usuario['carrinho'][nome_produto]['preco'] 
                    
                    # Verificar se a quantidade é maior que 1 antes de subtrair
                    if usuario['carrinho'][nome_produto]['quantidade'] > 1:
                        usuario['carrinho'][nome_produto]['quantidade'] -= 1
                    else:
                        del usuario['carrinho'][nome_produto]  # Se a quantidade for 1, remover o produto do carrinho
                    
                    # Salvar o conteúdo atualizado de volta no arquivo JSON
                    with open('clientes.json', 'w') as f:
                        json.dump(usuarios, f, indent=4)
                    break  # sair do loop depois de encontrar o usuário correto

    if pagina == 'paginaCliente':
        return redirect('/cliente')

    return redirect('/')








@app.route('/cliente')
def cliente():
    if 'clienteLogado' in session:
        email = session['clienteLogado']
        with open('clientes.json') as c:
            listaClientes = json.load(c)
        with open('artesao.json') as f:
            listaArtesao = json.load(f)

            ids_vendedores = []
            total_vendas = {} # dicionário para armazenar o valor total de vendas de cada vendedor
            for cliente in listaClientes:
                if email == cliente['email']:
                    nome = cliente['nome']
                    foto = cliente['foto']
                    dadosCliente = cliente

                    if cliente['carrinho']:
                        for produto, dados in cliente['carrinho'].items():
                            id_vendedor = dados['id_vendedor']
                            if id_vendedor not in ids_vendedores:
                                ids_vendedores.append(id_vendedor)
                            # adiciona o valor da venda do produto ao valor total de vendas do vendedor
                            if id_vendedor not in total_vendas:
                                total_vendas[id_vendedor] = dados['preco'] * dados['quantidade']
                            else:
                                total_vendas[id_vendedor] += dados['preco'] * dados['quantidade']

                    #dadosCliente['chavePIX'] = listaArtesao[id_vendedor - 1]['chavePIX'] # adiciona a chavePIX do vendedor ao cliente
                    valor_total_pago = dadosCliente['total_preco']
                    valor_total_vendas = sum(total_vendas.values())

                    # cria um dicionário para armazenar o valor que cada vendedor irá receber
                    valor_recebido_por_vendedor = {}
                    for vendedor in ids_vendedores:
                        valor_recebido_por_vendedor[vendedor] = (total_vendas[vendedor] / valor_total_vendas) * valor_total_pago

                    # passa as informações para o template HTML
                    return render_template('html/cliente.html', nome=nome, foto=foto,listaArtesao=listaArtesao , valor_recebido_por_vendedor=valor_recebido_por_vendedor,dadosCliente=dadosCliente)

    else:
        return redirect('/login')








# acesso a pagina de login do cliente para liberar as compras
@app.route("/login")
def login():
    return render_template('html/loginCliente.html')


# validação de login para liberar acesso ao cliente
@app.route("/acessoCliente", methods=['POST'])
def acessoCliente():
    email = request.form.get('EmailCliente') # pegando o email do formulario
    senha = request.form.get('SenhaCliente') # pegando a senha do formulario

    session['clienteLogado'] = email
    if 'artesaoLogado' in session:
        del session['artesaoLogado']
    with open('clientes.json') as clientes:  # abertura do arquivo JSON
        listaCliente = json.load(clientes) # colocando os dados do arquivo JSON dentro da variavel 
        cont = 0
        for cliente in listaCliente:  # loop para separar os dados 
            cont +=1
            if email == cliente['email'] and senha == cliente['senha']:#verificação se os dados escrito pelo usuario são iguais os salvos 
                
                return redirect('/cliente')

            if cont >= len(listaCliente):
                flash('Email ou senha incorretos')
                return redirect('/login')





# acesso a pagina do artesão onde ele fara upload dos artesanatos
@app.route('/artesao')
def artesao():
    
    if 'artesaoLogado' in session: # Verifica se a chave 'nomeUsuarioLogado' está presente na sessão
        
        email = session['artesaoLogado'] 
        with open('artesao.json') as TodosArtesao:  # abertura do arquivo JSON
            listaArtesao = json.load(TodosArtesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

            for artesao in listaArtesao:  # loop para separar os dados 
                if email == artesao['email']:
                    nome = artesao['nome']
                    foto = artesao['foto']
                    return render_template('html/artesao.html',artesao=artesao,nome=nome,foto=foto)
    else:
        # Usuário não está logado, redireciona para a página de login
        return redirect('/loginArtesao')




# acesso a pagina de login do artesão
@app.route("/loginArtesao")
def loginArtesao():

    return render_template('html/loginArtesao.html')


# validação de login para liberar acesso ao artesao
@app.route("/acessoArtesao", methods=['POST'])
def acessoArtesao():
    email = request.form.get('emailArtesao') # pegando o email do formulario
    senha = request.form.get('senhaArtesao') # pegando a senha do formulario
    session['artesaoLogado'] = email
    if 'clienteLogado' in session:
        del session['clienteLogado']
    with open('artesao.json') as artesao:  # abertura do arquivo JSON
        listaArtesao = json.load(artesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao
        cont = 0
        for artesao in listaArtesao:  # loop para separar os dados 
            cont +=1
            
            if email == artesao['email'] and senha == artesao['senha']:#verificação se os dados escrito pelo usuario são iguais os salvos 
                return redirect('/artesao')
            if cont >= len(listaArtesao):
                flash('Email ou senha incorretos')
                return redirect('/loginArtesao')

# cadastro de novo produto , salva a foto , edita o nome e coloca o novonome junto ao arquivo do usuario
@app.route('/novo_produto', methods=['POST'])
def novo_produto():
    foto = request.files.get('foto')
    nome_produto = request.form.get('nome')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')
    dados_usuario_str = request.form.get('dadosUsuario') 
    dados_usuario_str = dados_usuario_str.replace("'", "\"")
    print(f"dados_usuario_str: {dados_usuario_str}")
    dados_usuario = json.loads(dados_usuario_str)
    nome_arquivo = secure_filename(foto.filename) # obtém a extensão do arquivo carregado e adiciona ao nome do arquivo
    nome_arquivo = f"fotoProduto_{dados_usuario['nome']}_id_{dados_usuario['id']}_{nome_produto}"
    nome_arquivo = f"{nome_arquivo}.{foto.filename.split('.')[-1]}"
    foto.save(os.path.join('static/produtos', nome_arquivo))

    with open('artesao.json', 'r') as arq:
        lista_artesao = json.load(arq)

    for artesao in lista_artesao:
        if dados_usuario['email'] == artesao['email']:
            if 'produtos' not in artesao:
                artesao['produtos'] = {}
            artesao['produtos'][nome_produto] = {
                'imagem': nome_arquivo,
                'descricao': descricao,
                'preco': float(preco),
            }

    with open('artesao.json', 'w') as arq:
        json.dump(lista_artesao, arq, indent=4)

    return redirect('/artesao')





@app.route('/editar_produto', methods=['POST'])
def editar_produto():
    # Recebe os dados do formulário enviado
    nome = request.form.get('editar_nome')
    preco = request.form.get("editar_preco")
    descricao = request.form.get("editar_descricao")
    produto_dados_str = request.form.get("editar_produto_dados")
    produto_dados_str = produto_dados_str.replace("'", "\"")
    produto_dados = json.loads(produto_dados_str)
    nomeAntigo = request.form.get('nomeAntigo')

    # Carrega o arquivo JSON em memória
    with open('artesao.json', 'r') as f:
        data = json.load(f)

        for artesao in data:
            if produto_dados['id'] == artesao['id']:
                produtos = artesao['produtos']
                produtos_chaves = list(produtos.keys())
                index_antigo = produtos_chaves.index(nomeAntigo)

                produtos[nome] = {
                    "imagem": produtos[nomeAntigo]['imagem'],
                    "descricao": descricao,
                    "preco": preco
                }
                produtos.pop(nomeAntigo)
                produtos_chaves.pop(index_antigo)
                produtos_chaves.insert(index_antigo, nome)
                artesao['produtos'] = {chave: produtos[chave] for chave in produtos_chaves}

    with open('artesao.json', 'w') as f:
        json.dump(data, f, indent=4)



    # Redireciona o usuário para a página principal
    return redirect('/artesao')


# excluir produto
@app.route('/excluir_produto', methods=['POST'])
def excluir_produto():
    # Recebe o nome do produto a ser excluído do formulário enviado
    nome_produto = request.form.get('nomeProduto')
    produto_dados_str = request.form.get("produto_dados")
    produto_dados_str = produto_dados_str.replace("'", "\"")
    produto_dados = json.loads(produto_dados_str)

    # Carrega o arquivo JSON em memória
    with open('artesao.json', 'r') as f:
        data = json.load(f)

        for artesao in data:
            if produto_dados['id'] == artesao['id']:
                # pega o nome da imagem
                imagem_produto = artesao['produtos'][nome_produto]['imagem']
                # apaga a imagem do diretorio
                os.remove(os.path.join('static/produtos', imagem_produto))
                # Remove o produto do dicionário de produtos do artesão
                del artesao['produtos'][nome_produto]

    # Salva as alterações no arquivo JSON
    with open('artesao.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Redireciona o usuário para a página principal
    return redirect('/artesao')

#mudar senha artesão
@app.route('/mudar_senha', methods=['POST'])
def mudar_senha():

    novasenha = request.form.get('novaSenha')
    dados_usuario_str =  request.form.get('dadosUsuario')
    dados_usuario_str = dados_usuario_str.replace("'", "\"")
    dados_usuario = json.loads(dados_usuario_str)
    if 'artesaoLogado' in session:
        with open('artesao.json') as f:
            artesoes = json.load(f)
            for artesao in artesoes:
                if artesao['email'] == dados_usuario['email']:
                    artesao['senha'] = novasenha
        
        with open('artesao.json', 'w') as f:
            json.dump(artesoes, f, indent=4)
        flash(f'Senha alterada com sucesso, a nova senha é {novasenha}')
        return redirect('/artesao')
    
    if 'clienteLogado' in session:
        with open('clientes.json') as f:
            usuarios = json.load(f)
            for usuario in usuarios:
                if usuario['email'] == dados_usuario['email']:
                    usuario['senha'] = novasenha
                    
        with open('clientes.json', 'w') as f:
            json.dump(usuarios, f, indent=4)
        flash(f'Senha alterada com sucesso, a nova senha é {novasenha}')
        return redirect('/cliente')


   


    

# apagar conta de usuario artesão
@app.route('/apagar_conta', methods=['POST'])
def apagar_conta():
    emailUsuario = request.form.get('EmailUsuario')



    if 'artesaoLogado' in session:
        
        with open('artesao.json') as TodosArtesao: 
            listaArtesao = json.load(TodosArtesao)
            for artesao in listaArtesao:
                if artesao['email'] == emailUsuario:
                    
                    listaArtesao.remove(artesao)
                    del session['artesaoLogado']
        with open('artesao.json', 'w') as f:
            json.dump(listaArtesao, f, indent=4)
    

    if 'clienteLogado' in session:
        with open('clientes.json') as f:
            usuarios = json.load(f)
            for usuario in usuarios:
                if usuario['email'] == emailUsuario:
                    usuarios.remove(usuario)
                    del session['clienteLogado']
        with open('clientes.json', 'w') as f:
            json.dump(usuarios, f, indent=4)



    return redirect('/')

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
            

            if email == usuario['email'] :#verificação se os dados escrito pelo usuario são iguais os salvos 
                enviar_email(email, usuario['senha'])
                flash(f'Senha enviada para seu Email {email} ')
                return redirect('/esqueceuSenha') # codigo para enviar o email com a senha

            else:
                flash('Email não cadastrado')
                return redirect('/cadastrar')


    
    



# rota e função para envio de foto de perfil
@app.route('/enviar_foto', methods=['POST'])
def enviar_foto():
    retornoRota = request.form.get('retornoRota')
    foto = request.files.get('foto')
    dadosUsuario_str = request.form.get('dadosUsuario')
    
    # substitui as aspas simples por aspas duplas
    dadosUsuario_str = dadosUsuario_str.replace("'", "\"")
    dadosUsuario = json.loads(dadosUsuario_str)
    nome_arquivo = f"fotoPerfil_{dadosUsuario['nome']}_id_{dadosUsuario['id']}"
    nome_arquivo = secure_filename(nome_arquivo) # obtém a extensão do arquivo carregado e adiciona ao nome do arquivo
    nome_arquivo = f"{nome_arquivo}.{foto.filename.split('.')[-1]}"

    foto.save(os.path.join('static/fotoPerfil', nome_arquivo))
    if retornoRota == '/artesao':
        
        with open('artesao.json') as TodosArtesao:  # abertura do arquivo JSON
            listaArtesao = json.load(TodosArtesao) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

            for artesao in listaArtesao:  # loop para separar os dados 
               
                if dadosUsuario['email'] == artesao['email']:
                    artesao['foto'] = nome_arquivo # atualiza o nome do arquivo no dicionário correspondente
                    with open('artesao.json', 'w') as TodosArtesao:  # abre o arquivo JSON em modo de escrita
                        json.dump(listaArtesao, TodosArtesao, indent=4) # escreve a lista atualizada de volta no arquivo JSON
    else:
        with open('clientes.json') as c:  # abertura do arquivo JSON
            lista = json.load(c) # colocando os dados do arquivo JSON dentro da variavel listaArtesao

            for cliente in lista:  # loop para separar os dados 
                
                if dadosUsuario['email'] == cliente['email']:
                    cliente['foto'] = nome_arquivo # atualiza o nome do arquivo no dicionário correspondente
                    with open('clientes.json', 'w') as all:  # abre o arquivo JSON em modo de escrita
                        json.dump(lista, all, indent=4) # escreve a lista atualizada de volta no arquivo JSON


    return redirect(retornoRota)



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




#rota para cadastrar cliente
@app.route("/cadastrarCliente", methods=['POST'])
def cadastrarCliente():
    # pegando os dados que o usuario digitou no formulario de cadastro 
    email = request.form.get('emailClienteCadastro')
    senha = request.form.get('senhaClienteCadastro')
    nome = request.form.get('nomeCadastroCliente')
    id = 0 # definindo um valor iniciar para o ID
    with open('clientes.json') as cliente_json: # abrindo o arquivo onde tem todos os usuarios ja cadastrados
        listaCliente = json.load(cliente_json)# colocando todo arquivo dentro da variavel
    for cliente in listaCliente: # fazend o laço em todos os usuarios salvos
        id = cliente['id'] +1 # pegando o ultimo ID e adicionando 1 para o novo ID
        if email == cliente['email']:# verificando se o novo usuario ja não esta cadastrado atravez do email
            flash('opa parece que esse email ja esta cadastrado, se caso tenha esquecido a senha click em esqueci minha senha!')
            return redirect('/cadastrar')# se ja tiver um email cadastrado ele redireciona e da essa menssagem
# criando um novo  usuario com os dados obitidos do formulario html
    user = [    
        {
        "nome": nome,
        "email": email,
        "senha": senha,
        "id": id ,
        "foto": "",
        "carrinho": {},
        "total_preco": 0.0
        }
        ] # a foto de perfil sempre inicia vazia, depois o usuario pode adicionar uma...
    novaListaCliente = listaCliente + user # concatenando todos usuarios ja salvos com o novo e colocando em uma variavel
    with open('clientes.json', 'w') as cliente_json:# abrindo o arquivo JSON em mode de escrita(para edições)
        json.dump(novaListaCliente,cliente_json, indent=4 )# salvando todos incluindo o novo usuario no arquivo JSON
    flash('Usuario cadastrado com sucesso!! BOAS COMPRAS !!')
    return redirect('/login') # redireciona para o login junto com a menssagem flash






if __name__ in '__main__':
    app.run( debug=True )
