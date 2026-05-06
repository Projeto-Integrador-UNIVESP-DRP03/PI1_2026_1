from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app, jsonify
from datetime import datetime
from sqlalchemy import func

# tabelas
from .models import (
    db,
    Cliente,
    Veiculo,
    TelefoneCliente,
    EnderecoCliente,
    Tecido,
    Espuma,
    Costura,
    Cor,
    Orcamento,
    OrcamentoTecido,
    OrcamentoEspuma,
    OrcamentoCostura,
    OrcamentoCor,
    Pedido
)

# para gerar pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import io
import os




# função para criar slugs a partir de textos, para nomes de arquivos
import unicodedata
import re
def slugify(texto):
    # Normaliza acentos (ex: João -> Joao)
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    # Substitui espaços por underscore
    texto = re.sub(r"\s+", "_", texto)
    # Remove caracteres especiais
    texto = re.sub(r"[^\w\-]", "", texto)
    # Converte para minúsculas
    return texto.lower()


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
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = max(1, min(per_page, 10000))

    # apenas clientes com nome preenchido, para evitar mostrar registros "deletados" (soft delete)
    query = (
        Cliente.query
        .filter(~Cliente.nome.ilike("%Descadastrado%"))
        .order_by(Cliente.nome.asc())
    )
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "lista_clientes.html",
        clientes=pagination.items,
        pagination=pagination
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
    db.session.add(cliente)
    
    if request.form.get("telefone"):
        cliente.telefones.append(
            TelefoneCliente(telefone=request.form.get("telefone"))
        )

    
    if any(request.form.get(field) for field in ["rua", "numero", "bairro", "cidade", "estado", "cep", "complemento"]):
        cliente.enderecos.append(
            EnderecoCliente(
                rua=request.form.get("rua"),
                numero=request.form.get("numero"),
                bairro=request.form.get("bairro"),
                cidade=request.form.get("cidade"),
                estado=request.form.get("estado"),
                cep=request.form.get("cep"),
                complemento=request.form.get("complemento")
            )
        )
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

    # Telefone
    if cliente.telefones:  # já existe pelo menos um telefone
        # atualiza o telefone da posição zero
        cliente.telefones[0].telefone = request.form["telefone"]
    else:
        # adiciona um novo telefone como primeiro da lista
        cliente.telefones.append(
            TelefoneCliente(telefone=request.form.get("telefone"))
        )


    # Endereço
    if cliente.enderecos:
        cliente.enderecos[0].rua = request.form["rua"]
        cliente.enderecos[0].numero = request.form["numero"]
        cliente.enderecos[0].bairro = request.form["bairro"]
        cliente.enderecos[0].cidade = request.form["cidade"]
        cliente.enderecos[0].estado = request.form["estado"]
        cliente.enderecos[0].cep = request.form["cep"]
        cliente.enderecos[0].complemento = request.form["complemento"]
    else:
        cliente.enderecos.append(
            EnderecoCliente(
                rua=request.form["rua"],
                numero=request.form["numero"],
                bairro=request.form["bairro"],
                cidade=request.form["cidade"],
                estado=request.form["estado"],
                cep=request.form["cep"],
                complemento=request.form["complemento"])
        )

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
    for tel in cliente.telefones:
        db.session.delete(tel)

    for end in cliente.enderecos:
        db.session.delete(end)

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
    id_cliente = request.form.get("id_cliente")
    placa_nova = request.form.get("placa")
    placa_normalizada = placa_nova.upper() if placa_nova else placa_nova

    if not id_cliente:
        flash("Selecione o cliente antes de cadastrar o veículo.", "error")
        return redirect(url_for("main.listar_clientes"))

    if not placa_normalizada:
        flash("Informe a placa do veículo.", "error")
        return redirect(url_for("main.novo_veiculo", id_cliente=id_cliente))

    if id_veiculo:
        veiculo = Veiculo.query.get_or_404(id_veiculo)
    else:
        veiculo = Veiculo()

    existe = Veiculo.query.filter_by(placa=placa_normalizada).first()
    if existe and (not id_veiculo or existe.id_veiculo != int(id_veiculo)):
        flash("Já existe um veículo cadastrado com esta placa.", "error")
        return redirect(url_for("main.editar_veiculo", id_veiculo=existe.id_veiculo))

    veiculo.id_cliente = id_cliente
    veiculo.placa = placa_normalizada
    veiculo.marca = request.form.get("marca")
    veiculo.modelo = request.form.get("modelo")
    veiculo.ano = request.form.get("ano")
    veiculo.cor = request.form.get("cor")

    if not id_veiculo:
        db.session.add(veiculo)
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
    

