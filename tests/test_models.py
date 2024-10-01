import unittest
from unittest.mock import patch, MagicMock
from unittest import TestCase
from unittest.mock import patch, MagicMock
from api.models import get_certificado_by_id
from api.models import (
    fetch_data,
    fetch_certificados,
    fetch_categorias,
    add_certificado,
    delete_certificado_by_id,
    update_certificado,
    get_certificado_by_id,
    fetch_certificados_participacao,
    fetch_certificados_outros,
    gerar_pdf_certificados
)

class TestModels(unittest.TestCase):

    @patch('api.models.get_db_connection')
    def test_get_certificado_by_id(self, mock_get_db_connection):
        # Configuração do mock
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id_certificado': 1,
            'certificado': 'Test Certificado',
            'horas': 10,
            'data_emissao': '2024-01-01',
            'categoria_id': 1
        }

        # Chamar a função
        result = get_certificado_by_id(1)

        # Verificações
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_certificado, certificado, horas, data_emissao, categoria_id "
            "FROM certificados WHERE id_certificado = %s",
            (1,)
        )
        
        # Verifica se o resultado é o esperado
        self.assertEqual(result, {
            'id_certificado': 1,
            'certificado': 'Test Certificado',
            'horas': 10,
            'data_emissao': '2024-01-01',
            'categoria_id': 1
        })

    @patch('api.models.get_db_connection')
    def test_add_certificado(self, mock_get_db_connection):
        # Configuração do mock
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Chamar a função
        success, error = add_certificado('Test Certificado', 10, '2024-01-01', 1, '123')

        # Verificações
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()
        self.assertTrue(success)
        self.assertIsNone(error)

    @patch('api.models.get_db_connection')
    def test_delete_certificado_by_id(self, mock_get_db_connection):
        # Configuração do mock
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1  # Simula que uma linha foi deletada

        # Chamar a função
        result = delete_certificado_by_id(1)

        # Verificações
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with("DELETE FROM certificados WHERE id_certificado = %s", (1,))
        self.assertTrue(result)

    @patch('api.models.get_db_connection')
    def test_get_certificado_by_id(self, mock_get_db_connection):
        # Configuração do mock
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'id_certificado': 1, 'certificado': 'Test Certificado', 'horas': 10, 'data_emissao': '2024-01-01', 'categoria_id': 1}

        # Chamar a função
        result = get_certificado_by_id(1)

        # Verificações
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT id_certificado, certificado, horas, data_emissao, categoria_id FROM certificados WHERE id_certificado = %s",
            (1,)
        )
        self.assertEqual(result, {'id_certificado': 1, 'certificado': 'Test Certificado', 'horas': 10, 'data_emissao': '2024-01-01', 'categoria_id': 1})

    @patch('api.models.get_db_connection')
    def test_fetch_certificados_participacao(self, mock_get_db_connection):
        # Configuração do mock
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{'categoria': 'Participação', 'total_horas': 20}]

        # Chamar a função
        result = fetch_certificados_participacao('123')

        # Verificações
        mock_get_db_connection.assert_called_once()
        mock_cursor.execute.assert_called_once()
        self.assertEqual(result, [{'categoria': 'Participação', 'total_horas': 20}])

    # Adicione mais testes para as outras funções conforme necessário...

if __name__ == '__main__':
    unittest.main()
