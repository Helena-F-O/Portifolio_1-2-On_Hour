from flask import Flask, render_template
from api.models import fetch_data
from api.models import fetch_certificados
from api.models import fetch_categorias


app = Flask(__name__, static_folder='assets', template_folder='pages')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


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


if __name__ == '__main__':
    app.run(debug=True)
