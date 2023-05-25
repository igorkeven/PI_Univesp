

from flask import Flask, render_template,request,redirect,flash,session,url_for
import json
import os
from datetime import date, time, datetime
import mysql.connector


app = Flask(__name__)
app.config['SECRET_KEY'] = 'igorkeven'


def executar_consulta(consulta_sql):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bancodados_site_mercado_pi_univesp"
    )

    # Criar um cursor para executar as consultas SQL
    cursor = db.cursor()

    # Executar a consulta SQL
    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    db.close()

    return resultados


def enviar_dados_bd(instrucao_sql):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bancodados_site_mercado_pi_univesp"
    )

    # Criar um cursor para executar as instruções SQL
    cursor = db.cursor()

    try:
        # Executar a instrução SQL
        cursor.execute(instrucao_sql)

        # Confirmar as alterações no banco de dados
        db.commit()

        print("Dados enviados com sucesso para o banco de dados.")
    except mysql.connector.Error as error:
        # Lidar com erros ao enviar os dados para o banco de dados
        print("Erro ao enviar os dados para o banco de dados:", error)

    # Fechar a conexão com o banco de dados
    db.close()





@app.route("/")
def index():
    
    vendedores = executar_consulta("SELECT * FROM vendedores")

    # Consulta SQL para recuperar os dados dos clientes
    
    clientes = executar_consulta("SELECT * FROM usuarios")

    
    produtos_vendedor = executar_consulta("SELECT * FROM produtos_vendedor")

    
    carrinho = executar_consulta("SELECT * FROM carrinho")


    

    if 'cliente' in session:
        logado = True
        usuarioLogado = session['cliente']
    
    else:
        logado = False
        usuarioLogado = ''

    
    quantidades_vendidas = executar_consulta("SELECT quantidade_vendida FROM produtos_vendedor")

    produtos_destaque = []
    for quantidade_vendida in quantidades_vendidas:
        produtos_destaque.append(quantidade_vendida[0])

    quantidade_ordenada = sorted(produtos_destaque, reverse=True)
    quantidades_selecionadas = quantidade_ordenada[:3]

    print("quantidades_selecionadas")
    print(quantidades_selecionadas)
    print()
    print("usuarioLogado")
    print(usuarioLogado)
    print()
    print("vendedores")
    print(vendedores)
    print()
    print("clientes")
    print(clientes)
    print()
    print("produtos_vendedor")
    print(produtos_vendedor)
    print()
    print("carrinho")
    print(carrinho)
    print()


    return render_template('home.html',quantidades_selecionadas=quantidades_selecionadas,usuarioLogado=usuarioLogado,logado=logado, vendedores=vendedores, clientes=clientes, produtos_vendedor=produtos_vendedor, carrinho=carrinho )





@app.route('/sair')
def sair():
    session.clear()
    return redirect('/')

@app.route('/loginVendedor')
def loginVendedor():

    return render_template('loginVendedor.html')

@app.route("/acessoVendedor" , methods=['POST'])
def acessoVendedor():
    email = request.form.get('emailvendedor')
    senha = request.form.get('senhavendedor')
    
    vendedores = executar_consulta("SELECT * FROM vendedores")

    cont = 0
    for usuario in vendedores:
        cont += 1 
        
        if email == usuario[0]   and senha == usuario[2] :
            session['vendedor'] = email
            if 'cliente' in session:
                del session['cliente']
            return redirect('/vendedor')
        if cont >= len(vendedores):
            flash('Email ou senha incorretos.')
            
            return redirect('/loginVendedor')


# ------------------ pagina de login do cliente ---------------------------------------------------------------

@app.route('/loginCliente')
def loginCliente():
    if 'cliente' in session:
        del session['cliente']
    return render_template('loginCliente.html')
#---------------------------------------------------------------------------------------------------------



# -------------- rota de verificação para liberar aceço de cliente ----------------------------------------

@app.route("/acessoCliente", methods=['POST'])
def acessoCliente():
    email = request.form.get('emailCliente')
    senha = request.form.get('senhaCliente')
# -------------- uso do json como banco de dados caso nao use o mysql ----------------------------------------

    # with open('clientes.json') as cliente_json:
    #     listaDeClientes = json.load(cliente_json)
# --------------------------------------------------------------------------------------------------

    # abrindo bd e obtendo lista de usuarios
    clientes = executar_consulta("SELECT * FROM usuarios")


    cont = 0
    for usuario in clientes:
        cont += 1 
        
        if email == usuario[0]   and senha == usuario[2] :
            session['cliente'] = email
            if 'vendedor' in session:
                del session['vendedor']
            return redirect('/cliente')
        if cont >= len(clientes):
            flash('Email ou senha incorretos.')
            return redirect('/loginCliente')

