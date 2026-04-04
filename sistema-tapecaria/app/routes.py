from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from datetime import datetime

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
    OrcamentoCor
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
    

@main.route("/orcamento/<int:id_veiculo>")
def form_orcamento(id_veiculo):

    veiculo = Veiculo.query.get_or_404(id_veiculo)
    cliente = veiculo.cliente

    tecidos = Tecido.query.all()
    espumas = Espuma.query.all()
    costuras = Costura.query.all()
    cores = Cor.query.all()
    
    data_br = datetime.today().strftime("%d/%m/%Y")

    return render_template(
        "form_orcamento.html",
        cliente=cliente,
        veiculo=veiculo,
        tecidos=tecidos,
        espumas=espumas,
        costuras=costuras,
        cores=cores,
        today=data_br
    )
# =========================
# SALVAR ORÇAMENTO
# =========================
from datetime import datetime
from flask import request, redirect, url_for

@main.route("/salvar_orcamento", methods=["POST"])
def salvar_orcamento():

    id_veiculo = request.form.get("id_veiculo")

    # data
    data_str = request.form.get("dat_orcamento")
    dat_orcamento = datetime.strptime(data_str, "%d/%m/%Y").date()

    # números
    qtd_bancos = int(request.form.get("qtd_bancos") or 0)
    qtd_apoio_cabeca = int(request.form.get("qtd_apoio_cabeca") or 0)

    valor = float(request.form.get("valor") or 0)

    # booleanos
    bool_original = True if request.form.get("bool_original") else False
    bool_logo_prensada = True if request.form.get("bool_logo_prensada") else False
    bool_espuma = True if request.form.get("bool_espuma") else False

    obs = request.form.get("obs")

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
        valor=valor,
        obs=obs
    )

    db.session.add(novo_orcamento)
    db.session.commit()

    id_orcamento = novo_orcamento.id_orcamento

    # =========================
    # TECIDOS
    # =========================

    tecidos = request.form.getlist("tecidos")

    for tecido_id in tecidos:

        obs_item = request.form.get(f"obs_tecido_{tecido_id}")

        item = OrcamentoTecido(
            id_orcamento=id_orcamento,
            id_tecido=tecido_id,
            obs_item=obs_item
        )

        db.session.add(item)

    # =========================
    # COSTURAS
    # =========================

    costuras = request.form.getlist("costuras")

    for costura_id in costuras:

        obs_item = request.form.get(f"obs_costura_{costura_id}")

        item = OrcamentoCostura(
            id_orcamento=id_orcamento,
            id_costura=costura_id,
            obs_item=obs_item
        )

        db.session.add(item)

    # =========================
    # CORES
    # =========================

    cores = request.form.getlist("cores")

    for cor_id in cores:

        obs_item = request.form.get(f"obs_cor_{cor_id}")

        item = OrcamentoCor(
            id_orcamento=id_orcamento,
            id_cor=cor_id,
            obs_item=obs_item
        )

        db.session.add(item)

    # =========================
    # ESPUMAS
    # =========================

    if bool_espuma:

        espumas = request.form.getlist("espumas")

        for espuma_id in espumas:

            obs_item = request.form.get(f"obs_espuma_{espuma_id}")

            item = OrcamentoEspuma(
                id_orcamento=id_orcamento,
                id_espuma=espuma_id,
                obs_item=obs_item
            )

            db.session.add(item)

    db.session.commit()

    return redirect(url_for("main.lista_orcamentos"))


