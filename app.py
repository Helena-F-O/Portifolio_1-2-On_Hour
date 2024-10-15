from flask import Flask, render_template, request, jsonify
from api.models import fetch_data, fetch_certificados, fetch_categorias
from api.models import get_certificado_by_id, update_certificado
from api.models import gerar_pdf_certificados, delete_certificado_by_id
from api.models import fetch_certificados_participacao
from api.models import fetch_certificados_outros
from api.models import get_db_connection
from mysql.connector import Error
from flask import send_file
import bcrypt
from flask import redirect, url_for, session
from functools import wraps
from flask import session, redirect, url_for
import bcrypt

from flask import Flask, session, redirect, url_for, request, render_template

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash  # Certifique-se de que essa linha está presente
from api.models import fetch_data



app = Flask(__name__, static_folder='assets', template_folder='pages')

# Adicionando a chave secreta para a segurança da sessão
app.secret_key = 'e58c865a06f2a3b1cfc8c5ff78d75a62'  # Substitua pela chave gerada ou altere por outra string

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # Obtendo todos os usuários do banco de dados
        usuarios = fetch_data()
        
        # Verifica se as credenciais estão corretas
        usuario_encontrado = next((usuario for usuario in usuarios if usuario['email'] == email), None)

        if usuario_encontrado and check_password_hash(usuario_encontrado['senha'], senha):
            # Armazena o ID do usuário na sessão
            session['user_id'] = usuario_encontrado['cpf']  # Armazenar cpf ou id como preferir
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))  # Redireciona para a página inicial
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
    
    return render_template('sign-in.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove o ID do usuário da sessão
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('sign-in'))


@app.route('/')
def index():
    usuario_data = fetch_data()
    certificados_data = fetch_certificados()  # Dados gerais de certificados
    categorias_data = fetch_categorias()  # Dados das categorias

    if usuario_data:
        usuario = usuario_data[0]
        cpf_usuario = usuario.get('cpf', '12345678900') 
    else:
        usuario = {}
        cpf_usuario = '12345678900'  

    # Buscando certificados da pessoa na categoria "Participação"
    certificados_participacao = fetch_certificados_participacao(cpf_usuario)
    categorias_participacao = [certificado['categoria'] for certificado in certificados_participacao]
    horas_participacao = [certificado['total_horas'] for certificado in certificados_participacao]

    horas_participacao = horas_participacao or [0]  # Default to zero if empty
    categorias_participacao = categorias_participacao or ['Nenhuma Participação']  # Default label if empty

    # Buscando certificados das categorias restantes
    certificados_outros = fetch_certificados_outros(cpf_usuario)
    categorias_outros = [certificado['categoria'] for certificado in certificados_outros]
    horas_outros = [certificado['total_horas'] for certificado in certificados_outros]

    horas_outros = horas_outros or [0]  # Default to zero if empty
    categorias_outros = categorias_outros or ['Nenhuma Categoria']  # Default label if empty

    # Adicionando os cálculos ao contexto
    horas_exigidas = usuario.get('horas_exigidas', 0)
    total_horas_feitas = sum(categoria['total_horas'] for categoria in categorias_data)
    horas_faltantes = max(horas_exigidas - total_horas_feitas, 0)

    usuario['horas_feitas'] = total_horas_feitas
    usuario['horas_faltantes'] = horas_faltantes

    return render_template('index.html', usuario=usuario, certificados=certificados_data, categorias=categorias_data, categorias_participacao=categorias_participacao, horas_participacao=horas_participacao, categorias_outros=categorias_outros, horas_outros=horas_outros)


@app.route('/profile')
def profile():
    # Buscando os dados do banco usando as funções do models.py
    usuario_data = fetch_data()  # Retorna uma lista de dicionários

    # Para este exemplo, vou considerar que você está interessado apenas no primeiro usuário retornado
    if usuario_data:
        usuario = usuario_data[0]  # Pegando o primeiro usuário
    else:
        usuario = {}

    # Renderizando o template com os dados do usuário
    return render_template('profile.html', usuario=usuario)


@app.route('/regulamento')
def regulamento():
    return render_template('regulamento.html')


