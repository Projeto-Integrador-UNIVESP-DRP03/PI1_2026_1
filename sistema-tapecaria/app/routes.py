from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Cliente, TelefoneCliente, EnderecoCliente, Veiculo, Tecido, Espuma, Costura, Cor,  Orcamento, OrcamentoEspuma, OrcamentoTecido, OrcamentoCostura, Pedido
from datetime import datetime
main = Blueprint("main", __name__)


# =========================
# HOME
# =========================

@main.route("/")
def home():
    return render_template("consulta.html")


# =========================
# BUSCAR CLIENTE
# =========================

@main.route("/buscar", methods=["POST"])
def buscar():

    cod_cliente = request.form["cod_cliente"].upper()

    cliente = Cliente.query.filter_by(
        cod_cliente=cod_cliente
    ).first()
    
    if not cod_cliente:
        flash("Digite um CPF ou CNPJ para pesquisar.", "error")
        return redirect(url_for("main.home"))

    if cliente:

        return render_template(
            "cliente.html",
            cliente=cliente
        )

    flash("Cliente não encontrado.", "error")

    return redirect(url_for("main.home"))


# =========================
# LISTAR CLIENTES
# =========================

@main.route("/clientes")
def listar_clientes():
    # apenas clientes com nome preenchido, para evitar mostrar registros "deletados" (soft delete)
    clientes = Cliente.query.filter(~Cliente.nome.ilike("%Descadastrado%")).all()
    #clientes = Cliente.query.filter().all()
    return render_template(
        "lista_clientes.html",
        clientes=clientes
    )


# =========================
# CADASTRAR CLIENTE
# =========================

@main.route("/cadastrar_cliente")
def cadastrar_cliente():

    return render_template(
        "form_cliente.html",
        titulo="Cadastrar Cliente",
        acao="main.salvar_cliente",
        botao="Cadastrar",
        cliente=None,
        cod_cliente=""
    )
    db.session.add(cliente)
    db.session.commit()

# =========================
# SALVAR CLIENTE
# =========================   
@main.route("/salvar_cliente", methods=["POST"])
def salvar_cliente():
    
    cod_cliente = request.form.get("cod_cliente")
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")
    
    # Verifica se já existe cliente com esse código
    existente = Cliente.query.filter_by(cod_cliente=cod_cliente).first()
    if existente:
        flash("Já existe um cadastro com esse código!", "warning")
        return redirect(url_for("main.editar_cliente", id_cliente=existente.id_cliente))

    cliente = Cliente(
        cod_cliente=cod_cliente,
        nome=nome
    )

    cliente = Cliente(
        cod_cliente=cod_cliente,
        nome=nome
    )
    if telefone:
        cliente.telefone = TelefoneCliente(telefone=telefone)

    if any(request.form.get(field) for field in ["rua", "numero", "bairro", "cidade", "estado", "cep", "complemento"]):
        cliente.endereco = EnderecoCliente(
            rua=request.form.get("rua"),
            numero=request.form.get("numero"),
            bairro=request.form.get("bairro"),
            cidade=request.form.get("cidade"),
            estado=request.form.get("estado"),
            cep=request.form.get("cep"),
            complemento=request.form.get("complemento")
        )

    db.session.add(cliente)
    db.session.commit()

    return redirect(url_for("main.listar_clientes"))






@main.route("/cliente/<int:id_cliente>")
def perfil_cliente(id_cliente):

    cliente = Cliente.query.get_or_404(id_cliente)

    return render_template(
        "cliente.html",
        cliente=cliente
    )
# =========================
# EDITAR CLIENTE
# =========================

@main.route("/editar/<int:id_cliente>")
def editar_cliente(id_cliente):

    cliente = Cliente.query.get_or_404(id_cliente)

    return render_template(
        "form_cliente.html",
        titulo="Editar Cliente",
        botao="Atualizar",
        acao="main.atualizar_cliente",
        cliente=cliente
    )


# =========================
# ATUALIZAR CLIENTE
# =========================

@main.route("/atualizar_cliente/<int:id_cliente>", methods=["POST"])
def atualizar_cliente(id_cliente):

    cliente = Cliente.query.get_or_404(id_cliente)

    cliente.nome = request.form["nome"]

    cliente.telefone.telefone = request.form["telefone"]

    cliente.endereco.rua = request.form["rua"]
    cliente.endereco.numero = request.form["numero"]
    cliente.endereco.bairro = request.form["bairro"]
    cliente.endereco.cidade = request.form["cidade"]
    cliente.endereco.estado = request.form["estado"]
    cliente.endereco.cep = request.form["cep"]
    cliente.endereco.complemento = request.form["complemento"]

    db.session.commit()

    return redirect(url_for("main.listar_clientes"))

