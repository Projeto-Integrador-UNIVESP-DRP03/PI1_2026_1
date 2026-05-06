/**
 * Sistema de Modais Reutilizável
 * Gerencia abertura, fechamento e interações de modais
 */

class ModalManager {
    constructor() {
        this.currentModal = null;
        this.setupEventListeners();
    }

    /**
     * Configura eventos globais
     */
    setupEventListeners() {
        // Fechar modal ao clicar no overlay
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-overlay') && e.target.classList.contains('active')) {
                this.closeModal(e.target);
            }
        });

        // Fechar modal com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.currentModal) {
                this.closeModal(this.currentModal);
            }
        });

        // Botão de cancelar
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-btn-cancel')) {
                const overlay = e.target.closest('.modal-overlay');
                this.closeModal(overlay);
            }
        });
    }

    /**
     * Abre um modal
     * @param {string} modalId - ID do modal a abrir
     */
    openModal(modalId) {
        const overlay = document.getElementById(modalId);
        if (overlay) {
            overlay.classList.add('active');
            this.currentModal = overlay;
            document.body.style.overflow = 'hidden';
        }
    }

    /**
     * Fecha um modal
     * @param {HTMLElement} overlay - Elemento overlay do modal
     */
    closeModal(overlay) {
        if (overlay) {
            // Optional hook for callers that need to revert UI state when a modal is closed
            // without confirmation (e.g. a status dropdown that was changed).
            try {
                if (typeof overlay.__onClose === 'function') {
                    overlay.__onClose();
                }
            } catch (err) {
                console.error('Erro ao executar hook de fechamento do modal:', err);
            } finally {
                overlay.__onClose = null;
                overlay.__confirmed = false;
            }

            overlay.classList.remove('active');
            this.currentModal = null;
            document.body.style.overflow = '';
        }
    }

    /**
     * Abre modal de confirmação de exclusão
     * @param {string} tipo - Tipo de exclusão ('cliente', 'veiculo')
     * @param {string} nome - Nome do item a excluir
     * @param {function} callback - Função a executar após confirmação
     */
    confirmDelete(tipo, nome, callback) {
        const modalId = `modal-delete-${tipo}`;
        const modal = document.getElementById(modalId);
        
        if (!modal) {
            console.error(`Modal ${modalId} não encontrado`);
            return;
        }

        // Atualiza o nome no modal
        const nomeElement = modal.querySelector('.modal-delete-name');
        if (nomeElement) {
            nomeElement.textContent = nome;
        }

        // Configura botão de confirmação
        const confirmBtn = modal.querySelector('.modal-btn-confirm');
        confirmBtn.onclick = callback;

        this.openModal(modalId);
    }

    /**
     * Abre modal de aprovação/recusa de orçamento
     * @param {string} orcamentoId - ID do orçamento
     * @param {string} cliente - Nome do cliente
     * @param {function} onApprove - Função para aprovar
     * @param {function} onReject - Função para recusar
     */
    confirmBudget(orcamentoId, cliente, onApprove, onReject) {
        const modalId = 'modal-budget-decision';
        const modal = document.getElementById(modalId);
        
        if (!modal) {
            console.error(`Modal ${modalId} não encontrado`);
            return;
        }

        // Atualiza o cliente no modal
        const clienteElement = modal.querySelector('.modal-budget-client');
        if (clienteElement) {
            clienteElement.textContent = cliente;
        }

        // Configura botões
        const approveBtn = modal.querySelector('.modal-btn-approve');
        const rejectBtn = modal.querySelector('.modal-btn-reject');

        approveBtn.onclick = onApprove;
        rejectBtn.onclick = onReject;

        this.openModal(modalId);
    }

    /**
     * Mostra um modal de informação
     * @param {string} titulo - Título do modal
     * @param {string} mensagem - Mensagem a exibir
     * @param {string} tipo - Tipo ('success', 'error', 'warning', 'info')
     */
    showInfo(titulo, mensagem, tipo = 'info') {
        const modalId = 'modal-info';
        const modal = document.getElementById(modalId);
        
        if (!modal) {
            console.error(`Modal ${modalId} não encontrado`);
            return;
        }

        // Atualiza conteúdo
        const headerContent = modal.querySelector('.modal-header-content');
        const body = modal.querySelector('.modal-body');
        const icon = modal.querySelector('.modal-icon');

        headerContent.innerHTML = `<h2>${titulo}</h2>`;
        body.innerHTML = `<p>${mensagem}</p>`;

        // Atualiza ícone
        icon.className = `modal-icon ${tipo}`;
        const iconMap = {
            'success': '<i class="fas fa-check-circle"></i>',
            'error': '<i class="fas fa-exclamation-circle"></i>',
            'warning': '<i class="fas fa-exclamation-triangle"></i>',
            'info': '<i class="fas fa-info-circle"></i>'
        };
        icon.innerHTML = iconMap[tipo] || iconMap['info'];

        this.openModal(modalId);
    }
}

