import pytest
from unittest.mock import patch, MagicMock
from api.models import (
    get_db_connection, verificar_usuario, fetch_data, fetch_certificados,
    inserir_usuario, fetch_categorias, fetch_categorias_cpf, add_certificado,
    delete_certificado_by_id, delete_user_by_cpf, update_certificado,
    get_certificado_by_id, fetch_certificados_participacao, fetch_certificados_outros,
    gerar_pdf_certificados
)

@pytest.fixture
def mock_db_connection():
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    yield mock_connection, mock_cursor

@patch('api.models.mysql.connector.connect')
def test_get_db_connection_success(mock_connect):
    mock_connect.return_value.is_connected.return_value = True
    connection = get_db_connection()
    assert connection.is_connected()
    mock_connect.assert_called_once()

@patch('api.models.mysql.connector.connect', side_effect=Exception("Database connection failed"))
def test_get_db_connection_failure(mock_connect):
    connection = get_db_connection()
    assert connection is None

@patch('api.models.get_db_connection')
def test_verificar_usuario_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = {'email': 'test@example.com', 'senha': 'password'}
    mock_get_connection.return_value = mock_connection

    result = verificar_usuario('test@example.com', 'password')
    assert result is not None
    assert result['email'] == 'test@example.com'

@patch('api.models.get_db_connection')
def test_verificar_usuario_invalid(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = None
    mock_get_connection.return_value = mock_connection

    result = verificar_usuario('test@example.com', 'wrongpassword')
    assert result is None

@patch('api.models.get_db_connection')
def test_fetch_data_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [{'cpf': '12345678901', 'usuario': 'Test User'}]
    mock_get_connection.return_value = mock_connection

    result = fetch_data('12345678901')
    assert len(result) == 1
    assert result[0]['usuario'] == 'Test User'

@patch('api.models.get_db_connection')
def test_fetch_certificados_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [{'certificado': 'Certificado A', 'horas': 5}]
    mock_get_connection.return_value = mock_connection

    result = fetch_certificados('12345678901')
    assert len(result) == 1
    assert result[0]['certificado'] == 'Certificado A'

@patch('api.models.get_db_connection')
def test_inserir_usuario_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_get_connection.return_value = mock_connection

    result = inserir_usuario('12345678901', 'Test User', 'test@example.com', 'password', 100)
    assert result is True

@patch('api.models.get_db_connection')
def test_inserir_usuario_failure(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_get_connection.return_value = mock_connection

    result = inserir_usuario('12345678901', 'Test User', '', 'password', 100)
    assert result is False

@patch('api.models.get_db_connection')
def test_fetch_categorias_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [{'id_categoria': 1, 'categoria': 'Participação'}]
    mock_get_connection.return_value = mock_connection

    result = fetch_categorias()
    assert len(result) == 1
    assert result[0]['categoria'] == 'Participação'

@patch('api.models.get_db_connection')
def test_fetch_categorias_cpf_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [{'categoria': 'Participação', 'total_horas': 10}]
    mock_get_connection.return_value = mock_connection

    result = fetch_categorias_cpf('12345678901')
    assert len(result) == 1
    assert result[0]['total_horas'] == 10

@patch('api.models.get_db_connection')
def test_delete_certificado_by_id_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.rowcount = 1
    mock_get_connection.return_value = mock_connection

    result = delete_certificado_by_id(1)
    assert result is True

@patch('api.models.get_db_connection')
def test_delete_certificado_by_id_failure(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.rowcount = 0
    mock_get_connection.return_value = mock_connection

    result = delete_certificado_by_id(1)
    assert result is False

@patch('api.models.get_db_connection')
def test_fetch_certificados_participacao_success(mock_get_connection, mock_db_connection):
    mock_connection, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [{'categoria': 'Participação', 'total_horas': 15}]
    mock_get_connection.return_value = mock_connection

    result = fetch_certificados_participacao('12345678901')
    assert len(result) == 1
    assert result[0]['categoria'] == 'Participação'

@patch('api.models.gerar_pdf_certificados')
def test_gerar_pdf_certificados(mock_gerar_pdf):
    certificados = [{'certificado': 'Certificado A', 'horas': 5}]
    buffer = gerar_pdf_certificados(certificados)
    assert buffer is not None
