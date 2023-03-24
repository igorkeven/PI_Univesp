var produtos = [
    {
      nome: "Produto 1",
      descricao: "Descrição do Produto 1",
      preco: 10.00,
      imagem: "{{ url_for('static', filename='arquivos/produto1.jpg') }}"
    },
    {
      nome: "Produto 2",
      descricao: "Descrição do Produto 2",
      preco: 20.00,
      imagem: "{{ url_for('static', filename='arquivos/produto2.jpg') }}"
    },
    {
      nome: "Produto 3",
      descricao: "Descrição do Produto 3",
      preco: 30.00,
      imagem: "{{ url_for('static', filename='arquivos/produto3.jpg') }}"
    }
  ];
  


  function exibirProdutos() {
    // Seleciona o elemento onde os produtos serão exibidos
    var container = document.getElementById("produtos");
    
    // Limpa o conteúdo atual
    container.innerHTML = "";
    
    // Loop através da lista de produtos
    for (var i = 0; i < produtos.length; i++) {
      // Cria um elemento HTML para o produto
      var produtoElement = document.createElement("div");
      produtoElement.className = "produto";
      
      // Cria um elemento HTML para a imagem do produto
      var imagemElement = document.createElement("img");
      imagemElement.src = produtos[i].imagem;
      imagemElement.alt = produtos[i].nome;
      
      // Cria um elemento HTML para o nome do produto
      var nomeElement = document.createElement("h3");
      nomeElement.innerHTML = produtos[i].nome;
      
      // Cria um elemento HTML para a descrição do produto
      var descricaoElement = document.createElement("p");
      descricaoElement.innerHTML = produtos[i].descricao;
      
      // Cria um elemento HTML para o preço do produto
      var precoElement = document.createElement("p");
      precoElement.innerHTML = "R$ " + produtos[i].preco.toFixed(2);
      
      // Cria um elemento HTML para o botão de adicionar ao carrinho
      var botaoElement = document.createElement("button");
      botaoElement.className = "botao-adicionar";
      botaoElement.innerHTML = "Adicionar ao Carrinho";
      
      // Adiciona os elementos HTML criados ao elemento do produto
      produtoElement.appendChild(imagemElement);
      produtoElement.appendChild(nomeElement);
      produtoElement.appendChild(descricaoElement);
      produtoElement.appendChild(precoElement);
      produtoElement.appendChild(botaoElement);
      
      // Adiciona o elemento do produto ao container
      container.appendChild(produtoElement);
    }
  }
  



  window.onload = function() {
    exibirProdutos();
  };
  



  var carrinho = {
    itens: [],
    
    adicionarItem: function(produto) {
      // Verifica se o produto já está no carrinho
      for (var i = 0; i < this.itens.length; i++) {
        if (this.itens[i].produto === produto) {
          // Se o produto já está no carrinho, aumenta a quantidade
          this.itens[i].quantidade++;
          return;
        }
      }
      
      // Se o produto não está no carrinho, adiciona um novo item
      this.itens.push({
        produto: produto,
        quantidade: 1
      });
    },
    
    removerItem: function(index) {
      this.itens.splice(index, 1);
    },
    
    calcularTotal: function() {
      var total = 0;
      
      for (var i = 0; i < this.itens.length; i++) {
        total += this.itens[i].produto.preco * this.itens[i].quantidade;
      }
      
      return total;
    }
  };

  

  function adicionarAoCarrinho(event) {
    // Obtém o índice do produto na lista
    var index = event.target.getAttribute("data-index");
    
    // Adiciona o produto ao carrinho
    carrinho.adicionarItem(produtos[index]);
    
    // Exibe uma mensagem de confirmação
    alert("Produto adicionado ao carrinho!");
  }

  

  function exibirProdutos() {
    // Seleciona o elemento onde os produtos serão exibidos
    var container = document.getElementById("produtos-container");
    
    // Limpa o conteúdo atual
    container.innerHTML = "";
    
    // Loop através da lista de produtos
    for (var i = 0; i < produtos.length; i++) {
      // Cria um elemento HTML para o produto
      var produtoElement = document.createElement("div");
      produtoElement.className = "produto";
      
      // Cria um elemento HTML para a imagem do produto
      var imagemElement = document.createElement("img");
      imagemElement.src = produtos[i].imagem;
      imagemElement.alt = produtos[i].nome;
      
      // Cria um elemento HTML para o nome do produto
      var nomeElement = document.createElement("h3");
      nomeElement.innerHTML = produtos[i].nome;
      
      // Cria um elemento HTML para a descrição do produto
      var descricaoElement = document.createElement("p");
      descricaoElement.innerHTML = produtos[i].descricao;
      
      // Cria um elemento HTML para o preço do produto
      var precoElement = document.createElement("p");
      precoElement.innerHTML = "R$ " + produtos[i].preco.toFixed(2);
      
     
  // Cria um elemento HTML para o botão "Adicionar ao Carrinho"
  var adicionarElement = document.createElement("button");
  adicionarElement.innerHTML = "Adicionar ao Carrinho";
  adicionarElement.setAttribute("data-index", i);
  adicionarElement.addEventListener("click", adicionarAoCarrinho);
  
  // Adiciona os elementos HTML ao produto
  produtoElement.appendChild(imagemElement);
  produtoElement.appendChild(nomeElement);
  produtoElement.appendChild(descricaoElement);
  produtoElement.appendChild(precoElement);
  produtoElement.appendChild(adicionarElement);
  
  // Adiciona o produto ao container
  container.appendChild(produtoElement);
}
}



function exibirCarrinho() {
    // Seleciona o elemento onde o carrinho será exibido
    var container = document.getElementById("carrinho-container");
    
    // Limpa o conteúdo atual
    container.innerHTML = "";
    
    // Cria um elemento HTML para a lista de itens
    var listaElement = document.createElement("ul");
    
    // Loop através da lista de itens no carrinho
    for (var i = 0; i < carrinho.itens.length; i++) {
      // Cria um elemento HTML para o item
      var itemElement = document.createElement("li");
      
      // Cria um elemento HTML para o nome do produto
      var nomeElement = document.createElement("span");
      nomeElement.innerHTML = carrinho.itens[i].produto.nome;
      
      // Cria um elemento HTML para a quantidade do produto
      var quantidadeElement = document.createElement("span");
      quantidadeElement.innerHTML = "x " + carrinho.itens[i].quantidade;
      
      // Adiciona os elementos HTML ao item
      itemElement.appendChild(nomeElement);
      itemElement.appendChild(quantidadeElement);
      
      // Adiciona o item à lista
      listaElement.appendChild(itemElement);
    }
    
    // Cria um elemento HTML para o total
    var totalElement = document.createElement("p");
    totalElement.innerHTML = "Total: R$ " + carrinho.calcularTotal().toFixed(2);
    
    // Adiciona os elementos HTML ao container
    container.appendChild(listaElement);
    container.appendChild(totalElement);
  }
  