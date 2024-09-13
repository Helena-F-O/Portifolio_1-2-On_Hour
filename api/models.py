# api/models.py
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='1234',
            host='127.0.0.1',
            database='onhour'
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
            SELECT certificados.certificado, certificados.horas, categorias.categoria AS categoria
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
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    # Adiciona o título
    elements.append(Paragraph("Certificados", title_style))

    # Adiciona os dados dos certificados
    data = [['Certificado', 'Horas', 'Data de Emissão']]
    for cert in certificados:
        data.append([cert['certificado'], cert['horas'], cert['data_emissao']])

    # Cria a tabela
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d3d3d3'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica')
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
