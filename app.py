from flask import Flask, render_template
from api.models import fetch_data

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
    data = fetch_data()
    if not data:
        print("Nenhum dado encontrado para exibição.")
    else:
        print("Dados para exibição:", data)
    return render_template('relatorio.html', data=data)

@app.route('/sign-in')
def signin():
    return render_template('sign-in.html')

@app.route('/sign-up')
def signup():
    return render_template('sign-up.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

if __name__ == '__main__':
    app.run(debug=True)