@main.route("/orcamento/<int:id_veiculo>")
def form_orcamento(id_veiculo):

    veiculo = Veiculo.query.get_or_404(id_veiculo)
    cliente = veiculo.cliente

    tecidos = Tecido.query.all()
    espumas = Espuma.query.all()
    costuras = Costura.query.all()
    cores = Cor.query.all()
    
    data_br = datetime.today().strftime("%d/%m/%Y")
    today_iso = datetime.today().strftime("%Y-%m-%d")

    return render_template(
        "form_orcamento.html",
        cliente=cliente,
        veiculo=veiculo,
        tecidos=tecidos,
        espumas=espumas,
        costuras=costuras,
        cores=cores,
        today=data_br,
        today_iso=today_iso,
        orcamento=None,
        tecidos_selecionados=[],
        costuras_selecionadas=[],
        cores_selecionadas=[],
        espumas_selecionadas=[],
        obs_tecidos="",
        obs_costuras="",
        obs_cores=""
    )


@main.route("/orcamento/<int:id_orcamento>/editar")
def editar_orcamento(id_orcamento):
    orcamento = Orcamento.query.get_or_404(id_orcamento)
    veiculo = orcamento.veiculo
    cliente = veiculo.cliente

    tecidos = Tecido.query.all()
    espumas = Espuma.query.all()
    costuras = Costura.query.all()
    cores = Cor.query.all()

    data_br = orcamento.dat_orcamento.strftime("%d/%m/%Y") if orcamento.dat_orcamento else datetime.today().strftime("%d/%m/%Y")

    tecidos_itens = OrcamentoTecido.query.filter_by(id_orcamento=id_orcamento).all()
    costuras_itens = OrcamentoCostura.query.filter_by(id_orcamento=id_orcamento).all()
    cores_itens = OrcamentoCor.query.filter_by(id_orcamento=id_orcamento).all()
    espumas_itens = OrcamentoEspuma.query.filter_by(id_orcamento=id_orcamento).all()

    tecidos_selecionados = [f"{item.tecido.material} - {item.tecido.cor}" if item.tecido and item.tecido.cor else (item.tecido.material if item.tecido else "") for item in tecidos_itens if item.tecido]
    costuras_selecionadas = [item.costura.tipo for item in costuras_itens if item.costura]
    cores_selecionadas = [item.cor.descricao for item in cores_itens if item.cor]
    espumas_selecionadas = [item.id_espuma for item in espumas_itens if item.id_espuma]

    obs_tecidos = next((item.obs_item for item in tecidos_itens if (item.obs_item or "").strip()), "") or ""
    obs_costuras = next((item.obs_item for item in costuras_itens if (item.obs_item or "").strip()), "") or ""
    obs_cores = next((item.obs_item for item in cores_itens if (item.obs_item or "").strip()), "") or ""

    return render_template(
        "form_orcamento.html",
        cliente=cliente,
        veiculo=veiculo,
        tecidos=tecidos,
        espumas=espumas,
        costuras=costuras,
        cores=cores,
        today=data_br,
        orcamento=orcamento,
        tecidos_selecionados=tecidos_selecionados,
        costuras_selecionadas=costuras_selecionadas,
        cores_selecionadas=cores_selecionadas,
        espumas_selecionadas=espumas_selecionadas,
        obs_tecidos=obs_tecidos,
        obs_costuras=obs_costuras,
        obs_cores=obs_cores
    )
# =========================
# SALVAR ORÇAMENTO
# =========================
from datetime import datetime
from flask import request, redirect, url_for

