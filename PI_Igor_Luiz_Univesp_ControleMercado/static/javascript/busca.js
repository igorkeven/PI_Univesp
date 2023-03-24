// Obtemos a lista de produtos
const produtos = document.querySelectorAll('.produto');

// Obtemos o campo de busca
const campoBusca = document.querySelector('#campo-busca');

// Adicionamos um evento de input ao campo de busca
campoBusca.addEventListener('input', () => {
  // Obtemos o valor do campo de busca e convertemos para minúsculas
  const valorBusca = campoBusca.value.toLowerCase();

  // Iteramos sobre a lista de produtos e exibimos apenas aqueles que correspondem à busca
  produtos.forEach((produto) => {
    const titulo = produto.querySelector('h3').textContent.toLowerCase();
    const descricao = produto.querySelector('p').textContent.toLowerCase();
    
    if (titulo.includes(valorBusca) || descricao.includes(valorBusca)) {
      produto.style.display = 'block';
    } else {
      produto.style.display = 'none';
    }
  });
});



