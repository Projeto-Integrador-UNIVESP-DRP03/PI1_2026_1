# Sistema de Modais - Documentação

## Visão Geral

O sistema de modais foi implementado para substituir os alertas nativos do navegador (`confirm()`) por uma interface mais elegante e intuitiva, alinhada com o design do aplicativo.

## Componentes Inclusos

### 1. **Modal de Exclusão de Cliente**
- **ID**: `modal-delete-cliente`
- **Ícone**: Lixeira vermelha
- **Cor**: Vermelho (#ef4444)
- **Ação**: Confirmação antes de deletar um cliente
- **Função**: `openDeleteModal('cliente', nome, formId)`

### 2. **Modal de Exclusão de Veículo**
- **ID**: `modal-delete-veiculo`
- **Ícone**: Carro acidentado
- **Cor**: Vermelho (#ef4444)
- **Ação**: Confirmação antes de deletar um veículo
- **Função**: `openDeleteModal('veiculo', nome, formId)`

### 3. **Modal de Aprovação/Recusa de Orçamento**
- **ID**: `modal-budget-decision`
- **Ícone**: Documento com cifrão (azul)
- **Cores**: Azul para informação, verde para aprovação, laranja para recusa
- **Ações**: Aprovar ou recusar um orçamento
- **Funções**: 
  - `openBudgetModal(orcamentoId, cliente)`
  - `openRejectBudgetModal(orcamentoId, cliente)`

## Como Usar

### Para Exclusão

```html
<!-- Criar um formulário oculto com ID único -->
<form id="form-delete-cliente-{{ id }}" action="/deletar" method="post" style="display: none;"></form>

<!-- Criar botão que chama a função -->
<button type="button" class="icon-btn" 
        onclick="openDeleteModal('cliente', '{{ nome }}', 'form-delete-cliente-{{ id }}')">
    <i class="fas fa-trash-alt"></i>
</button>
```

### Para Orçamentos

```html
<!-- Criar formulários ocultos para aprovação e recusa -->
<form id="form-approve-{{ id }}" method="POST" action="/aprovar" style="display: none;"></form>
<form id="form-reject-{{ id }}" method="POST" action="/recusar" style="display: none;"></form>

<!-- Criar botões que chamam as funções -->
<button type="button" class="icon-btn" 
        onclick="openBudgetModal('{{ id }}', '{{ cliente }}')">
    <i class="fas fa-check"></i>
</button>

<button type="button" class="icon-btn" 
        onclick="openRejectBudgetModal('{{ id }}', '{{ cliente }}')">
    <i class="fas fa-times"></i>
</button>
```

## Arquivos Modificados

1. **`templates/base.html`**
   - Adicionados os 3 modais reutilizáveis
   - Importado `static/js/modal.js`

2. **`static/css/estilo.css`**
   - Adicionados estilos para:
     - `.modal-overlay` (fundo escuro com animação)
     - `.modal-container` (container do modal)
     - `.modal-header` (cabeçalho com ícone)
     - `.modal-body` (corpo do modal)
     - `.modal-footer` (rodapé com botões)
     - `.modal-btn-*` (estilos dos botões)

3. **`static/js/modal.js`** (novo arquivo)
   - Classe `ModalManager` para gerenciar modais
   - Função `openDeleteModal()` para exclusões
   - Função `openBudgetModal()` para aprovação
   - Função `openRejectBudgetModal()` para recusa

4. **`templates/lista_clientes.html`**
   - Substituído `confirm()` por `openDeleteModal()` para clientes
   - Substituído `confirm()` por `openDeleteModal()` para veículos

5. **`templates/lista_orcamentos.html`**
   - Substituído `confirm()` por `openBudgetModal()` e `openRejectBudgetModal()`

## Funcionalidades

### Navegação
- ✅ Clicar fora do modal fecha
- ✅ Tecla ESC fecha o modal
- ✅ Botão "Cancelar" fecha o modal
- ✅ Overlay escuro com efeito blur

### Animações
- ✅ Fade-in do overlay
- ✅ Slide-up do container
- ✅ Hover effects nos botões
- ✅ Transform ao passar o mouse

### Design
- ✅ Alinhado com o design do aplicativo
- ✅ Usa cores definidas em `:root`
- ✅ Responsive em mobile
- ✅ Box shadows elegantes
- ✅ Transições suaves

## Cores Utilizadas

- **Perigo (Exclusão)**: #ef4444 (Vermelho)
- **Aviso (Recusa)**: #f59e0b (Laranja)
- **Sucesso (Aprovação)**: #10b981 (Verde)
- **Info (Orçamento)**: #3b82f6 (Azul)

## Integrações Futuras

Para adicionar novos modais, siga o padrão:

1. Crie um div com `class="modal-overlay"` e um `id` único
2. Estruture o conteúdo seguindo o layout do header/body/footer
3. Crie uma função auxiliar chamando `modalManager.openModal(id)`
4. Implemente os event listeners nos botões

## Troubleshooting

### Modal não abre
- Verifique se o ID do modal está correto
- Verifique se o `modal.js` foi carregado
- Abra o console do navegador para erros

### Formulário não envia
- Verifique se o formulário oculto tem um ID válido
- Verifique se o ID é passado corretamente para a função
- Teste manualmente o envio do formulário

### Estilos não aparecem
- Verifique se `estilo.css` foi atualizado
- Limpe o cache do navegador (Ctrl+Shift+Delete)
- Verifique no DevTools se os estilos estão sendo aplicados