@main.route("/orcamentos")
def lista_orcamentos():

    orcamentos = Orcamento.query.order_by(Orcamento.dat_orcamento.desc()).all()

    return render_template(
        "lista_orcamentos.html",
        orcamentos=orcamentos
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

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    elementos = []

    # ======================
    # ESTILOS PADRÃO
    # ======================
    estilo_tabela = TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
    ])

    valor_style = ParagraphStyle(
        "Valor",
        parent=styles["Heading2"],
        textColor=colors.red,
        alignment=1,  # centralizado
        fontSize=14
    )

    # ======================
    # CABEÇALHO
    # ======================
    logo_path = os.path.join(
        current_app.root_path,
        "static/imagens/Identidade_visual/logo_zito.png"
    )
    logo = Image(logo_path, width=4*cm, height=4*cm)

    dados_empresa = Paragraph("""
    <b>Zito Tapeçaria para Autos</b><br/>
    Rua Dr. Laerte Machado Guimarães, 241 – São Benedito<br/>
    Pindamonhangaba – SP<br/>
    Tel. (12) 3642-4713 / 3522-4713<br/>
    CNPJ 74.458.852/0001-63<br/>
    I.E. 528.045.963.113<br/>
    Email: zitotapecaria@gmail.com
    """, styles["Normal"])

    cabecalho = Table([[dados_empresa, logo]], colWidths=[14*cm,4*cm])
    cabecalho.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ALIGN", (0,0), (0,0), "LEFT"),
        ("ALIGN", (1,0), (1,0), "RIGHT"),
    ]))

    elementos.append(cabecalho)
    elementos.append(Spacer(1,20))

    # ======================
    # CLIENTE
    # ======================
    telefone = cliente.telefones[0].telefone if cliente.telefones else ""
    elementos.append(Paragraph(f"<b>Cliente:</b> {cliente.nome}", styles["Normal"]))
    elementos.append(Paragraph(f"<b>Telefone:</b> {telefone}", styles["Normal"]))
    elementos.append(Spacer(1,20))

    # ======================
    # VEÍCULO
    # ======================
    dados_veiculo = [
        ["Modelo", veiculo.modelo],
        ["Placa", veiculo.placa],
        ["Data do orçamento", str(orcamento.dat_orcamento)]
    ]
    tabela_veiculo = Table(dados_veiculo)
    tabela_veiculo.setStyle(estilo_tabela)
    elementos.append(tabela_veiculo)
    elementos.append(Spacer(1,20))

    # ======================
    # SERVIÇOS
    # ======================
    servicos = [
        ["Quantidade de bancos", orcamento.qtd_bancos],
        ["Apoios de cabeça", orcamento.qtd_apoio_cabeca],
        ["Manter padrão original", "Sim" if orcamento.bool_original else "Não"],
        ["Logo prensada", "Sim" if orcamento.bool_logo_prensada else "Não"],
        ["Troca de espuma", "Sim" if orcamento.bool_espuma else "Não"]
    ]
    tabela_servicos = Table(servicos)
    tabela_servicos.setStyle(estilo_tabela)
    elementos.append(tabela_servicos)
    elementos.append(Spacer(1,20))

    # ======================
    # MATERIAIS
    # ======================
    def tabela_materiais(titulo, cabecalho, dados):
        elementos.append(Paragraph(f"<b>{titulo}</b>", styles["Heading4"]))
        tabela = Table([cabecalho] + dados)
        tabela.setStyle(estilo_tabela)
        elementos.append(tabela)
        elementos.append(Spacer(1,15))

    if tecidos:
        tabela_materiais("Tecidos", ["Material","Observação"],
            [[item.tecido.material, item.obs_item or ""] for item in tecidos])

    if costuras:
        tabela_materiais("Costuras", ["Tipo","Observação"],
            [[item.costura.tipo, item.obs_item or ""] for item in costuras])

    if cores:
        tabela_materiais("Cores de Linha", ["Cor","Observação"],
            [[item.cor.descricao, item.obs_item or ""] for item in cores])

    if espumas:
        tabela_materiais("Espumas", ["Tipo","Observação"],
            [[item.espuma.tipo, item.obs_item or ""] for item in espumas])

    # ======================
    # VALOR
    # ======================
    elementos.append(Spacer(1,20))
    elementos.append(Paragraph(f"Valor do orçamento: R$ {orcamento.valor}", valor_style))
    elementos.append(Spacer(1,20))

    # ======================
    # OBSERVAÇÕES
    # ======================
    if orcamento.obs:
        elementos.append(Paragraph(f"<b>Observações:</b> {orcamento.obs}", styles["Normal"]))
        elementos.append(Spacer(1,20))

    # ======================
    # ASSINATURA
    # ======================
    assinatura = Table([
        ["",""],
        ["___________________________","___________________________"],
        ["Cliente","Zito Tapeçaria"]
    ], colWidths=[9*cm,9*cm])
    assinatura.setStyle(TableStyle([
        ("ALIGN", (0,1), (-1,-1), "CENTER"),
        ("LINEABOVE", (0,1), (0,1), 0.5, colors.black),
        ("LINEABOVE", (1,1), (1,1), 0.5, colors.black),
    ]))
    elementos.append(Spacer(1,40))
    elementos.append(assinatura)

    # ======================
    # GERAR PDF
    # ======================
    doc.build(elementos)
    buffer.seek(0)

    # Normaliza os textos para evitar espaços e acentos no nome do arquivo
    modelo = slugify(veiculo.modelo)
    cliente_nome = slugify(cliente.nome)

    nome_arquivo = f"orc_{modelo}_{cliente_nome}_{orcamento.id_orcamento}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype="application/pdf"
)

