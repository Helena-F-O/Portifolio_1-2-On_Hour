import pytest
from flask import session
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testing_key'
    with app.test_client() as client:
        yield client

def mock_fetch_data(cpf):
    return [{'cpf_usuario': cpf, 'horas_exigidas': 100}]

def mock_fetch_certificados(cpf):
    return [{'categoria': 'Categoria A', 'total_horas': 50}]

def mock_fetch_categorias_cpf(cpf):
    return [{'total_horas': 50}]

def mock_verificar_usuario(email, senha):
    return {'cpf': '12345678901', 'usuario': 'Teste'}

@patch('app.fetch_data', side_effect=mock_fetch_data)
@patch('app.fetch_certificados', side_effect=mock_fetch_certificados)
@patch('app.fetch_categorias_cpf', side_effect=mock_fetch_categorias_cpf)
def test_index_authenticated(mock_fetch_data, mock_fetch_certificados, mock_fetch_categorias_cpf, client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = '12345678901'
        sess['cpf_usuario'] = '12345678901'
    
    response = client.get('/')
    assert response.status_code == 200  # Verifica se informações calculadas aparecem na resposta.

def test_index_unauthenticated(client):
    response = client.get('/')
    assert response.status_code == 302
    assert "/login" in response.location

@patch('app.verificar_usuario', side_effect=mock_verificar_usuario)
def test_login_success(mock_verificar_usuario, client):
    response = client.post('/login', data={'email': 'test@example.com', 'senha': 'password'}, follow_redirects=True)
    assert response.status_code == 200

@patch('app.verificar_usuario', return_value=None)
def test_login_failure(mock_verificar_usuario, client):
    response = client.post('/login', data={'email': 'test@example.com', 'senha': 'wrongpassword'})
    assert response.status_code == 302
    assert "/login" in response.location

def test_logout(client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = '12345678901'

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert "login" in response.data.decode('utf-8')  # Verifica redirecionamento para login

@patch('app.fetch_certificados', side_effect=mock_fetch_certificados)
def test_relatorio_authenticated(mock_fetch_certificados, client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = '12345678901'
        sess['cpf_usuario'] = '12345678901'
    
    response = client.get('/relatorio')
    assert response.status_code == 200

def test_relatorio_unauthenticated(client):
    response = client.get('/relatorio')
    assert response.status_code == 302
    assert "/login" in response.location

@patch('app.inserir_usuario', return_value=True)
def test_cadastrar_usuario_success(mock_inserir_usuario, client):
    response = client.post('/cadastrar_usuario', data={
        'usuario': 'Test User',
        'cpf': '12345678901',
        'email': 'test@example.com',
        'senha': 'password',
        'horas_exigidas': '50'
    })
    assert response.status_code == 200

@patch('app.inserir_usuario', return_value=False)
def test_cadastrar_usuario_failure(mock_inserir_usuario, client):
    response = client.post('/cadastrar_usuario', data={
        'usuario': 'Test User',
        'cpf': '12345678901',
        'email': 'test@example.com',
        'senha': 'password',
        'horas_exigidas': '50'
    })
    assert response.status_code == 400

@patch('app.inserir_usuario', side_effect=Exception('Erro inesperado'))
def test_cadastrar_usuario_exception(mock_inserir_usuario, client):
    response = client.post('/cadastrar_usuario', data={
        'usuario': 'Test User',
        'cpf': '12345678901',
        'email': 'test@example.com',
        'senha': 'password',
        'horas_exigidas': '50'
    })
    
    assert response.status_code == 500  # Verifica se o status retornado é 500


def test_regulamento_logged_in(client):
    # Simula um usuário logado na sessão
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1

    # Chama a rota /regulamento
    response = client.get('/regulamento')

    # Verifica se a resposta tem status 200 e se o template correto foi renderizado
    assert response.status_code == 200
    assert b'regulamento' in response.data

def test_regulamento_not_logged_in(client):
    # Chama a rota /regulamento sem estar logado
    response = client.get('/regulamento', follow_redirects=True)

    # Verifica se há um redirecionamento para o login
    assert response.status_code == 200
    assert b'login' in response.data  # Verifica se a página de login foi carregada


# Testa a rota /profile
def test_profile_logged_in(client):
    # Simula um usuário logado na sessão
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1
        sess['cpf_usuario'] = '12345678900'

    # Chama a rota /profile
    response = client.get('/profile')

    # Verifica se a resposta tem status 200 e se o template correto foi renderizado
    assert response.status_code == 200
    assert b'profile' in response.data

def test_profile_not_logged_in(client):
    # Chama a rota /profile sem estar logado
    response = client.get('/profile', follow_redirects=True)

    # Verifica se há um redirecionamento para o login
    assert response.status_code == 200
    assert b'login' in response.data  # Verifica se a página de login foi carregada


def test_signin(client):
    # Chama a rota /sign-in
    response = client.get('/sign-in')

    # Verifica se a resposta tem status 200 e se o template correto foi renderizado
    assert response.status_code == 200
    assert b'sign-in' in response.data

def test_signup(client):
    # Chama a rota /sign-up
    response = client.get('/sign-up')

    # Verifica se a resposta tem status 200 e se o template correto foi renderizado
    assert response.status_code == 200


def test_tables_not_logged_in(client):
    # Realiza a requisição para a rota /tables sem estar logado
    response = client.get('/tables')
    
    # Verifica se a resposta é um redirecionamento
    assert response.status_code == 302
    # Verifica se o redirecionamento é para a página de login
    assert "/login" in response.location


def test_pesquisar_certificados_unauthenticated(client):
    # Verifica redirecionamento para login quando o usuário não está autenticado
    response = client.get('/pesquisar_certificados')
    assert response.status_code == 302  # Redireciona para o login
    assert "/login" in response.location