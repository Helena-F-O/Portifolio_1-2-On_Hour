from flask import Flask, render_template
from api.models import fetch_data
from api.models import fetch_certificados
from api.models import fetch_categorias
from api.models import fetch_certificados_participacao
from api.models import fetch_certificados_outros
from flask import Flask, render_template, request, redirect, url_for, flash
from api.models import get_db_connection
from mysql.connector import Error
from flask import send_file




app = Flask(__name__, static_folder='assets', template_folder='pages')

@app.route('/')
def index():
    usuario_data = fetch_data()
    certificados_data = fetch_certificados()  # Dados gerais de certificados
    categorias_data = fetch_categorias()  # Dados das categorias
    
    if usuario_data:
        usuario = usuario_data[0]
        cpf_usuario = usuario.get('cpf', '12345678900')  # Ajuste conforme necessário
    else:
        usuario = {}
        cpf_usuario = '12345678900'  # Valor padrão ou ajuste conforme necessário

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

@app.route('/download_certificados')
def download_certificados():
    # Função que retorna todos os certificados
    certificados = fetch_certificados()  # Substitua com sua função para buscar certificados

    pdf_buffer = gerar_pdf_certificados(certificados)
    return send_file(pdf_buffer, as_attachment=True, download_name='certificados.pdf', mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
