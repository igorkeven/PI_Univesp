


// codigo para fazer aparecer o modal de confirmação de apagar a conta
const apagarContaButton = document.querySelector('.apagar_conta');
const modalApagarConta = document.querySelector('#modal_apagarConta');
const cancelarButton = document.querySelector('#cancelarApagarConta');

apagarContaButton.addEventListener('click', () => {
  modalApagarConta.style.display = "block";
});

cancelarButton.addEventListener('click', () => {
  modalApagarConta.style.display = "none";
});






// codigo para verificar se a nova senha e a repetição são iguis 
const formMudarSenha = document.querySelector("#formMudarSenha");
const novaSenha = document.querySelector("#novaSenha");
const repetirNovaSenha = document.querySelector("#repetirNovaSenha");
const mensagemErroSenha = document.querySelector("#mensagemErroSenha");

formMudarSenha.addEventListener("submit", (event) => {
  if (novaSenha.value !== repetirNovaSenha.value) {
    mensagemErroSenha.textContent = "As senhas não são iguais.";
    event.preventDefault();
  }
});






  // codigo do botão para cancelar a edição do produto
var botaoCancelar = document.querySelectorAll("#cancelar-edicao");
botaoCancelar.forEach(function(botao){
  botao.addEventListener('click',function(){
    document.querySelector('#produtos').style.display = 'block';
      document.querySelector('#editar-produto').style.display = 'none';
      titulo.textContent = "Meus Produtos";

});
} ) 
  

  
  // Seleciona todos os botões "Editar"
  var botoesEditar = document.querySelectorAll('#Editar');
  
  // Adiciona um evento de clique para cada botão "Editar"
  botoesEditar.forEach(function(botao) {
    botao.addEventListener('click', function() {
      // Obtém a imagem do produto correspondente ao botão "Editar" clicado

        

      // Obtém os dados do produto selecionado
      var produto = botao.parentNode.querySelector('h2').textContent;
      var preco = botao.parentNode.querySelector('p:nth-child(4)').textContent.replace('Preço: R$ ', '');
      var descricao = botao.parentNode.querySelector('p:nth-child(3)').textContent;
      //var imagem = $(this).siblings("img").attr("src");
      var imagem = botao.parentNode.querySelector('img').src;

      //$("#imagem-produto").attr("src", imagem);
      // Preenche os campos do formulário de edição com os dados do produto
      document.querySelector('#editar_nome').value = produto;
      document.querySelector('#editar_preco').value = preco;
      document.querySelector('#editar_descricao').value = descricao;
      document.querySelector('#nomeAntigo').value = produto;
      document.querySelector('#imagem-produto').setAttribute('src', imagem);

      // Oculta a lista de produtos e mostra o formulário de edição
      document.querySelector('#produtos').style.display = 'none';
      document.querySelector('#editar-produto').style.display = 'block';
      titulo.textContent = "Editar Produto";
      
    });
  });






// codigo para mostrar ou escolher o formulario escolhido
const btnEnviarProdutos = document.querySelector("#escolha_formulario_produtos");
const divProdutos = document.querySelector("#produtos");
const divFormularioProdutos = document.querySelector("#formulario_produtos");
const editar = document.querySelector("#editar-produto");
const titulo = document.querySelector("#titulo")
const btnMudarSenha = document.querySelector("#escolha_formulario_senha");
const divFormularioSenha = document.querySelector("#formulario_senha");
const btnPedidos = document.querySelector("#meus_pedidos");


btnMudarSenha.addEventListener("click", () => {
  divFormularioSenha.style.display = 'flex';
  divProdutos.style.display = "none";
  divFormularioProdutos.style.display = "none";
  editar.style.display = 'none';
  titulo.textContent = "Mudar Senha";
  
})






btnEnviarProdutos.addEventListener("click", () => {
 
  if (divProdutos.style.display !== "none") {
    // produtos está visível, então esconda-o e mostre o formulário
    divProdutos.style.display = "none";
    divFormularioSenha.style.display = 'none';
    divFormularioProdutos.style.display = "flex";
    btnEnviarProdutos.textContent = "Meus produtos";
    titulo.textContent = "Enviar Produtos";
  } else {
    // produtos está escondido, então mostre-o e esconda o formulário
    divProdutos.style.display = "block";
    divFormularioProdutos.style.display = "none";
    editar.style.display = 'none';
    divFormularioSenha.style.display = 'none';
    btnEnviarProdutos.textContent = "Enviar produtos";
    titulo.textContent = "Meus Produtos";
  }
});







// codigo para aparecer o modal de envio de foto do perfil
document.getElementById("foto-artesao").addEventListener("click", function() {
  if (this.src.includes("usuario.png")) {
    // Usuário ainda não tem uma imagem definida, permitir a mudança da imagem sem alerta
  } else {
    // Usuário já tem uma imagem definida, solicitar confirmação antes de permitir a mudança da imagem
    if (confirm("Você tem certeza que deseja mudar sua foto?")) {
      // Usuário confirmou a mudança da foto
    } else {
      // Usuário cancelou a mudança da foto
      return;
    }
  }
  var modal = document.createElement("div");
  modal.classList.add("modal");
  modal.innerHTML = `
    <div class="modal-content">
      <span class="close">&times;</span>
      <form action="/enviar_foto" method="post" enctype="multipart/form-data">
        <input type="file" name="foto" id="foto">
        <input type="hidden" name="dadosUsuario" value="{{artesao}}" >
        <input type="hidden" name="retornoRota" value="/artesao" >
        
        <input type="submit" value="Enviar">
      </form>
    </div>
  `;
  document.body.appendChild(modal);
  
  var closeButton = modal.querySelector(".close");
  closeButton.addEventListener("click", function() {
    modal.remove();
  });
});
