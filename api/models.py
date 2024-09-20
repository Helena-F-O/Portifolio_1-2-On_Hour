# api/models.py
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='1234',
            host='127.0.0.1',
            database='onhour1'
        )
        if connection.is_connected():
            print("Conexão com o banco de dados bem-sucedida")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# api/models.py
def fetch_data():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT cpf, usuario, email, senha, horas_exigidas FROM usuarios")
            data = cursor.fetchall()
            print("Dados retornados do banco de dados:", data)  # Verificar o conteúdo retornado
            cursor.close()
            connection.close()
            return data
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha ao conectar ao banco de dados")
    return []

def fetch_certificados():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT certificados.id_certificado, certificados.certificado, certificados.horas, categorias.categoria AS categoria
            FROM certificados
            JOIN categorias ON certificados.categoria_id = categorias.id_categoria
            """
            cursor.execute(query)
            data = cursor.fetchall()
            print("Dados retornados do banco de dados:", data)  # Verificar o conteúdo retornado
            cursor.close()
            connection.close()
            return data
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha ao conectar ao banco de dados")
    return []


def fetch_categorias():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT id_categoria, categoria, 
                   horas_maximas, 
                   COALESCE(SUM(certificados.horas), 0) AS total_horas, 
                   COALESCE((SUM(certificados.horas) / categorias.horas_maximas) * 100, 0) AS percentual
            FROM categorias
            LEFT JOIN certificados ON categorias.id_categoria = certificados.categoria_id
            GROUP BY categorias.id_categoria, categorias.categoria, categorias.horas_maximas
            """
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return data
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha ao conectar ao banco de dados")
    return []


def add_certificado(nome_certificado, horas, data_emissao, categoria_id, cpf_usuario):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO certificados (nome_certificado, horas, data_emissao, categoria_id, cpf_usuario)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome_certificado, horas, data_emissao, categoria_id, cpf_usuario))
        connection.commit()
        cursor.close()
        connection.close()
        return True, None
    except Error as e:
        return False, str(e)

def delete_certificado_by_id(id_certificado):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM certificados WHERE id_certificado = %s"
            cursor.execute(query, (id_certificado,))
            connection.commit()
            cursor.close()
            connection.close()
            return cursor.rowcount > 0  # Retorna True se alguma linha foi afetada
        except Error as e:
            print(f"Erro ao excluir o certificado: {e}")
            return False
    else:
        print("Falha ao conectar ao banco de dados")
        return False


def fetch_certificados_participacao(cpf_usuario):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT ca.categoria, SUM(c.horas) as total_horas
            FROM certificados c
            JOIN categorias ca ON c.categoria_id = ca.id_categoria
            WHERE c.usuario_cpf = %s AND ca.categoria LIKE '%Participação%'
            GROUP BY ca.categoria
            """
            cursor.execute(query, (cpf_usuario,))
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return data
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha ao conectar ao banco de dados")
    return []

def fetch_certificados_outros(cpf_usuario):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT ca.categoria, SUM(c.horas) as total_horas
            FROM certificados c
            JOIN categorias ca ON c.categoria_id = ca.id_categoria
            WHERE c.usuario_cpf = %s AND ca.categoria NOT LIKE '%Participação%'
            GROUP BY ca.categoria
            """
            cursor.execute(query, (cpf_usuario,))
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            return data
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha ao conectar ao banco de dados")
    return []

def gerar_pdf_certificados(certificados):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from io import BytesIO
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Estilos personalizados com fonte reduzida (tamanho 6)
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(name='Normal', fontSize=6, leading=8)
    title_style = ParagraphStyle(name='Title', fontSize=8, leading=10, alignment=1)

    # Título principal com fonte menor
    elements.append(Paragraph("CENTRO UNIVERSITÁRIO CATÓLICA DE SANTA CATARINA", normal_style))
    elements.append(Paragraph("CURSO DE BACHARELADO EM ENGENHARIA DE SOFTWARE", normal_style))
    elements.append(Paragraph("FORMULÁRIO DE SOLICITAÇÃO DE VALIDAÇÃO DAS ATIVIDADES COMPLEMENTARES", title_style))

    # Informações de identificação com tamanho ajustado
    data_identificacao = [
        ['IDENTIFICAÇÃO DO ACADÊMICO (A)', '', '', ''],
        ['Nome:', '', 'Fase:', 'Matrícula:']
    ]
    table_identificacao = Table(data_identificacao, colWidths=[4*cm, 8*cm, 2*cm, 4*cm])  # Ajuste do campo de "Nome"
    table_identificacao.setStyle(TableStyle([
        ('SPAN', (0, 0), (3, 0)),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 6),  # Fonte menor para a tabela
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),  # Reduzindo o padding vertical
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(table_identificacao)

    # Cabeçalho da tabela de atividades com nova organização e adição de "Para Uso da Instituição"
    data_header = [
        ['Dados Certificados', 'Para Uso da Instituição', '', '', '', ''],  # Primeira linha de cabeçalho
        ['Nº', 'Atividade', 'Ano de Realização', 'Carga Horária', 'Deferido', 'Carga Horária Validada', 'Observações']  # Segunda linha de cabeçalho
    ]
    
    # Linhas de atividades com nome da categoria
    data_atividades = []
    for i, cert in enumerate(certificados, start=1):
        # Definindo o ano da data de emissão
        ano_realizacao = cert.get('data_emissao', 'N/A').split('-')[0]  # Pega apenas o ano da data
        
        # Adiciona os dados à linha da tabela
        data_atividades.append([
            str(i),
            cert.get('certificado', 'N/A'),
            ano_realizacao,
            cert.get('horas', 'N/A'),
            '', '', ''
        ])

    # Completar linhas até 15
    for i in range(len(certificados) + 1, 16):
        data_atividades.append([str(i), '', '', '', '', '', ''])

    # Junta cabeçalho e atividades
    data_final = data_header + data_atividades

    # Ajuste das colunas para reduzir espaço desnecessário
    table_atividades = Table(data_final, colWidths=[1*cm, 5*cm, 2*cm, 2*cm, 2*cm, 3*cm, 3*cm])
    table_atividades.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('SPAN', (0, 0), (3, 0)),  # Mescla as primeiras 4 colunas na primeira linha
        ('SPAN', (4, 0), (6, 0)),  # Mescla as últimas 3 colunas na primeira linha
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 6),  # Fonte menor para a tabela
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),  # Reduz o padding para deixar mais compacto
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),  # Reduz o padding lateral
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(table_atividades)

    # Assinaturas
    data_assinatura = [
        ['Assinatura do Acadêmico (A):', '', 'Data da entrega:', ''],
        ['Assinatura do Professor (A) Responsável:', '', 'Data da validação:', '']
    ]
    table_assinatura = Table(data_assinatura, colWidths=[6*cm, 6*cm, 3*cm, 3*cm])
    table_assinatura.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 6),  # Fonte menor para a tabela de assinaturas
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),  # Padding reduzido
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(table_assinatura)

    # Gera o documento PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer