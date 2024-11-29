import pytest
from unittest.mock import patch, MagicMock
from mysql.connector import Error
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
    # Chama a função e verifica se retorna None quando ocorre uma falha
    connection = get_db_connection()
    assert connection is None  # A função deve retornar None em caso de falha

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

# Mock da função de inserir usuário
@patch('api.models.get_db_connection')
def test_inserir_usuario_failure(mock_get_connection):
    # Mock de conexão e cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    # Quando a função get_db_connection for chamada, retornará a conexão mockada
    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Simula a falha na execução do comando SQL
    mock_cursor.execute.side_effect = Error("Falha na inserção")

    # Chama a função inserir_usuario
    result = inserir_usuario('12345678900', 'Test User', 'test@example.com', 'password', 100)

    # Verifica se o resultado é False, indicando falha na inserção
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


@patch('api.models.get_db_connection')
def test_add_certificado_success(mock_get_connection, mock_db_connection):
    # Mock da conexão e cursor
    mock_connection, mock_cursor = mock_db_connection
    mock_get_connection.return_value = mock_connection

    # Dados de entrada
    nome_certificado = "Certificado Python"
    horas = 10
    data_emissao = "2024-11-27"
    categoria_id = 1
    cpf_usuario = "12345678901"

    # Chama a função que será testada
    result, error = add_certificado(nome_certificado, horas, data_emissao, categoria_id, cpf_usuario)

    # Verifica se a função retornou sucesso
    assert result is True
    assert error is None
    mock_cursor.execute.assert_called_once()

@patch('api.models.get_db_connection')
def test_add_certificado_failure(mock_get_connection, mock_db_connection):
    # Mock da conexão e cursor
    mock_connection, mock_cursor = mock_db_connection
    mock_get_connection.return_value = mock_connection

    # Simula um erro ao executar o comando SQL
    mock_cursor.execute.side_effect = Error("Erro ao inserir no banco de dados")

    # Dados de entrada
    nome_certificado = "Certificado Python"
    horas = 10
    data_emissao = "2024-11-27"
    categoria_id = 1
    cpf_usuario = "12345678901"

    # Chama a função que será testada
    result, error = add_certificado(nome_certificado, horas, data_emissao, categoria_id, cpf_usuario)

    # Verifica se a função retornou falha
    assert result is False
    assert error == "Erro ao inserir no banco de dados"
    mock_cursor.execute.assert_called_once()

@patch('api.models.get_db_connection')
def test_delete_user_by_cpf_success(mock_get_connection, mock_db_connection):
    # Mock da conexão e cursor
    mock_connection, mock_cursor = mock_db_connection
    mock_get_connection.return_value = mock_connection

    # Simula que uma linha foi afetada pelo comando DELETE
    mock_cursor.rowcount = 1

    # Chama a função que será testada
    result = delete_user_by_cpf("12345678901")

    # Verifica se a função retornou True
    assert result is True
    mock_cursor.execute.assert_called_once_with("DELETE FROM usuarios WHERE cpf = %s", ("12345678901",))


@patch('api.models.get_db_connection')
def test_delete_user_by_cpf_no_user_found(mock_get_connection, mock_db_connection):
    # Mock da conexão e cursor
    mock_connection, mock_cursor = mock_db_connection
    mock_get_connection.return_value = mock_connection

    # Simula que nenhuma linha foi afetada pelo comando DELETE
    mock_cursor.rowcount = 0

    # Chama a função que será testada
    result = delete_user_by_cpf("12345678901")

    # Verifica se a função retornou False
    assert result is False
    mock_cursor.execute.assert_called_once_with("DELETE FROM usuarios WHERE cpf = %s", ("12345678901",))


@patch('api.models.get_db_connection')
def test_delete_user_by_cpf_failure(mock_get_connection, mock_db_connection):
    # Mock da conexão e cursor
    mock_connection, mock_cursor = mock_db_connection
    mock_get_connection.return_value = mock_connection

    # Simula uma exceção ao executar o comando SQL
    mock_cursor.execute.side_effect = Error("Erro ao excluir usuário")

    # Chama a função que será testada
    result = delete_user_by_cpf("12345678901")

    # Verifica se a função retornou False
    assert result is False
    mock_cursor.execute.assert_called_once_with("DELETE FROM usuarios WHERE cpf = %s", ("12345678901",))
