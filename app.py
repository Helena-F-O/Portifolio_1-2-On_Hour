from flask import (
    Flask, render_template, request, jsonify, url_for, redirect, session, flash
)
from api.models import fetch_data, fetch_certificados, fetch_categorias
from api.models import get_certificado_by_id
from api.models import gerar_pdf_certificados, delete_certificado_by_id
from api.models import fetch_certificados_participacao, delete_user_by_cpf
from api.models import fetch_certificados_outros, inserir_usuario
from api.models import get_db_connection, fetch_categorias_cpf
from mysql.connector import Error
from flask import send_file
from api.models import verificar_usuario
import os
import subprocess
# from flask_talisman import Talisman


app = Flask(__name__, static_folder='assets', template_folder='pages')
app.secret_key = 'minha_chave_temporaria'

# Configurações de segurança
# Talisman(app)


@app.route('/deploy', methods=['POST'])
def deploy():
    # Verifica se o webhook recebeu uma requisição válida
    if request.method == 'POST':
        try:
            # Executa o script de deploy
            subprocess.run(
                ['/bin/bash', '/home/ubuntu/Portifolio_1-2-On_Hour/deploy.sh'],
                check=True
            )
            return 'Deploy executado com sucesso!', 200
        except subprocess.CalledProcessError as e:
            return f'Erro ao executar deploy: {e}', 500
    return 'Método inválido', 400


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = verificar_usuario(email, senha)
        if usuario:
            session['usuario_id'] = usuario['cpf']
            session['usuario_nome'] = usuario['usuario']
            session['cpf_usuario'] = usuario['cpf']

            return redirect(url_for('index'))
        else:
            flash('Login ou senha incorretos. Tente novamente.', 'danger')
            return redirect(url_for('login'))

    return render_template('sign-in.html')  # Use seu template de login aqui


# Rota de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    cpf_usuario_logado = session.get('cpf_usuario')

    # Adicionando debug para verificar qual CPF está sendo usado
    print(f"CPF do usuário logado: {cpf_usuario_logado}")

    usuario_data = fetch_data(cpf_usuario_logado)
    # Dados gerais de certificados
    certificados_data = fetch_certificados(cpf_usuario_logado)
    # Dados das categorias
    categorias_data = fetch_categorias_cpf(cpf_usuario_logado)

    if usuario_data:
        usuario = usuario_data[0]
        print(f"Dados do usuário retornados: {usuario_data}")
    else:
        print("Usuário não encontrado, redirecionando para login.")
        return redirect(url_for('login'))

    # Buscando certificados da pessoa na categoria "Participação"
    certificados_participacao = fetch_certificados_participacao(
        cpf_usuario_logado
    )
    categorias_participacao = [
        certificado['categoria'] for certificado in certificados_participacao
    ]
    horas_participacao = [
        certificado['total_horas'] for certificado in certificados_participacao
    ]

    horas_participacao = horas_participacao or [0]
    categorias_participacao = categorias_participacao or [
        'Nenhuma Participação'
    ]

    print(f"Certificados de Participação: {certificados_participacao}")

    # Buscando certificados das categorias restantes
    certificados_outros = fetch_certificados_outros(cpf_usuario_logado)
    categorias_outros = [
        certificado['categoria'] for certificado in certificados_outros
    ]
    horas_outros = [
        certificado['total_horas'] for certificado in certificados_outros
    ]

    horas_outros = horas_outros or [0]
    categorias_outros = categorias_outros or [
        'Nenhuma Categoria'
    ]

    print(f"Certificados de Outras Categorias: {certificados_outros}")

    # Adicionando os cálculos ao contexto
    horas_exigidas = usuario.get('horas_exigidas', 0)
    total_horas_feitas = sum(
        categoria['total_horas'] for categoria in categorias_data
    )
    horas_faltantes = max(
        horas_exigidas - total_horas_feitas, 0
    )

    print(
        f"Total de horas feitas: {total_horas_feitas}, "
        f"Horas faltantes: {horas_faltantes}"
    )

    usuario['horas_feitas'] = total_horas_feitas
    usuario['horas_faltantes'] = horas_faltantes

    return render_template(
        'index.html',
        usuario=usuario,
        certificados=certificados_data,
        categorias=categorias_data,
        categorias_participacao=categorias_participacao,
        horas_participacao=horas_participacao,
        categorias_outros=categorias_outros,
        horas_outros=horas_outros
    )


@app.route('/profile')
def profile():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    cpf_usuario_logado = session.get('cpf_usuario')

    # Buscando os dados do usuário
    usuario_data = fetch_data(cpf_usuario_logado)
    if usuario_data:
        usuario = usuario_data[0]
    else:
        usuario = {}

    return render_template('profile.html', usuario=usuario)


@app.route('/regulamento')
def regulamento():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    return render_template('regulamento.html')


@app.route('/relatorio')
def relatorio():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    cpf_usuario_logado = session.get('cpf_usuario')

    data = fetch_certificados(cpf_usuario_logado)
    # Verificar os dados enviados ao template
    print("Dados passados para o template:", data)
    return render_template('relatorio.html', data=data)


@app.route('/sign-in')
def signin():
    return render_template('sign-in.html')


@app.route('/sign-up')
def signup():
    return render_template('sign-up.html')