@main.route("/salvar_orcamento", methods=["POST"])
def salvar_orcamento():

    id_veiculo = request.form.get("id_veiculo")
    id_orcamento = request.form.get("id_orcamento")

    # data
    data_str = request.form.get("dat_orcamento")
    try:
        dat_orcamento = datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        dat_orcamento = datetime.strptime(data_str, "%d/%m/%Y").date()

    # números
    qtd_bancos = int(request.form.get("qtd_bancos") or 0)
    qtd_apoio_cabeca = int(request.form.get("qtd_apoio_cabeca") or 0)

    valor_raw = request.form.get("valor") or "0"
    try:
        valor = float(valor_raw)
    except ValueError:
        valor = float(valor_raw.replace(".", "").replace(",", "."))

    # booleanos
    bool_original = True if request.form.get("bool_original") else False
    bool_logo_prensada = True if request.form.get("bool_logo_prensada") else False
    bool_espuma = True if request.form.get("bool_espuma") else False

    banco_motorista = True if request.form.get("banco_motorista") else False
    banco_passageiro = True if request.form.get("banco_passageiro") else False
    banco_traseiro = True if request.form.get("banco_traseiro") else False

    obs = request.form.get("obs")

    # Observações por seção (30 chars)
    obs_tecidos = (request.form.get("obs_tecidos") or "").strip()[:30]
    obs_costuras = (request.form.get("obs_costuras") or "").strip()[:30]
    obs_cores = (request.form.get("obs_cores") or "").strip()[:30]

    if id_orcamento:
        orcamento = Orcamento.query.get_or_404(id_orcamento)
        orcamento.id_veiculo = id_veiculo
        orcamento.dat_orcamento = dat_orcamento
        orcamento.qtd_bancos = qtd_bancos
        orcamento.qtd_apoio_cabeca = qtd_apoio_cabeca
        orcamento.bool_original = bool_original
        orcamento.bool_logo_prensada = bool_logo_prensada
        orcamento.bool_espuma = bool_espuma
        orcamento.banco_motorista = banco_motorista
        orcamento.banco_passageiro = banco_passageiro
        orcamento.banco_traseiro = banco_traseiro
        orcamento.valor = valor
        orcamento.obs = obs
        db.session.commit()
    else:
        # =========================
        # CRIAR ORÇAMENTO
        # =========================

        novo_orcamento = Orcamento(
            id_veiculo=id_veiculo,
            dat_orcamento=dat_orcamento,
            qtd_bancos=qtd_bancos,
            qtd_apoio_cabeca=qtd_apoio_cabeca,
            bool_original=bool_original,
            bool_logo_prensada=bool_logo_prensada,
            bool_espuma=bool_espuma,
            banco_motorista=banco_motorista,
            banco_passageiro=banco_passageiro,
            banco_traseiro=banco_traseiro,
            valor=valor,
            obs=obs
        )

        db.session.add(novo_orcamento)
        db.session.commit()

        id_orcamento = novo_orcamento.id_orcamento

    db.session.query(OrcamentoTecido).filter_by(id_orcamento=id_orcamento).delete()
    db.session.query(OrcamentoCostura).filter_by(id_orcamento=id_orcamento).delete()
    db.session.query(OrcamentoCor).filter_by(id_orcamento=id_orcamento).delete()
    db.session.query(OrcamentoEspuma).filter_by(id_orcamento=id_orcamento).delete()
    db.session.commit()

    # =========================
    # MAPEAMENTOS PARA MATERIAIS
    # =========================
    tecido_map = {f"{t.material} - {t.cor}" if t.cor else t.material: t.id_tecido for t in Tecido.query.all()}
    costura_map = {c.tipo: c.id_costura for c in Costura.query.all()}
    cor_map = {c.descricao: c.id_cor for c in Cor.query.all()}

    # =========================
    # TECIDOS
    # =========================

    tecidos = request.form.getlist("tecidos")

    for tecido_nome in tecidos:
        tecido_id = tecido_map.get(tecido_nome)
        if not tecido_id:
            continue  # ou erro, mas por enquanto skip

        item = OrcamentoTecido(
            id_orcamento=id_orcamento,
            id_tecido=tecido_id,
            obs_item=obs_tecidos
        )

        db.session.add(item)

    # =========================
    # COSTURAS
    # =========================

    costuras = request.form.getlist("costuras")

    for costura_nome in costuras:
        costura_id = costura_map.get(costura_nome)
        if not costura_id:
            continue

        item = OrcamentoCostura(
            id_orcamento=id_orcamento,
            id_costura=costura_id,
            obs_item=obs_costuras
        )

        db.session.add(item)

    # =========================
    # CORES
    # =========================

    cores = request.form.getlist("cores")

    for cor_nome in cores:
        cor_id = cor_map.get(cor_nome)
        if not cor_id:
            continue

        item = OrcamentoCor(
            id_orcamento=id_orcamento,
            id_cor=cor_id,
            obs_item=obs_cores
        )

        db.session.add(item)

    # =========================
    # ESPUMAS
    # =========================

    if bool_espuma:
        espumas_selecionadas = request.form.getlist("espumas")
        for e_id in espumas_selecionadas:
            try:
                espuma_id = int(e_id)
                item = OrcamentoEspuma(
                    id_orcamento=id_orcamento,
                    id_espuma=espuma_id
                )
                db.session.add(item)
            except (ValueError, TypeError):
                continue

    db.session.commit()

    return redirect(url_for("main.lista_orcamentos"))