# =========================
# DELETAR CLIENTE
# =========================
# soft delete - para preservar o histórico de pedidos e veículos associados ao cliente, vamos apenas limpar os dados sensíveis e remover as associações com telefone e endereço, em vez de deletar o registro completamente.
## Para proteger a privacidade do cliente, em vez de deletar o registro, vamos apenas limpar os dados sensíveis e remover as associações com telefone e endereço.
@main.route("/deletar_cliente/<int:id_cliente>", methods=["POST"])
def deletar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)

    # Remove dados sensíveis
    # Marca como "Descadastrado" em vez de apagar
    cliente.nome = f"Descadastrado_{cliente.id_cliente}"
    cliente.cod_cliente = f"Descadastrado_{cliente.id_cliente}"
    # Atualiza veículos vinculados
    veiculos = Veiculo.query.filter_by(id_cliente=id_cliente).all()
    for veiculo in veiculos:
        veiculo.placa = f"Descadastrado_{veiculo.id_veiculo}"
    # Remove telefone e endereço, se existirem
    if cliente.telefone:
        db.session.delete(cliente.telefone)
    if cliente.endereco:
        db.session.delete(cliente.endereco)

    db.session.commit()

    return redirect(url_for(
        "main.listar_clientes"
    ))

# =========================
# DELETAR VEÍCULO
# =========================
# soft delete
@main.route("/deletar_veiculo/<int:id_veiculo>", methods=["POST"])
def deletar_veiculo(id_veiculo):

    veiculo = Veiculo.query.get_or_404(id_veiculo)

    id_cliente = veiculo.id_cliente

    veiculo.placa = f"Descadastrado_{veiculo.id_veiculo}"
    db.session.commit()

    return redirect(url_for(
        "main.listar_clientes"
    ))

# =========================
# ADICIONAR VEÍCULO
# =========================

@main.route("/novo_veiculo/<int:id_cliente>")
def novo_veiculo(id_cliente):

    return render_template(
        "form_veiculo.html",
        id_cliente=id_cliente
    )
    
@main.route("/salvar_veiculo", methods=["POST"])
def salvar_veiculo():

    id_veiculo = request.form.get("id_veiculo")

    if id_veiculo:
        veiculo = Veiculo.query.get_or_404(id_veiculo)
    else:
        veiculo = Veiculo()
        db.session.add(veiculo)

    veiculo.id_cliente = request.form.get("id_cliente")
    veiculo.placa = request.form.get("placa")
    veiculo.marca = request.form.get("marca")
    veiculo.modelo = request.form.get("modelo")
    veiculo.ano = request.form.get("ano")
    veiculo.cor = request.form.get("cor")

    db.session.commit()

    return redirect(url_for("main.listar_clientes"))
    
@main.route("/editar_veiculo/<int:id_veiculo>", methods=["GET"])
def editar_veiculo(id_veiculo):

    veiculo = Veiculo.query.get_or_404(id_veiculo)

    return render_template(
        "form_veiculo.html",
        veiculo=veiculo,
        id_cliente=veiculo.id_cliente
    )
    

    
# =========================
# ADICIONAR PEDIDO
# =========================
@main.route("/ordem_servico/cadastrar/<int:id_cliente>/<int:id_veiculo>", methods=["GET", "POST"])
def cadastrar_ordem_servico(id_cliente, id_veiculo):
    cliente = Cliente.query.get_or_404(id_cliente)
    veiculo = Veiculo.query.get_or_404(id_veiculo)

    if request.method == "POST":
        data_abertura_str = request.form.get("data_abertura")
        data_abertura = None
        if data_abertura_str:
            data_abertura = datetime.strptime(data_abertura_str, "%Y-%m-%d").date() # transforma a string em objeto date
        else:
            data_abertura = datetime.today().date() # se não for fornecida, usa a data atual
        quantidade_bancos = request.form.get("quantidade_bancos")
        padrao_veiculo = request.form.get("padrao_veiculo") == "true"
        personalizacao_igual = request.form.get("personalizacao_igual") == "true"
        observacoes = request.form.get("observacoes")

        nova_os = OrdemServico(
            id_veiculo=id_veiculo,
            data_abertura=data_abertura,
            quantidade_bancos=quantidade_bancos,
            padrao_veiculo=padrao_veiculo,
            personalizacao_igual=personalizacao_igual,
            observacoes=observacoes
        )

        db.session.add(nova_os)
        db.session.commit()

        return redirect(url_for("main.listar_clientes"))  # ajuste se sua função estiver dentro de blueprint "main"

    # Passa os objetos cliente e veiculo para o template
    return render_template(
        "ordem_servico.html",
        cliente=cliente,
        veiculo=veiculo
    )
