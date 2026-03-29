from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Cliente, TelefoneCliente, EnderecoCliente, Veiculo

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

    if cliente:

        return render_template(
            "cliente.html",
            cliente=cliente
        )

    return render_template(
        "form_cliente.html",
        titulo="Cadastrar Cliente",
        botao="Cadastrar",
        acao="main.cadastrar_cliente",
        cliente=None,
        cod_cliente=cod_cliente
    )


# =========================
# LISTAR CLIENTES
# =========================

@main.route("/clientes")
def listar_clientes():

    clientes = Cliente.query.all()

    return render_template(
        "lista_clientes.html",
        clientes=clientes
    )


# =========================
# CADASTRAR CLIENTE
# =========================

@main.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():

    cliente = Cliente(
        cod_cliente=request.form["cod_cliente"],
        nome=request.form["nome"]
    )

    telefone = TelefoneCliente(
        telefone=request.form["telefone"],
        cliente=cliente
    )

    endereco = EnderecoCliente(
        rua=request.form["rua"],
        numero=request.form["numero"],
        bairro=request.form["bairro"],
        cidade=request.form["cidade"],
        estado=request.form["estado"],
        cep=request.form["cep"],
        complemento=request.form["complemento"],
        cliente=cliente
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

@main.route("/deletar_cliente/<int:id_cliente>", methods=["POST"])
def deletar_cliente(id_cliente):

    cliente = Cliente.query.get_or_404(id_cliente)

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("main.listar_clientes"))


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
    
@main.route("/deletar_veiculo/<int:id_veiculo>", methods=["POST"])
def deletar_veiculo(id_veiculo):

    veiculo = Veiculo.query.get_or_404(id_veiculo)

    id_cliente = veiculo.id_cliente

    db.session.delete(veiculo)
    db.session.commit()

    return redirect(url_for(
        "main.editar_cliente",
        id_cliente=id_cliente
    ))