@main.route("/orcamentos")
def lista_orcamentos():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = max(1, min(per_page, 10000))

    if request.args.get("all") == "1":
        query = Orcamento.query.order_by(Orcamento.dat_orcamento.desc())
    else:
        query = (
            Orcamento.query
            .outerjoin(Pedido, Pedido.id_orcamento == Orcamento.id_orcamento)
            .filter(Pedido.id_pedido == None)
            .order_by(Orcamento.dat_orcamento.desc())
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Estatísticas globais (não dependem da página atual)
    base = query.order_by(None)
    valor_total = float(base.with_entities(func.coalesce(func.sum(Orcamento.valor), 0.0)).scalar() or 0.0)

    hoje = datetime.today().date()
    mes_inicio = datetime(hoje.year, hoje.month, 1).date()
    if hoje.month == 12:
        mes_fim = datetime(hoje.year + 1, 1, 1).date()
    else:
        mes_fim = datetime(hoje.year, hoje.month + 1, 1).date()

    orcamentos_mes = (
        base
        .filter(Orcamento.dat_orcamento >= mes_inicio)
        .filter(Orcamento.dat_orcamento < mes_fim)
        .count()
    )

    total_orcamentos = int(pagination.total or 0)
    ticket_medio = (valor_total / total_orcamentos) if total_orcamentos else 0.0

    return render_template(
        "lista_orcamentos.html",
        orcamentos=pagination.items,
        pagination=pagination,
        stats={
            "total_orcamentos": total_orcamentos,
            "orcamentos_mes": int(orcamentos_mes or 0),
            "ticket_medio": float(ticket_medio),
            "valor_total": float(valor_total),
        }
    )

@main.route("/orcamento/<int:id_orcamento>/aceitar", methods=["POST"])
def aceitar_orcamento(id_orcamento):
    orcamento = Orcamento.query.get_or_404(id_orcamento)

    pedido = Pedido.query.filter_by(id_orcamento=orcamento.id_orcamento).first()
    if not pedido:
        pedido = Pedido(id_orcamento=orcamento.id_orcamento)

    pedido.boolean_aceite_cliente = True
    pedido.aceite_cliente = True
    pedido.dat_aceite_cliente = datetime.today().date()
    if not pedido.status or pedido.status.lower() == "recusado":
        pedido.status = "Pendente"

    db.session.add(pedido)
    db.session.commit()

    flash("Orçamento aprovado e enviado para pedidos.", "success")
    return redirect(url_for("main.lista_pedidos"))


@main.route("/orcamento/<int:id_orcamento>/recusar", methods=["POST"])
def recusar_orcamento(id_orcamento):
    orcamento = Orcamento.query.get_or_404(id_orcamento)

    pedido = Pedido.query.filter_by(id_orcamento=orcamento.id_orcamento).first()
    if not pedido:
        pedido = Pedido(id_orcamento=orcamento.id_orcamento)

    pedido.boolean_aceite_cliente = False
    pedido.aceite_cliente = False
    pedido.dat_aceite_cliente = datetime.today().date()
    pedido.status = "Recusado"

    db.session.add(pedido)
    db.session.commit()

    flash("Orçamento recusado pelo cliente.", "info")
    return redirect(url_for("main.lista_orcamentos"))


@main.route("/pedidos")
def lista_pedidos():

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = max(1, min(per_page, 10000))

    query = (
        Orcamento.query
        .join(Pedido, Pedido.id_orcamento == Orcamento.id_orcamento)
        .filter(Pedido.boolean_aceite_cliente == True)
        .filter(Pedido.status != "Concluído")
        .order_by(Orcamento.dat_orcamento.desc())
    )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Estatísticas globais (não dependem da página atual)
    base = query.order_by(None)
    total_pedidos = int(pagination.total or 0)
    pedidos_andamento = base.filter(Pedido.status == "Em Andamento").count()
    valor_total = float(base.with_entities(func.coalesce(func.sum(Orcamento.valor), 0.0)).scalar() or 0.0)

    # Total concluídos (geral) para o card, mesmo sendo uma tela só de "não concluídos"
    concluidos_total = (
        Orcamento.query
        .join(Pedido, Pedido.id_orcamento == Orcamento.id_orcamento)
        .filter(Pedido.boolean_aceite_cliente == True)
        .filter(Pedido.status == "Concluído")
        .order_by(None)
        .count()
    )

    return render_template(
        "pedidos.html",
        orcamentos=pagination.items,
        pagination=pagination,
        stats={
            "total_pedidos": total_pedidos,
            "pedidos_andamento": int(pedidos_andamento or 0),
            "pedidos_concluidos": int(concluidos_total or 0),
            "valor_total": float(valor_total),
        }
    )

@main.route("/pedidos/concluidos")
def pedidos_concluidos():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = max(1, min(per_page, 10000))

    query = (
        Orcamento.query
        .join(Pedido, Pedido.id_orcamento == Orcamento.id_orcamento)
        .filter(Pedido.boolean_aceite_cliente == True)
        .filter(Pedido.status == "Concluído")
        .order_by(Orcamento.dat_orcamento.desc())
    )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    # Estatísticas globais (não dependem da página atual)
    base = query.order_by(None)
    total_concluidos = int(pagination.total or 0)
    valor_total = float(base.with_entities(func.coalesce(func.sum(Orcamento.valor), 0.0)).scalar() or 0.0)

    hoje = datetime.today().date()
    mes_inicio = datetime(hoje.year, hoje.month, 1).date()
    if hoje.month == 12:
        mes_fim = datetime(hoje.year + 1, 1, 1).date()
    else:
        mes_fim = datetime(hoje.year, hoje.month + 1, 1).date()

    concluidos_mes = (
        base
        .filter(Pedido.data_conclusao >= mes_inicio)
        .filter(Pedido.data_conclusao < mes_fim)
        .count()
    )

    return render_template(
        "pedidos_concluidos.html",
        orcamentos=pagination.items,
        pagination=pagination,
        stats={
            "total_concluidos": total_concluidos,
            "concluidos_mes": int(concluidos_mes or 0),
            "valor_total": float(valor_total),
        }
    )


@main.route("/pedido/<int:id_pedido>/editar", methods=["GET", "POST"])
def editar_pedido(id_pedido):
    pedido = Pedido.query.get_or_404(id_pedido)

    if request.method == "POST":
        status = request.form.get("status")
        status = status.strip() if status else ""

        if status not in ["Pendente", "Em Andamento", "Concluído"]:
            flash("Status inválido. Use Pendente, Em Andamento ou Concluído.", "error")
            return redirect(url_for("main.editar_pedido", id_pedido=id_pedido))

        pedido.status = status

        if status == "Em Andamento" and not pedido.data_inicio:
            pedido.data_inicio = datetime.today().date()

        if status == "Concluído":
            if not pedido.data_conclusao:
                pedido.data_conclusao = datetime.today().date()
        else:
            pedido.data_conclusao = None

        db.session.commit()
        flash("Status do pedido atualizado.", "success")
        return redirect(url_for("main.lista_pedidos"))

    return render_template(
        "pedido_editar.html",
        pedido=pedido
    )

@main.route("/pedido/<int:id_pedido>/status", methods=["POST"])
def atualizar_status_pedido(id_pedido):
    pedido = Pedido.query.get_or_404(id_pedido)

    status = (request.form.get("status") or "").strip()
    if status not in ["Pendente", "Em Andamento", "Concluído"]:
        flash("Status inválido. Use Pendente, Em Andamento ou Concluído.", "error")
        return redirect(url_for("main.lista_pedidos"))

    pedido.status = status
    if status == "Em Andamento" and not pedido.data_inicio:
        pedido.data_inicio = datetime.today().date()

    if status == "Concluído":
        if not pedido.data_conclusao:
            pedido.data_conclusao = datetime.today().date()
    else:
        pedido.data_conclusao = None

    db.session.commit()
    flash("Status atualizado.", "success")
    return redirect(url_for("main.lista_pedidos"))


@main.route("/novo_pedido")
def novo_pedido():
    # apenas clientes com nome preenchido, para evitar mostrar registros "deletados" (soft delete)
    clientes = Cliente.query.filter(~Cliente.nome.ilike("%Descadastrado%")).all()
    return render_template(
        "selecionar_cliente_pedido.html",
        clientes=clientes
    )


@main.route("/selecionar_veiculo/<int:id_cliente>")
def selecionar_veiculo_pedido(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    return render_template(
        "selecionar_veiculo_pedido.html",
        cliente=cliente
    )
    
    
@main.route("/orcamento/<int:id_orcamento>/visualizar")
def visualizar_orcamento(id_orcamento):

    orcamento = Orcamento.query.get_or_404(id_orcamento)

    veiculo = orcamento.veiculo
    cliente = veiculo.cliente

    tecidos = OrcamentoTecido.query.filter_by(id_orcamento=id_orcamento).all()
    costuras = OrcamentoCostura.query.filter_by(id_orcamento=id_orcamento).all()
    cores = OrcamentoCor.query.filter_by(id_orcamento=id_orcamento).all()
    espumas = OrcamentoEspuma.query.filter_by(id_orcamento=id_orcamento).all()

    return render_template(
        "visualizar_orcamento.html",
        orcamento=orcamento,
        veiculo=veiculo,
        cliente=cliente,
        tecidos=tecidos,
        costuras=costuras,
        cores=cores,
        espumas=espumas
    )
#--------------------------
# Rota para gerar PDF do orçamento
#--------------------------
@main.route("/orcamento/<int:id_orcamento>/pdf")
def gerar_pdf_orcamento(id_orcamento):

    orcamento = Orcamento.query.get_or_404(id_orcamento)
    veiculo = Veiculo.query.get(orcamento.id_veiculo)
    cliente = Cliente.query.get(veiculo.id_cliente)

    tecidos = OrcamentoTecido.query.filter_by(id_orcamento=id_orcamento).all()
    costuras = OrcamentoCostura.query.filter_by(id_orcamento=id_orcamento).all()
    cores = OrcamentoCor.query.filter_by(id_orcamento=id_orcamento).all()
    espumas = OrcamentoEspuma.query.filter_by(id_orcamento=id_orcamento).all()

    buffer = io.BytesIO()

    # Configuração da página com margens reduzidas para caber em uma página
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=15,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()
    elementos = []

    # ======================
    # ESTILOS PERSONALIZADOS
    # ======================
    
    # Estilo para título principal
    titulo_style = ParagraphStyle(
        "Titulo",
        parent=styles["Heading1"],
        fontSize=16,
        alignment=1,
        spaceAfter=8,
        textColor=colors.HexColor("#1a237e")
    )
    
    # Estilo para seções
    secao_style = ParagraphStyle(
        "Secao",
        parent=styles["Heading3"],
        fontSize=11,
        textColor=colors.HexColor("#1565c0"),
        spaceAfter=5,
        spaceBefore=8,
        fontWeight='bold'
    )
    
    # Estilo para o valor
    valor_style = ParagraphStyle(
        "Valor",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#c62828"),
        alignment=1,
        fontSize=16,
        spaceAfter=10,
        spaceBefore=10,
        fontWeight='bold'
    )
    
    # Estilo para informações do cliente
    info_style = ParagraphStyle(
        "Info",
        parent=styles["Normal"],
        fontSize=8,
        leading=10
    )
    
    # Estilo para texto normal
    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontSize=9,
        leading=11
    )

    # ======================
    # CABEÇALHO COM LOGO E EMPRESA (COMPLETO)
    # ======================
    logo_path = os.path.join(
        current_app.root_path,
        "static/imagens/Identidade_visual/logo_zito.png"
    )
    
    # Verifica se o logo existe
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.8*cm, height=2.8*cm)
    else:
        logo = Paragraph("", styles["Normal"])

    # Dados da empresa completos
    dados_empresa = Paragraph("""
    <b><font size="10">ZITO TAPEÇARIA PARA AUTOS</font></b><br/>
    <font size="7">Rua Dr. Laerte Machado Guimarães, 241 – São Benedito<br/>
    Pindamonhangaba – SP<br/>
    Tel. (12) 3642-4713 / 3522-4713<br/>
    CNPJ 74.458.852/0001-63<br/>
    I.E. 528.045.963.113<br/>
    Email: zitotapecaria@gmail.com</font>
    """, info_style)

    # Tabela do cabeçalho
    cabecalho = Table([[dados_empresa, logo]], colWidths=[12*cm, 3.5*cm])
    cabecalho.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (0,0), "LEFT"),
        ("ALIGN", (1,0), (1,0), "RIGHT"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("TOPPADDING", (0,0), (-1,-1), 3),
    ]))

    elementos.append(cabecalho)
    
    # Linha divisória
    elementos.append(Paragraph("<hr/>", styles["Normal"]))
    elementos.append(Spacer(1, 3))

    # Título do documento
    elementos.append(Paragraph("ORÇAMENTO", titulo_style))
    elementos.append(Spacer(1, 5))

    # ======================
    # INFORMAÇÕES DO CLIENTE E VEÍCULO (LADO A LADO)
    # ======================
    telefone = cliente.telefones[0].telefone if cliente.telefones else "Não informado"
    endereco = cliente.enderecos[0] if cliente.enderecos else None
    
    # Construir endereço sem a palavra "ENDEREÇO:" antes
    endereco_linhas = []
    if endereco:
        linha1 = f"{endereco.rua}, {endereco.numero}"
        if endereco.bairro:
            linha1 += f" - {endereco.bairro}"
        endereco_linhas.append(linha1)
        
        linha2 = ""
        if endereco.cidade:
            linha2 += endereco.cidade
        if endereco.estado:
            linha2 += f"/{endereco.estado}"
        if linha2:
            endereco_linhas.append(linha2)
        
        if endereco.complemento:
            endereco_linhas.append(f"Complemento: {endereco.complemento}")
    
    endereco_texto = "<br/>".join(endereco_linhas) if endereco_linhas else "Não informado"
    
    # Criar conteúdo do cliente (esquerda)
    conteudo_cliente = []
    conteudo_cliente.append(Paragraph(f"<b>CLIENTE:</b> {cliente.nome}", normal_style))
    conteudo_cliente.append(Paragraph(f"<b>TELEFONE:</b> {telefone}", normal_style))
    conteudo_cliente.append(Paragraph(endereco_texto, normal_style))
    
    # Criar conteúdo do veículo (direita)
    veiculo_texto = f"{veiculo.marca} {veiculo.modelo}".strip() if veiculo.marca or veiculo.modelo else "Não informado"
    conteudo_veiculo = []
    conteudo_veiculo.append(Paragraph(f"<b>VEÍCULO:</b> {veiculo_texto}", normal_style))
    conteudo_veiculo.append(Paragraph(f"<b>PLACA:</b> {veiculo.placa}", normal_style))
    conteudo_veiculo.append(Paragraph(f"<b>DATA DO ORÇAMENTO:</b> {orcamento.dat_orcamento.strftime('%d/%m/%Y')}", normal_style))
    
    # Container para cliente e veículo lado a lado
    col_esquerda = Table([[item] for item in conteudo_cliente], colWidths=[8*cm])
    col_esquerda.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))
    
    col_direita = Table([[item] for item in conteudo_veiculo], colWidths=[8*cm])
    col_direita.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))
    
    tabela_lado_lado = Table([[col_esquerda, col_direita]], colWidths=[8*cm, 8*cm])
    tabela_lado_lado.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    
    elementos.append(tabela_lado_lado)
    elementos.append(Spacer(1, 5))
    
    # Linha divisória
    elementos.append(Paragraph("<hr/>", styles["Normal"]))
    elementos.append(Spacer(1, 3))

    # ======================
    # SERVIÇOS (Tabela compacta)
    # ======================
    elementos.append(Paragraph("SERVIÇOS", secao_style))
    
    espuma_texto = "Sim" if orcamento.bool_espuma else "Não"
    if orcamento.bool_espuma and espumas:
        espuma_nomes = ", ".join([e.espuma.tipo for e in espumas if e.espuma])
        espuma_texto += f" ({espuma_nomes})"
    
    bancos_selecionados = []
    if orcamento.banco_motorista: bancos_selecionados.append("Motorista")
    if orcamento.banco_passageiro: bancos_selecionados.append("Passageiro")
    if orcamento.banco_traseiro: bancos_selecionados.append("Traseiro")
    
    bancos_texto = str(orcamento.qtd_bancos)
    if bancos_selecionados:
        bancos_texto += f" ({', '.join(bancos_selecionados)})"
    
    servicos = [
        ["Quantidade de bancos", bancos_texto],
        ["Apoios de cabeça", str(orcamento.qtd_apoio_cabeca)],
        ["Manter padrão original", "Sim" if orcamento.bool_original else "Não"],
        ["Logo prensada", "Sim" if orcamento.bool_logo_prensada else "Não"],
        ["Troca de espuma", espuma_texto]
    ]
    
    tabela_servicos = Table(servicos, colWidths=[7*cm, 7*cm])
    tabela_servicos.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bdbdbd")),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e3f2fd")),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#ffffff")),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("FONTWEIGHT", (0,0), (-1,0), "BOLD"),
        ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#0d47a1")),
    ]))
    
    elementos.append(tabela_servicos)
    elementos.append(Spacer(1, 5))

    # ======================
    # MATERIAIS (UM EMBAIXO DO OUTRO)
    # ======================
    
    def criar_tabela_material(titulo, cabecalho, dados):
        if not dados:
            return None
        
        elementos.append(Paragraph(titulo, secao_style))
        
        col_widths = [7*cm, 7*cm]
        
        tabela = Table([cabecalho] + dados, colWidths=col_widths)
        tabela.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bdbdbd")),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e8eaf6")),
            ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#ffffff")),
            ("ALIGN", (0,0), (-1,-1), "LEFT"),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING", (0,0), (-1,-1), 5),
            ("RIGHTPADDING", (0,0), (-1,-1), 5),
            ("FONTWEIGHT", (0,0), (-1,0), "BOLD"),
            ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor("#1a237e")),
        ]))
        
        elementos.append(tabela)
        elementos.append(Spacer(1, 5))
        return tabela
    
    # Preparar dados dos materiais
    tecidos_dados = [[(item.tecido.material if item.tecido else "Não informado"), item.obs_item or "-"] 
                     for item in tecidos] if tecidos else []
    costuras_dados = [[(item.costura.tipo if item.costura else "Não informado"), item.obs_item or "-"] 
                      for item in costuras] if costuras else []
    cores_dados = [[(item.cor.descricao if item.cor else "Não informado"), item.obs_item or "-"] 
                   for item in cores] if cores else []
    espumas_dados = [[(item.espuma.tipo if item.espuma else "Não informado"), item.obs_item or "-"] 
                     for item in espumas] if espumas else []
    
    # Adicionar materiais um embaixo do outro
    if tecidos_dados:
        criar_tabela_material("TECIDOS", ["Material", "Observação"], tecidos_dados)
    
    if costuras_dados:
        criar_tabela_material("COSTURAS", ["Tipo", "Observação"], costuras_dados)
    
    if cores_dados:
        criar_tabela_material("CORES DE LINHA", ["Cor", "Observação"], cores_dados)
    
    if espumas_dados:
        criar_tabela_material("ESPUMAS", ["Tipo", "Observação"], espumas_dados)
    
    # Espaço antes do valor
    elementos.append(Spacer(1, 5))

    # ======================
    # VALOR (Destacado)
    # ======================
    elementos.append(Paragraph("<hr/>", styles["Normal"]))
    
    valor_formatado = f"R$ {orcamento.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    elementos.append(Paragraph(f"<b>VALOR TOTAL:</b> {valor_formatado}", valor_style))
    
    # ======================
    # OBSERVAÇÕES GERAIS
    # ======================
    if orcamento.obs and orcamento.obs.strip():
        elementos.append(Spacer(1, 3))
        elementos.append(Paragraph("OBSERVAÇÕES:", secao_style))
        elementos.append(Paragraph(orcamento.obs, normal_style))
    
    elementos.append(Spacer(1, 5))
    elementos.append(Paragraph("<hr/>", styles["Normal"]))

    # ======================
    # ASSINATURA (com linhas)
    # ======================
    elementos.append(Spacer(1, 25))  # Espaço aumentado antes da assinatura
    
    assinatura = Table([
        ["", ""],
        ["_________________________", "_________________________"],
        ["Cliente", "Zito Tapeçaria"]
    ], colWidths=[7*cm, 7*cm])
    
    assinatura.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("LINEABOVE", (0,1), (0,1), 0.5, colors.HexColor("#757575")),
        ("LINEABOVE", (1,1), (1,1), 0.5, colors.HexColor("#757575")),
        ("TEXTCOLOR", (0,2), (0,2), colors.HexColor("#37474f")),
        ("TEXTCOLOR", (1,2), (1,2), colors.HexColor("#37474f")),
    ]))
    
    elementos.append(assinatura)

    # ======================
    # GERAR PDF
    # ======================
    doc.build(elementos)
    buffer.seek(0)

    # Normaliza os textos para evitar espaços e acentos no nome do arquivo
    modelo = slugify(veiculo.modelo) if veiculo.modelo else "veiculo"
    cliente_nome = slugify(cliente.nome) if cliente.nome else "cliente"

    nome_arquivo = f"orc_{modelo}_{cliente_nome}_{orcamento.id_orcamento}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype="application/pdf"
    )

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@main.route("/api/dashboard/stats")
def dashboard_stats():
    # KPI 1: Total de Clientes (não descadastrados)
    total_clientes = Cliente.query.filter(~Cliente.nome.ilike("%Descadastrado%")).count()
    
    # KPI 2: Total de Orçamentos
    total_orcamentos = Orcamento.query.count()
    
    # KPI 3: Orçamentos Convertidos (únicos)
    # Contamos quantos orçamentos diferentes possuem pelo menos um pedido aceito
    pedidos_convertidos = db.session.query(func.count(func.distinct(Pedido.id_orcamento)))\
        .filter(Pedido.boolean_aceite_cliente == True).scalar() or 0
        
    taxa_conversao = round((pedidos_convertidos / total_orcamentos * 100), 1) if total_orcamentos > 0 else 0
    
    # KPI 4: Orçamentos este mês
    hoje = datetime.today().date()
    mes_inicio = datetime(hoje.year, hoje.month, 1).date()
    orcamentos_mes = Orcamento.query.filter(Orcamento.dat_orcamento >= mes_inicio).count()
    
    # KPI 5: Valor de Pedidos Concluídos no Mês
    query_concluidos = db.session.query(
        func.sum(Orcamento.valor),
        func.count(Pedido.id_pedido)
    ).join(Orcamento).filter(
        Pedido.status == 'Concluído',
        Pedido.data_conclusao >= mes_inicio
    ).first()
    
    valor_concluidos_mes = float(query_concluidos[0] or 0)
    total_concluidos_mes = query_concluidos[1] or 0
    ticket_concluidos_mes = (valor_concluidos_mes / total_concluidos_mes) if total_concluidos_mes > 0 else 0
    
    # Dados para Gráfico 1: Orçamentos por Mês (últimos 12 meses)
    # Usando SQLite strftime para agrupar
    orcamentos_mensais_raw = db.session.query(
        func.strftime('%Y-%m', Orcamento.dat_orcamento).label('mes_ano'),
        func.count(Orcamento.id_orcamento)
    ).group_by('mes_ano').order_by('mes_ano').all()
    
    # Dados para Gráfico de Conversão (Pedidos por Mês)
    pedidos_mensais_raw = db.session.query(
        func.strftime('%Y-%m', Orcamento.dat_orcamento).label('mes_ano'),
        func.count(Pedido.id_pedido)
    ).join(Orcamento).filter(Pedido.boolean_aceite_cliente == True)\
     .group_by('mes_ano').order_by('mes_ano').all()
    
    # Formatação para o Chart.js
    labels_meses = sorted(list(set([r[0] for r in orcamentos_mensais_raw] + [r[0] for r in pedidos_mensais_raw])))
    orc_map = {r[0]: r[1] for r in orcamentos_mensais_raw}
    ped_map = {r[0]: r[1] for r in pedidos_mensais_raw}
    
    def format_mes(iso_mes):
        # YYYY-MM -> MM/YYYY
        y, m = iso_mes.split('-')
        return f"{m}/{y}"

    return jsonify({
        "totalClientes": total_clientes,
        "totalOrcamentos": total_orcamentos,
        "pedidosConvertidos": pedidos_convertidos,
        "taxaConversao": taxa_conversao,
        "orcamentosEsteMes": orcamentos_mes,
        "valorConcluidosMes": valor_concluidos_mes,
        "ticketConcluidosMes": ticket_concluidos_mes,
        "novosClientesMes": 0, # Implementar se houver data_criacao no Cliente
        "chartData": {
            "labels": [format_mes(l) for l in labels_meses],
            "orcamentos": [orc_map.get(l, 0) for l in labels_meses],
            "pedidos": [ped_map.get(l, 0) for l in labels_meses]
        }
    })


