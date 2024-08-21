# api/models.py
import mysql.connector
from mysql.connector import Error

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
            SELECT categorias.categoria, 
                   categorias.horas_maximas, 
                   COALESCE(SUM(certificados.horas), 0) AS total_horas, 
                   COALESCE((SUM(certificados.horas) / categorias.horas_maximas) * 100, 0) AS percentual
            FROM categorias
            LEFT JOIN certificados ON categorias.id_categoria = certificados.categoria_id
            GROUP BY categorias.categoria, categorias.horas_maximas
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