// Instancia o gerenciador de modais globalmente
const modalManager = new ModalManager();

/**
 * Função auxiliar para abrir modal de exclusão
 */
function openDeleteModal(tipo, nome, formId) {
    const modal = document.getElementById(`modal-delete-${tipo}`);
    if (!modal) return;

    const nomeElement = modal.querySelector('.modal-delete-name');
    if (nomeElement) {
        nomeElement.textContent = nome;
    }

    const confirmBtn = modal.querySelector('.modal-btn-confirm');
    confirmBtn.onclick = () => {
        const form = document.getElementById(formId);
        if (form) form.submit();
        modalManager.closeModal(modal.parentElement);
    };

    modalManager.openModal(`modal-delete-${tipo}`);
}

/**
 * Função auxiliar para abrir modal de aprovação de orçamento
 */
function openApproveBudgetModal(orcamentoId, cliente) {
    openApproveStyleConfirmModal({
        title: 'Aprovar Orçamento',
        subtitleHtml: `Cliente: <strong class="modal-budget-client">${escapeHtml(cliente)}</strong>`,
        bodyHtml: `
            <p>Confirmar aprovação deste orçamento?</p>
            <p style="margin-top: 1rem; font-size: 0.875rem; color: #10b981;">
                <i class="fas fa-info-circle"></i> O orçamento será enviado para a lista de pedidos.
            </p>
        `,
        confirmHtml: '<i class="fas fa-check-circle"></i> Aprovar',
        onConfirm: () => {
            const form = document.getElementById(`form-approve-${orcamentoId}`);
            if (form) form.submit();
        }
    });
}

/**
 * Função auxiliar para abrir modal de recusa de orçamento
 */
function openRejectBudgetModal(orcamentoId, cliente) {
    const modal = document.getElementById('modal-reject-budget');
    if (!modal) return;

    const clienteElement = modal.querySelector('.modal-budget-client');
    if (clienteElement) {
        clienteElement.textContent = cliente;
    }

    const rejectBtn = modal.querySelector('.modal-btn-reject');
    rejectBtn.onclick = () => {
        const form = document.getElementById(`form-reject-${orcamentoId}`);
        if (form) form.submit();
    };

    modalManager.openModal('modal-reject-budget');
}

function escapeHtml(value) {
    return (value || '')
        .toString()
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/**
 * Reusa o modal "Aprovar Orçamento" como um confirm genérico (mesmo visual).
 * @param {Object} opts
 * @param {string} opts.title
 * @param {string} opts.subtitleHtml
 * @param {string} opts.bodyHtml
 * @param {string} opts.confirmHtml
 * @param {Function} opts.onConfirm
 * @param {Function} [opts.onCancel] - Executa quando o modal fechar sem confirmar (Cancelar/ESC/clicar fora)
 */
function openApproveStyleConfirmModal(opts) {
    const modalId = 'modal-approve-budget';
    const modal = document.getElementById(modalId);
    if (!modal) return;

    const icon = modal.querySelector('.modal-icon');
    if (icon) {
        icon.className = 'modal-icon success';
        icon.innerHTML = '<i class="fas fa-check-circle"></i>';
    }

    const titleEl = modal.querySelector('.modal-header-content h2');
    if (titleEl) titleEl.textContent = opts.title || 'Confirmar';

    const subtitleEl = modal.querySelector('.modal-header-content p');
    if (subtitleEl) {
        if (opts.subtitleHtml) {
            subtitleEl.style.display = '';
            subtitleEl.innerHTML = opts.subtitleHtml;
        } else {
            subtitleEl.style.display = 'none';
            subtitleEl.innerHTML = '';
        }
    }

    const body = modal.querySelector('.modal-body');
    if (body) body.innerHTML = opts.bodyHtml || '<p>Confirmar ação?</p>';

    const approveBtn = modal.querySelector('.modal-btn-approve');
    if (approveBtn) {
        approveBtn.innerHTML = opts.confirmHtml || '<i class="fas fa-check-circle"></i> Confirmar';
        approveBtn.onclick = () => {
            modal.__confirmed = true;
            modalManager.closeModal(modal);
            if (typeof opts.onConfirm === 'function') opts.onConfirm();
        };
    }

    modal.__confirmed = false;
    modal.__onClose = () => {
        if (!modal.__confirmed && typeof opts.onCancel === 'function') {
            opts.onCancel();
        }
    };

    modalManager.openModal(modalId);
}