# ------------------------------------------------------------------------------------------------

#--------------------- Pagina do Cliente ---------------------------------------------------------------

@app.route('/cliente')
def cliente():
    if 'cliente' in session:
        # Obtendo o email do cliente da sessão
        emailCliente = session['cliente']
        
        # Obtendo os dados do cliente
        dados_cliente = executar_consulta(f"SELECT * FROM usuarios WHERE email = '{emailCliente}'")
        
        # Obtendo o carrinho do cliente
        carrinho = executar_consulta(f"SELECT * FROM carrinho WHERE usuario_email = '{emailCliente}'")
        
        # Calculando o total_preco
        total_preco = sum(item[5] * item[7] for item in carrinho)
        
        # Atualizando o total_preco na tabela usuarios
        enviar_dados_bd(f"UPDATE usuarios SET total_preco = {total_preco} WHERE email = '{emailCliente}'")
        
        # Restante do código...
        vendedores = executar_consulta("SELECT * FROM vendedores")
        historico = executar_consulta("SELECT * FROM historico_compras")
        itens_historico = executar_consulta("SELECT * FROM itens_compra")
        for usuario in dados_cliente:
            if usuario[0] == session['cliente']:
                foto = usuario[3]
                nome = usuario[1]
                email = usuario[0]
                dados_cliente = usuario
                valor_pagar_vendedor = {}
                for produto in carrinho :
                    if produto[1] == email:
                        if produto[6] not in valor_pagar_vendedor:
                            valor_pagar_vendedor[produto[6]] = produto[5] * produto[7]
                        else:
                            valor_pagar_vendedor[produto[6]] += produto[5] * produto[7]

        # Restante do código...
        
        return render_template('cliente.html', vendedores=vendedores, historico=historico, itens_historico=itens_historico, valor_pagar_vendedor=valor_pagar_vendedor, dados_cliente=dados_cliente, foto=foto, nome=nome, email=email, carrinho=carrinho)
    
    else:
        flash('Necessario fazer login.')
        return redirect('/loginCliente')

# ---------------------------------------------------------------------------------------------------------------


#----------------------------  pagina do vendedor --------------------------------------------------------
@app.route("/vendedor")
def vendedor():
    if 'vendedor' in session:
        vendedores = executar_consulta("SELECT * FROM vendedores")
        produtos = executar_consulta("SELECT * FROM produtos_vendedor")
        for vendedor in vendedores:
            if vendedor[0] == session['vendedor']:
                foto = vendedor[4]
                nome = vendedor[1]
                email = vendedor[0]
                listaProduto = []
                for produto in produtos:
                    if produto[1] == email:
                        listaProduto.append(produto)
                print(listaProduto)
                return render_template('vendedor.html' , foto=foto, nome=nome, email=email, produtos=listaProduto)
    else:
        flash('Necessario fazer login.')
        return redirect('/loginVendedor')

#-------------------------------------------------------------------------------------------------------

#-----------------   pagina de cadastro de usuarios ------------------------------------------------

@app.route('/cadastrar')
def cadastrar():

    return render_template('cadastro.html')
#-------------------------------------------------------------------------------------------------------------



#------------------  rota para verificação de dados e cadastro de clientes-------------------------------
@app.route('/cadastroCliente', methods=['POST'])
def cadastroCliente():
    email = request.form.get('emailclienter')
    nome  = request.form.get('nomecliente')
    senha  = request.form.get('senhacliente')
    clientes = executar_consulta("SELECT * FROM usuarios")

    for usuario in clientes:
        if usuario[0] == email:
            flash('Email já cadastrado no banco de dados, se esqueceu sua senha clique em "esqueci minha senha".')
            return redirect('/loginCliente')
    
    enviar_dados_bd(f"INSERT INTO usuarios (email, nome, senha, foto, total_preco) VALUES ('{email}', '{nome}', '{senha}','', 0);")

    flash(f'{nome} cadastrado com sucesso!! BOAS COMPRAS!')
    return redirect('/loginCliente')
#-------------------------------------------------------------------------------------------------------------



#--------------------------------------area de cadastro de vendedores------------------------------------