@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    try:
        usuario = request.form['usuario']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = request.form['senha']
        horas_exigidas = request.form['horas_exigidas']

        # Tente inserir o usuário no banco de dados
        if inserir_usuario(
            cpf, usuario, email, senha, horas_exigidas
        ):
            # Mensagem de sucesso
            return 'Usuário cadastrado com sucesso!', 200
        else:
            # Mensagem de erro
            return (
                'Erro ao cadastrar usuário. Verifique os dados '
                'e tente novamente.', 400
            )
    except Exception as e:
        # Log do erro no console
        print(f"Erro ao cadastrar usuário: {e}")
        # Mensagem de erro genérica
        return 'Ocorreu um erro ao cadastrar o usuário.', 500


@app.route('/tables')
def tables():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    cpf_usuario_logado = session.get('cpf_usuario')

    certificados_data = fetch_certificados(cpf_usuario_logado)
    categorias_data = fetch_categorias_cpf(cpf_usuario_logado)
    return render_template(
        'tables.html',
        certificados=certificados_data,
        categorias=categorias_data
    )


@app.route('/pesquisar_certificados', methods=['GET', 'POST'])
def pesquisar_certificados():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    certificados = []
    if request.method == 'POST':
        cpf = request.form['cpf']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Consulta para buscar certificados pelo CPF
        cursor.execute(
            "SELECT * FROM certificados "
            "JOIN categorias "
            "ON certificados.categoria_id = categorias.id_categoria "
            "WHERE usuario_cpf = %s",
            (cpf,)
        )
        certificados = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template(
        'pesquisar_certificados.html',
        certificados=certificados
    )


@app.route('/add_certificado', methods=['GET', 'POST'])
def add_certificado():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        cpf_usuario_logado = session.get('cpf_usuario')
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
                INSERT INTO certificados (
                certificado, horas, data_emissao,
                categoria_id, usuario_cpf)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    nome_certificado,
                    horas,
                    data_emissao,
                    categoria_id,
                    cpf_usuario_logado
                ))
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({
                    'message':
                    'Certificado adicionado com sucesso!',
                    'status':
                    'success'
                })
            except Error as e:
                print(f"Erro ao inserir certificado: {e}")
                return jsonify({
                    'message':
                    'Erro ao adicionar o certificado.',
                    'status':
                    'danger'
                }), 500
        else:
            return jsonify({
                'message':
                'Falha ao conectar ao banco de dados.',
                'status':
                'danger'
            }), 500

    # Buscar categorias do banco de dados
    categorias = fetch_categorias()
    return render_template('add_certificado.html', categorias=categorias)


@app.route('/delete_certificado/<int:id_certificado>', methods=['POST'])
def delete_certificado(id_certificado):
    try:
        result = delete_certificado_by_id(
            id_certificado
        )
        if result:
            return jsonify({
                "status":
                "success",
                "message":
                "Certificado excluído com sucesso."
            }), 200
        else:
            return jsonify({
                "status":
                "error",
                "message":
                "Certificado não encontrado."
            }), 404
    except Exception as e:
        print(f"Erro ao excluir o certificado: {e}")
        return jsonify({
            "status":
            "error",
            "message":
            "Erro ao excluir certificado."
        }), 500


@app.route('/delete_user/<cpf>', methods=['POST'])
def delete_user(cpf):
    try:
        result = delete_user_by_cpf(cpf)
        if result:
            return jsonify({
                "status":
                "success",
                "message":
                "Usuário excluído com sucesso."
            }), 200
        else:
            return jsonify({
                "status":
                "error",
                "message":
                "Usuário não encontrado."
            }), 404
    except Exception as e:
        print(f"Erro ao excluir o usuário: {e}")
        return jsonify({
            "status":
            "error",
            "message":
            "Erro ao excluir usuário."
        }), 500


@app.route('/edit_certificado/<int:id_certificado>', methods=['GET', 'POST'])
def edit_certificado(id_certificado):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

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
                SET certificado = %s,
                horas = %s,
                data_emissao = %s,
                categoria_id = %s
                WHERE id_certificado = %s
                """
                cursor.execute(query, (
                    nome_certificado,
                    horas,
                    data_emissao,
                    categoria_id, id_certificado
                ))
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({
                    'message':
                    'Certificado atualizado com sucesso!',
                    'status':
                    'success'
                })
            except Error as e:
                print(f"Erro ao atualizar certificado: {e}")
                return jsonify({
                    'message':
                    'Erro ao atualizar o certificado.',
                    'status':
                    'danger'
                }), 500
        else:
            return jsonify({
                'message':
                'Falha ao conectar ao banco de dados.',
                'status':
                'danger'
            }), 500

    # Buscar o certificado pelo ID e as categorias para exibição
    certificado = get_certificado_by_id(id_certificado)
    categorias = fetch_categorias()
    return render_template(
        'edit_certificado.html',
        certificado=certificado,
        categorias=categorias
    )


@app.route('/download_certificados')
def download_certificados():

    cpf_usuario = session.get('cpf_usuario')
    # Conectar ao banco de dados e buscar dados dos certificados
    # Função para buscar os certificados do banco
    certificados = fetch_certificados(cpf_usuario)
    pdf_buffer = gerar_pdf_certificados(certificados)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name='certificados.pdf',
        mimetype='application/pdf'
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
