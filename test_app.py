import unittest
from app import app  # Certifique-se de que o nome do seu arquivo é app.py

class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_index_redirects_if_not_logged_in(self):
        response = self.app.get('/')  # Follow redirects
        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        response = self.app.get('/login', follow_redirects=True)  # Follow any possible redirects
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        with self.app.session_transaction() as session:
            session['cpf_usuario'] = '12345678900'  # Simule um CPF para a sessão
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.app.session_transaction() as session:
            self.assertNotIn('cpf_usuario', session)  # Verifica se a sessão foi limpa

    def test_profile_page(self):
        with self.app.session_transaction() as session:
            session['cpf_usuario'] = '12345678900'  # Simule um CPF

        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 302)

    def test_add_certificado(self):
        with self.app.session_transaction() as session:
            session['cpf_usuario'] = '12345678900'  # Use CPF na sessão

        response = self.app.post('/add_certificado', data={
            'nome_certificado': 'Certificado Teste',
            'horas': 10,
            'data_emissao': '2024-11-01',
            'categoria': 1
        }, follow_redirects=True)  # Add follow_redirects=True
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