@app.route('/cadastroVendedor' , methods=['POST'])
def cadastroVendedor():
    email = request.form.get('emailVendedor')
    nome = request.form.get('nomeVendedor')
    chavePIX = request.form.get('pixVendedor')
    senha = request.form.get('senhaVendedor')
    vendedores = executar_consulta("SELECT * FROM vendedores")


    for vendedor in vendedores:
        if vendedor[0] == email:
            flash('usuario ja cadastrado, tente fazer login ou clique em esqueci minha senha. ')
            return redirect('/loginVendedor')
    
    enviar_dados_bd(f"INSERT INTO vendedores (email, nome, senha, chavePIX, foto) VALUES ('{email}', '{nome}', '{senha}', '{chavePIX}', '');")

    flash(f'{nome} cadastrado com sucesso!! BOAS VENDAS!')
    return redirect('/loginVendedor')
#-------------------------------------------------------------------------------------------------------------
    

#-------------------------------  rota para envio de foto de perfil ------------------------------
@app.route('/enviarFoto', methods=['POST'])
def enviarFoto():
    foto = request.files.get('foto')
    emailUsuario = request.form.get('emailUsuario')
    rota = request.form.get('rota')

    nome_arquivo = f"Foto_perfil_{emailUsuario}.{foto.filename.split('.')[-1] }"
    foto.save(os.path.join('static/fotoperfil', nome_arquivo))
    if rota == '/cliente':
        clientes = executar_consulta("SELECT * FROM usuarios")


        for cliente in clientes:
            if cliente[0] == emailUsuario:
                enviar_dados_bd(f"UPDATE usuarios SET foto = '{nome_arquivo}' WHERE email = '{emailUsuario}'; ")

    else:
        vendedores = executar_consulta("SELECT * FROM vendedores")

        for vendedor in vendedores:
            if vendedor[0] == emailUsuario:
                enviar_dados_bd(f"UPDATE vendedores SET foto = '{nome_arquivo}' WHERE email = '{emailUsuario}'; ")


    return redirect(rota)
#-------------------------------------------------------------------------------------------------------------




#-----------------------------------  rota para envio de nova senha ---------------------------------
@app.route("/novaSenha", methods=['POST'])
def novaSenha():
    novasenha = request.form.get('novaSenha')
    emailUsuario = request.form.get('emailUsuario')
    

    if 'cliente' in session:
        clientes = executar_consulta("SELECT * FROM usuarios")
        for usuario in clientes:
            if usuario[0] == emailUsuario:
                enviar_dados_bd(f"UPDATE usuarios SET senha = '{novasenha}' WHERE email = '{emailUsuario}'; ")



        flash(f'Senha alterada com sucesso, a nova senha é {novasenha}')
        return redirect('/cliente')

    if 'vendedor' in session:

        vendedores = executar_consulta("SELECT * FROM vendedores")

        for usuario in vendedores:
            if usuario[0] == emailUsuario:
                enviar_dados_bd(f"UPDATE vendedores SET senha = '{novasenha}' WHERE email = '{emailUsuario}'; ")


        flash(f'Senha alterada com sucesso, a nova senha é {novasenha}')
        return redirect('/vendedor')
 #-------------------------------------------------------------------------------------------------------------



#--------------------------------  area para apagar conta de usuario  -----------------------------
@app.route('/apagar_conta', methods=['POST'])
def apagar_conta():
    emailUsuario = request.form.get("emailUsuario")

    if 'cliente' in session:

        clientes = executar_consulta("SELECT * FROM usuarios")
        ids_historico = executar_consulta(f"SELECT id FROM historico_compras WHERE usuario_email = '{emailUsuario}' ")
        for cliente in clientes:
            if cliente[0] == emailUsuario:
                # Deletar os registros do usuário na tabela "usuarios"
                
                enviar_dados_bd(f"DELETE FROM usuarios WHERE email = '{emailUsuario}'")

                # Deletar os registros do usuário na tabela "carrinho"
                
                enviar_dados_bd(f"DELETE FROM carrinho WHERE usuario_email = '{emailUsuario}'")

                # Deletar os registros do usuário na tabela "historico_compras" e "itens_compra"
                
                enviar_dados_bd(f"DELETE FROM historico_compras WHERE usuario_email = '{emailUsuario}'")

                for id in ids_historico:

                    enviar_dados_bd(f"DELETE FROM itens_compra WHERE historico_id   = '{id[0]}'")

                del session['cliente']


    if 'vendedor' in session:
        enviar_dados_bd(f"DELETE FROM vendedores WHERE email = '{emailUsuario}'")

        imagemProduto = executar_consulta(f"SELECT imagem FROM produtos_vendedor WHERE vendedor_email = '{emailUsuario}' ")
        for imagem in imagemProduto:
            os.remove(os.path.join('static/produtos', imagem[0]))

        enviar_dados_bd(f"DELETE FROM produtos_vendedor WHERE vendedor_email = '{emailUsuario}'") 

        del session['vendedor']



    return redirect('/')
