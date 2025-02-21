import unittest
from unittest.mock import MagicMock
from app.controllers.application import Application
from unittest.mock import patch
class TestApplicationAuth(unittest.TestCase):
    def setUp(self):
        """Configuração inicial antes de cada teste"""
        self.mock_datarecord = MagicMock()
        self.app = Application()
        self.app._Application__model = self.mock_datarecord  # Substitui model por mock
        self.app.get_session_id = MagicMock(return_value="sessao123")


    def test_authenticate_user_valid(self):
        """Testa login válido"""
        self.mock_datarecord.checkUser.return_value = "sessao123"
        self.mock_datarecord.getUserName.return_value = "jogador1"

        session_id, username = self.app.authenticate_user("jogador1", "senha123")

        self.assertEqual(session_id, "sessao123")
        self.assertEqual(username, "jogador1")
        self.mock_datarecord.checkUser.assert_called_with("jogador1", "senha123")

    def test_authenticate_user_invalid(self):
        """Testa login inválido"""
        self.mock_datarecord.checkUser.return_value = None

        session_id, username = self.app.authenticate_user("jogador1", "senhaErrada")

        self.assertIsNone(session_id)
        self.assertIsNone(username)

    def test_logout_user(self):
        """Testa logout do usuário"""
        self.app.get_session_id.return_value = "sessao123"  # Simula sessão ativa
        self.mock_datarecord.logout.return_value = None  # Simula logout bem-sucedido

        self.app.logout_user()

        self.assertIsNone(self.app._Application__current_username)
        self.mock_datarecord.logout.assert_called_with("sessao123")


    def test_create_user_success(self):
        """Testa criação de usuário novo"""
        self.mock_datarecord.user_exists.return_value = False
        
        # Mock para bcrypt.gensalt e bcrypt.hashpw
        with patch('bcrypt.gensalt', return_value=b'$2b$12$P4akoZFVWqy3RIV/olpzSONFfOb2DhaqWFcPuOF3mKazMSit8hAwO'):
            with patch('bcrypt.hashpw', return_value=b'$2b$12$P4akoZFVWqy3RIV/olpzSONFfOb2DhaqWFcPuOF3mKazMSit8hAwO'):
                result = self.app.create_user("novo_jogador", "senha123")

        self.assertTrue(result)
        self.mock_datarecord.book.assert_called_with("novo_jogador", b'$2b$12$P4akoZFVWqy3RIV/olpzSONFfOb2DhaqWFcPuOF3mKazMSit8hAwO')

    def test_create_user_already_exists(self):
        """Testa tentativa de criar usuário já existente"""
        self.mock_datarecord.user_exists.return_value = True

        result = self.app.create_user("jogador1", "senha123")

        self.assertFalse(result)
        self.mock_datarecord.book.assert_not_called()

    def test_is_authenticated_true(self):
        """Testa autenticação de usuário válido"""
        self.app.get_session_id.return_value = "sessao123"  # Simula um session_id válido
        self.mock_datarecord.getUserName.return_value = "jogador1"

        result = self.app.is_authenticated("jogador1")

        self.assertTrue(result)
        self.mock_datarecord.getUserName.assert_called_with("sessao123")


    def test_is_authenticated_false(self):
        """Testa autenticação falha (usuário não autenticado)"""
        self.mock_datarecord.getUserName.return_value = None

        result = self.app.is_authenticated("jogador1")

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

#comando: python3 -m unittest -v tests.application_test