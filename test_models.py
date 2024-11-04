# tests/test_models.py
import pytest
from unittest.mock import patch, MagicMock

from api.models import fetch_data, fetch_certificados, fetch_categorias
from api.models import get_certificado_by_id, update_certificado
from api.models import gerar_pdf_certificados, delete_certificado_by_id
from api.models import fetch_certificados_participacao
from api.models import fetch_certificados_outros, inserir_usuario
from api.models import get_db_connection, fetch_categorias_cpf
from api.models import fetch_data
from api.models import verificar_usuario

import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

@pytest.fixture
def mock_db_connection():
    with patch('api.models.mysql.connector.connect') as mock_connect:
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        yield mock_connection

def test_verificar_usuario_success(mock_db_connection):
    # Configura o retorno do cursor e a consulta
    cursor_mock = MagicMock()
    
    # Mockando fetchone para retornar o usuário corretamente
    cursor_mock.fetchone.return_value = {'email': 'helena@gmail.com', 'senha': '1234'}
    mock_db_connection.cursor.return_value = cursor_mock

    # Chama a função que está sendo testada
    result = verificar_usuario('helena@gmail.com', '1234')
    
    # Verificações
    assert result is not None  # Certifique-se de que o resultado não é None
    assert result['email'] == 'helena@gmail.com'  # Verifique o email retornado

def test_verificar_usuario_failure(mock_db_connection):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = []
    mock_db_connection.cursor.return_value = cursor_mock

    result = verificar_usuario('test@example.com', 'wrong_password')
    assert result is None

def test_fetch_data_success(mock_db_connection):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [{'cpf': '12345678900', 'usuario': 'test_user'}]
    mock_db_connection.cursor.return_value = cursor_mock

    result = fetch_data('12345678900')
    assert len(result) == 1
    assert result[0]['usuario'] == 'test_user'

def test_fetch_data_failure(mock_db_connection):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = []
    mock_db_connection.cursor.return_value = cursor_mock

    result = fetch_data('non_existent_cpf')
    assert len(result) == 0

def test_inserir_usuario_success(mock_db_connection):
    cursor_mock = MagicMock()
    mock_db_connection.cursor.return_value = cursor_mock

    result = inserir_usuario('98765432155', 'test_user', 'test@example.com', '1234', 10)
    assert result is True

def test_inserir_usuario_failure(mock_db_connection):
    cursor_mock = MagicMock(side_effect=Exception("DB Error"))
    mock_db_connection.cursor.return_value = cursor_mock

    result = inserir_usuario('123456789', 'test_user', 'test', '1234', 10)
    assert result is True

def test_fetch_certificados_success(mock_db_connection):
    cursor_mock = MagicMock()
    cursor_mock.fetchall.return_value = [{'id_certificado': 1, 'certificado': 'Certificado A'}]
    mock_db_connection.cursor.return_value = cursor_mock

    result = fetch_certificados('12345678900')
    assert len(result) == 1
    assert result[0]['certificado'] == 'Certificado A'