#-------------------------------------------------------------------------------------------------------------


#---------------     area para envio de produto para venda   -----------------------------------------------

@app.route("/novo_produto", methods=['POST'])
def novo_produto():

    foto = request.files.get("foto")
    nome_produto = request.form.get("nome")
    preco = request.form.get("preco")
    descricao = request.form.get("descricao")
    emailUsuario =  request.form.get("emailUsuario")
    preco = float(preco)

    
    nome_arquivo = f"foto_produto{emailUsuario}_{nome_produto}.{foto.filename.split('.')[-1]}"
    foto.save(os.path.join('static/produtos', nome_arquivo))

    enviar_dados_bd(f"INSERT INTO produtos_vendedor (vendedor_email, produto, imagem, descricao, preco, quantidade_vendida) VALUES ('{emailUsuario}', '{nome_produto}', '{nome_arquivo}', '{descricao}', {preco}, 0); ")


    return redirect('/vendedor')

#-------------------------------------------------------------------------------------------------------------





#---------------------------------------   area para edição de dados do produtos para venda-----------------------

@app.route('/editar_produto', methods=['POST'])
def editar_produto():
    nome = request.form.get('editar_nome')
    preco = request.form.get('editar_preco')
    descricao = request.form.get('editar_descricao')
    emailUsuario = request.form.get('emailUsuario')
    nomeAntigo = request.form.get('nomeAntigo')
    preco = float(preco)
    id_produto = request.form.get('id_produto')



    enviar_dados_bd(f"UPDATE produtos_vendedor SET produto = '{nome}', descricao = '{descricao}', preco = {preco} WHERE id = '{id_produto}';")


    return redirect('/vendedor')


# ---------------------------------------------------------------------------------------

# ----------------------------excluir produto-----------------------------------------------------------

@app.route('/excluir_produto', methods=['POST'])
def excluir_produto():
    nomeProduto = request.form.get('nomeProduto')
    emailUsuario = request.form.get('emailUsuario')
    id_produto = request.form.get('id_produto')

    

    imagemProduto = executar_consulta(f"SELECT imagem FROM produtos_vendedor WHERE id = {id_produto};")
    for imagem in imagemProduto:
        os.remove(os.path.join('static/produtos', imagem[0]))
    enviar_dados_bd(f"DELETE FROM produtos_vendedor WHERE  id = {id_produto};")

    
    return redirect('/vendedor')

# ---------------------------------------------------------------------------------------




# --------------------------adicionar no carrinho-------------------------------------------------------------


@app.route('/adicionarCarrinho', methods=['POST'])
def adicionar_carrinho():
    nome_produto = request.form.get('nome_produto')
    imagem_produto = request.form.get('imagem_produto')
    preco_produto = float(request.form.get('preco_produto'))
    descricao_produto = request.form.get('descricao_produto')
    email_vendedor = request.form.get('email_vendedor')
    pagina_retorno = request.form.get('pagina_retorno')
    id_produto = request.form.get('id_produto')
    email_usuario = request.form.get('email_usuario')
  
    # Verificar se o produto já está no carrinho
    resultado = executar_consulta(f"SELECT id, quantidade FROM carrinho WHERE usuario_email = '{email_usuario}' AND produto = '{nome_produto}'")
    if resultado:
        carrinho_id = resultado[0][0]
        quantidade_atual = resultado[0][1]
        nova_quantidade = quantidade_atual + 1
        # Atualizar a quantidade do produto no carrinho
        enviar_dados_bd(f"UPDATE carrinho SET quantidade = {nova_quantidade} WHERE id = {carrinho_id}")
    else:
        # Inserir um novo registro no carrinho
        enviar_dados_bd(f"INSERT INTO carrinho (usuario_email, produto, imagem, descricao, preco, email_vendedor, quantidade) VALUES ('{email_usuario}', '{nome_produto}', '{imagem_produto}', '{descricao_produto}', {preco_produto}, '{email_vendedor}', 1)")
  
    return redirect(pagina_retorno)

# ---------------------------------------------------------------------------------------