@app.route('/relatorio')
def relatorio():
    data = fetch_certificados()
    print("Dados passados para o template:", data)  # Verificar os dados enviados ao template
    return render_template('relatorio.html', data=data)


@app.route('/sign-in')
def signin():
    return render_template('sign-in.html')


@app.route('/sign-up')
def signup():
    return render_template('sign-up.html')


@app.route('/tables')
def tables():
    certificados_data = fetch_certificados()
    categorias_data = fetch_categorias()
    return render_template('tables.html', certificados=certificados_data, categorias=categorias_data)

@app.route('/pesquisar_certificados', methods=['GET', 'POST'])
def pesquisar_certificados():
    certificados = []
    if request.method == 'POST':
        cpf = request.form['cpf']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Consulta para buscar certificados pelo CPF
        cursor.execute("SELECT * FROM certificados JOIN categorias ON certificados.categoria_id = categorias.id_categoria WHERE usuario_cpf = %s", (cpf,))
        certificados = cursor.fetchall()

        cursor.close()
        conn.close()
    
    return render_template('pesquisar_certificados.html', certificados=certificados)


@app.route('/notifications')
def notifications():
    return render_template('notifications.html')


@app.route('/add_certificado', methods=['GET', 'POST'])
def add_certificado():
    if request.method == 'POST':
        nome_certificado = request.form['nome_certificado']
        horas = request.form['horas']
        data_emissao = request.form['data_emissao']
        categoria_id = request.form['categoria']

        # Inserindo o certificado no banco de dados
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO certificados (certificado, horas, data_emissao, categoria_id, usuario_cpf)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nome_certificado, horas, data_emissao, categoria_id, '12345678900'))
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({'message': 'Certificado adicionado com sucesso!', 'status': 'success'})
            except Error as e:
                print(f"Erro ao inserir certificado: {e}")
                return jsonify({'message': 'Erro ao adicionar o certificado.', 'status': 'danger'}), 500
        else:
            return jsonify({'message': 'Falha ao conectar ao banco de dados.', 'status': 'danger'}), 500

    # Buscar categorias do banco de dados
    categorias = fetch_categorias()
    return render_template('add_certificado.html', categorias=categorias)


@app.route('/delete_certificado/<int:id_certificado>', methods=['POST'])
def delete_certificado(id_certificado):
    try:
        result = delete_certificado_by_id(id_certificado)
        if result:
            return jsonify({"status": "success", "message": "Certificado excluído com sucesso."}), 200
        else:
            return jsonify({"status": "error", "message": "Certificado não encontrado."}), 404
    except Exception as e:
        print(f"Erro ao excluir o certificado: {e}")
        return jsonify({"status": "error", "message": "Erro ao excluir certificado."}), 500


@app.route('/edit_certificado/<int:id_certificado>', methods=['GET', 'POST'])
def edit_certificado(id_certificado):
    if request.method == 'POST':
        nome_certificado = request.form['nome_certificado']
        horas = request.form['horas']
        data_emissao = request.form['data_emissao']
        categoria_id = request.form['categoria']

        # Atualizando o certificado no banco de dados
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                UPDATE certificados
                SET certificado = %s, horas = %s, data_emissao = %s, categoria_id = %s
                WHERE id_certificado = %s
                """
                cursor.execute(query, (nome_certificado, horas, data_emissao, categoria_id, id_certificado))
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({'message': 'Certificado atualizado com sucesso!', 'status': 'success'})
            except Error as e:
                print(f"Erro ao atualizar certificado: {e}")
                return jsonify({'message': 'Erro ao atualizar o certificado.', 'status': 'danger'}), 500
        else:
            return jsonify({'message': 'Falha ao conectar ao banco de dados.', 'status': 'danger'}), 500

    # Buscar o certificado pelo ID e as categorias para exibição
    certificado = get_certificado_by_id(id_certificado)
    categorias = fetch_categorias()
    return render_template('edit_certificado.html', certificado=certificado, categorias=categorias)


@app.route('/download_certificados')
def download_certificados():
    # Conectar ao banco de dados e buscar dados dos certificados
    certificados = fetch_certificados()  # Função para buscar os certificados do banco
    pdf_buffer = gerar_pdf_certificados(certificados)
    return send_file(pdf_buffer, as_attachment=True, download_name='certificados.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
