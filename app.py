from flask import Flask, render_template
from api.models import fetch_data
from api.models import fetch_certificados
from api.models import fetch_categorias
from flask import Flask, render_template, request, redirect, url_for, flash
from api.models import get_db_connection
from mysql.connector import Error




app = Flask(__name__, static_folder='assets', template_folder='pages')

@app.route('/')
def index():
    # Buscando os dados do banco usando as funções do models.py
    usuario_data = fetch_data()  # Retorna uma lista de dicionários
    certificados_data = fetch_certificados()  # Retorna uma lista de dicionários
    categorias_data = fetch_categorias()  # Retorna uma lista de dicionários

    # Para este exemplo, vou considerar que você está interessado apenas no primeiro usuário retornado
    if usuario_data:
        usuario = usuario_data[0]  # Pegando o primeiro usuário
    else:
        usuario = {}

    # Calculando horas feitas e horas faltantes
    horas_exigidas = usuario.get('horas_exigidas', 0)
    total_horas_feitas = sum(categoria['total_horas'] for categoria in categorias_data)
    horas_faltantes = max(horas_exigidas - total_horas_feitas, 0)

    # Adicionando os cálculos ao contexto
    usuario['horas_feitas'] = total_horas_feitas
    usuario['horas_faltantes'] = horas_faltantes

    # Renderizando o template com os dados
    return render_template('index.html', usuario=usuario, certificados=certificados_data, categorias=categorias_data)

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
                INSERT INTO certificados (certificado, horas, data_emissao, categoria_id, cpf_usuario)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (nome_certificado, horas, data_emissao, categoria_id, '12345678900'))
                connection.commit()
                cursor.close()
                connection.close()
                flash('Certificado adicionado com sucesso!', 'success')
            except Error as e:
                print(f"Erro ao inserir certificado: {e}")
                flash('Erro ao adicionar o certificado.', 'danger')
        else:
            flash('Falha ao conectar ao banco de dados.', 'danger')

        return redirect(url_for('add_certificado'))

    # Buscar categorias do banco de dados
    categorias = fetch_categorias()
    return render_template('add_certificado.html', categorias=categorias)


if __name__ == '__main__':
    app.run(debug=True)