# -----------------------remover do carrinho----------------------------------------------------------------
@app.route('/remover_carrinho', methods=['POST'])
def remover_carrinho():
    nome_produto = request.form.get('nome_produto')
    pagina_retorno = request.form.get('pagina_retorno')
    email_usuario = session['cliente']

    # Consultar o item no carrinho do usuário no banco de dados
    item_carrinho = executar_consulta(f"SELECT * FROM carrinho WHERE usuario_email = '{email_usuario}' AND produto = '{nome_produto}'")

    if item_carrinho:
        quantidade = item_carrinho[0][7]  # Quantidade do item no carrinho
        if quantidade > 1:
            # Se a quantidade for maior que 1, decrementar a quantidade
            enviar_dados_bd(f"UPDATE carrinho SET quantidade = quantidade - 1 WHERE usuario_email = '{email_usuario}' AND produto = '{nome_produto}'")
        else:
            # Se a quantidade for 1, remover completamente o item do carrinho
            enviar_dados_bd(f"DELETE FROM carrinho WHERE usuario_email = '{email_usuario}' AND produto = '{nome_produto}'")

    return redirect(pagina_retorno)


# ---------------------------------------------------------------------------------------

#------------- finalização de compra --------------------------------------
# @app.route('/finalizar_compra', methods=['POST'])
# def finalizar_compra():
#     emailUsuario = request.form.get('emailUsuario')
#     with open('clientes.json') as cliente_json:
#         listaClientes = json.load(cliente_json)
#         for cliente in listaClientes:
#             if cliente['email'] == emailUsuario:
#                 if len(cliente['historico']) > 0:
#                     novo = [{
#                         "compras_finalizadas": cliente['carrinho'],
#                         "compra_feita_em": datetime.today().strftime("%d-%m-%y %H:%M:%S")
#                     }]
#                     cliente['historico'] = novo +  cliente['historico']
#                 else:
#                     cliente['historico'] = [{
#                         "compras_finalizadas": cliente['carrinho'],
#                         "compra_feita_em": datetime.today().strftime("%d-%m-%y %H:%M:%S")
#                     }]
#                 with open('vendedor.json') as vendedor_json:
#                     listaVendedores = json.load(vendedor_json)
#                     for vendedor in listaVendedores:
#                         for nome_produto, dados in cliente['carrinho'].items():
#                             if dados['email_vendedor'] == vendedor['email']:
#                                 vendedor['produtos'][nome_produto]['quantidade_vendida'] += dados['quantidade']
#                 cliente['carrinho'] = {}
#                 cliente['total_preco'] = 0.0

#                 with open('clientes.json', 'w') as cliente_json:
#                     json.dump(listaClientes, cliente_json, indent=4)
#                 with open('vendedor.json', 'w') as vendedor_novo:
#                     json.dump(listaVendedores, vendedor_novo, indent=4)




#     return redirect('/cliente')



from datetime import datetime

@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    emailUsuario = request.form.get('emailUsuario')
    
    # Obter o carrinho do cliente
    carrinho = executar_consulta(f"SELECT * FROM carrinho WHERE usuario_email = '{emailUsuario}'")
    
    # Verificar se o carrinho não está vazio
    if len(carrinho) > 0:
        # Inserir uma nova entrada no histórico de compras
        dataCompra = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        enviar_dados_bd(f"INSERT INTO historico_compras (usuario_email, compra_feita_em) VALUES ('{emailUsuario}', '{dataCompra}')")
        
        # Obter o ID da última compra feita pelo cliente
        idCompra = executar_consulta("SELECT LAST_INSERT_ID()")[0][0]
        
        # Atualizar a quantidade vendida dos produtos do vendedor
        for item in carrinho:
            produto = item[2]
            quantidade = item[7]
            emailVendedor = item[6]
            
            enviar_dados_bd(f"UPDATE produtos_vendedor SET quantidade_vendida = quantidade_vendida + {quantidade} WHERE vendedor_email = '{emailVendedor}' AND produto = '{produto}'")
        
        # Inserir os itens da compra no banco de dados
        for item in carrinho:
            produto = item[2]
            imagem = item[3]
            descricao = item[4]
            preco = item[5]
            emailVendedor = item[6]
            quantidade = item[7]
            
            enviar_dados_bd(f"INSERT INTO itens_compra (historico_id, produto, imagem, descricao, preco, email_vendedor, quantidade) VALUES ({idCompra}, '{produto}', '{imagem}', '{descricao}', {preco}, '{emailVendedor}', {quantidade})")
        
        # Limpar o carrinho do cliente
        enviar_dados_bd(f"DELETE FROM carrinho WHERE usuario_email = '{emailUsuario}'")
    
    return redirect('/cliente')


#-----------------------------------------------------------------------------

#---------------------------- esqueceu a senha e envio de email -----------------------------

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


    
    



#-----------------------------------------------------------------------------------------------------------







if __name__ in '__main__':
    app.run( debug=True )