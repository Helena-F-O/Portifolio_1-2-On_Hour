import mysql.connector
from mysql.connector import Error


# Variável de controle de login
usuario_logado = False


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            user='helena',
            password='1234',
            host='127.0.0.1',
            database='onhour1'
        )
        if connection.is_connected():
            print("Conexão com o banco de dados bem-sucedida")
            return connection
    except Exception as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None


def verificar_usuario(email, senha):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            usuario = cursor.fetchone()
            cursor.close()
            connection.close()

            if usuario and usuario['senha'] == senha:
                return usuario
            else:
                return None
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None


# api/models.py
def fetch_data(cpf_usuario):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT cpf, usuario, email, senha, horas_exigidas
            FROM usuarios
            WHERE cpf = %s  -- Filtro pelo CPF
            """
            cursor.execute(query, (cpf_usuario,))
            data = cursor.fetchall()
            # Verificar o conteúdo retornado
            print("Dados retornados do banco de dados:", data)
            cursor.close()
            connection.close()
            return data
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha ao conectar ao banco de dados")
    return []


def fetch_certificados(cpf_usuario):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT certificados.id_certificado,
            certificados.certificado,
            certificados.horas,
            certificados.data_emissao,
            categorias.categoria AS categoria
            FROM certificados
            JOIN categorias
            ON certificados.categoria_id = categorias.id_categoria
            WHERE certificados.usuario_cpf = %s
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


def inserir_usuario(cpf, usuario, email, senha, horas_exigidas):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO usuarios (cpf, usuario, email, senha, horas_exigidas)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (cpf, usuario, email, senha, horas_exigidas))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Erro ao inserir usuário: {e}")  # Log do erro
            connection.rollback()  # Desfaz as alterações em caso de erro
            return False
    else:
        print("Falha ao conectar ao banco de dados")
    return False


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
            LEFT JOIN certificados
            ON categorias.id_categoria = certificados.categoria_id
            GROUP BY categorias.id_categoria,
            categorias.categoria, categorias.horas_maximas
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


def fetch_categorias_cpf(cpf_usuario):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT
                categorias.id_categoria,
                categorias.categoria,
                categorias.horas_maximas,
                COALESCE(SUM(certificados.horas), 0) AS total_horas,
                COALESCE((SUM(certificados.horas) / categorias.horas_maximas) * 100, 0) AS percentual
            FROM categorias
            LEFT JOIN certificados
                ON categorias.id_categoria = certificados.categoria_id
                AND certificados.usuario_cpf = %s  -- Filtro pelo CPF
            GROUP BY categorias.id_categoria, categorias.categoria, categorias.horas_maximas
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


def delete_user_by_cpf(cpf):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM usuarios WHERE cpf = %s"
            cursor.execute(query, (cpf,))
            connection.commit()
            row_count = cursor.rowcount
            cursor.close()
            connection.close()
            return row_count > 0  # Retorna True se uma linha foi afetada
        except Error as e:
            print(f"Erro ao excluir o usuário: {e}")
            return False
    else:
        print("Falha ao conectar ao banco de dados.")
        return False


def update_certificado(id_certificado, certificado, horas, data_emissao, categoria):
    # Exemplo de código SQL corrigido
    query = """UPDATE certificados
               SET certificado = %s, horas = %s, data_emissao = %s, categoria_id = %s
               WHERE id_certificado = %s"""
    params = (certificado, horas, data_emissao, categoria, id_certificado)
    # Execute a query no banco de dados
    execute_query(query, params)


def get_certificado_by_id(id_certificado):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT certificados.id_certificado,
                   certificados.certificado,
                   certificados.horas,
                   certificados.data_emissao,
                   certificados.categoria_id,
                   categorias.categoria AS categoria_nome
            FROM certificados
            JOIN categorias ON certificados.categoria_id = categorias.id_categoria
            WHERE id_certificado = %s
            """
            cursor.execute(query, (id_certificado,))
            certificado = cursor.fetchone()  # Recupera apenas um resultado
            cursor.close()
            connection.close()
            return certificado
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
    else:
        print("Falha ao conectar ao banco de dados")
    return None


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
    from datetime import datetime

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Estilos personalizados
    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(name='Normal', fontSize=6, leading=8)
    title_style = ParagraphStyle(name='Title', fontSize=8, leading=10, alignment=1)

    # Títulos principais
    elements.append(Paragraph("CENTRO UNIVERSITÁRIO CATÓLICA DE SANTA CATARINA", normal_style))
    elements.append(Paragraph("CURSO DE BACHARELADO EM ENGENHARIA DE SOFTWARE", normal_style))
    elements.append(Paragraph("FORMULÁRIO DE SOLICITAÇÃO DE VALIDAÇÃO DAS ATIVIDADES COMPLEMENTARES", title_style))

    # Informações de identificação
    data_identificacao = [
        ['IDENTIFICAÇÃO DO ACADÊMICO (A)', '', '', ''],
        ['Nome:', '', 'Fase:', 'Matrícula:']
    ]
    table_identificacao = Table(data_identificacao, colWidths=[4*cm, 8*cm, 2*cm, 4*cm])
    table_identificacao.setStyle(TableStyle([
        ('SPAN', (0, 0), (3, 0)),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(table_identificacao)

    # Cabeçalho da tabela de atividades
    data_header = [
        ['Dados Certificados', 'Para Uso da Instituição', '', '', '', ''],
        ['Nº', 'Atividade', 'Ano de Realização', 'Carga Horária', 'Deferido', 'Carga Horária Validada', 'Observações']
    ]

    # Linhas de atividades com os certificados
    data_atividades = []
    for i, cert in enumerate(certificados, start=1):
        data_emissao = cert.get('data_emissao', 'N/A')
        if data_emissao != 'N/A':
            try:
                if isinstance(data_emissao, str):
                    data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d')
                data_emissao_formatada = data_emissao.strftime('%d/%m/%Y')
            except ValueError:
                data_emissao_formatada = 'N/A'
        else:
            data_emissao_formatada = 'N/A'

        data_atividades.append([
            str(i),
            cert.get('certificado', 'N/A'),
            data_emissao_formatada,
            cert.get('horas', 'N/A'),
            '',
            '',
            ''
        ])

    # Completar linhas até 15
    for i in range(len(certificados) + 1, 16):
        data_atividades.append([str(i), '', '', '', '', '', ''])

    data_final = data_header + data_atividades

    table_atividades = Table(data_final, colWidths=[1*cm, 5*cm, 2*cm, 2*cm, 2*cm, 3*cm, 3*cm])
    table_atividades.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('SPAN', (0, 0), (3, 0)),
        ('SPAN', (4, 0), (6, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
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
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(table_assinatura)

    doc.build(elements)
    buffer.seek(0)
    return buffer
