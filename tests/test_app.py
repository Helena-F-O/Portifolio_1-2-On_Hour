import pytest
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the '/' route to ensure the correct template is rendered."""
    response = client.get('/')
    assert response.status_code == 200
    # Alterar a verificação para um conteúdo que você sabe que está na página
    assert b'On Hour - Home' in response.data  # Altere para algo que realmente está na página

def test_profile_route(client):
    """Test the '/profile' route."""
    response = client.get('/profile')
    assert response.status_code == 200
    # Check for a unique text or element that should be on the profile page
    assert b'On Hour - Profile' in response.data  # Example check for an h1 tag in profile

def test_regulamento_route(client):
    """Testa a rota '/regulamento'."""
    response = client.get('/regulamento')
    assert response.status_code == 200
    assert b'On Hour - Regulamento' in response.data  # Verifica se o template 'regulamento.html' é renderizado

def test_relatorio_route(client):
    """Test the '/relatorio' route to ensure the correct template is rendered."""
    response = client.get('/relatorio')
    assert response.status_code == 200
    # Verifique se o conteúdo esperado está na resposta, decodificando os dados.
    assert 'On Hour - Relatório' in response.data.decode('utf-8')
    
def test_add_certificado_get(client):
    """Testa a rota '/add_certificado' com GET."""
    response = client.get('/add_certificado')
    assert response.status_code == 200
    assert b'On Hour - Adicionar Certificado' in response.data  # Verifica se o template 'add_certificado.html' é renderizado

def test_signin_route(client):
    """Testa a rota '/sign-in'."""
    response = client.get('/sign-in')
    assert response.status_code == 200
    assert b'On Hour - Sign-In' in response.data  # Verifica se o template 'sign-in.html' é renderizado

def test_signup_route(client):
    """Testa a rota '/sign-up'."""
    response = client.get('/sign-up')
    assert response.status_code == 200
    assert b'On Hour - Sign-Up' in response.data  # Verifica se o template 'sign-up.html' é renderizado

def test_tables_route(client):
    """Testa a rota '/tables'."""
    response = client.get('/tables')
    assert response.status_code == 200
    assert b'On Hour - Certificados' in response.data  # Verifica se o template 'tables.html' é renderizado
