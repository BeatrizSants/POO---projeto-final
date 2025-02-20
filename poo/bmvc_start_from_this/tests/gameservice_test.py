import unittest
from unittest.mock import MagicMock, patch
from bottle import response
from app.models.gameservice import GameService

class TestGameService(unittest.TestCase):
    def setUp(self):
        """Configuração inicial antes de cada teste"""
        self.mock_app = MagicMock()
        self.game_service = GameService(self.mock_app)

        # Simular usuário autenticado corretamente
        self.mock_app.get_authenticated_username.return_value = "jogador1"
        self.mock_app.is_authenticated.return_value = True  

    def test_start_game_authenticated(self):
        """Testa iniciar o jogo com usuário autenticado"""
        self.mock_app.get_authenticated_username.return_value = "jogador1"

        with patch("app.models.gameservice.request") as mock_request:
            mock_request.get_cookie.return_value = "123"  # Simula que o cookie está presente

            result = self.game_service.start_game()

        self.assertIn("success", result)

    def test_start_game_unauthenticated(self):
        """Testa iniciar o jogo sem usuário autenticado"""
        self.mock_app.get_authenticated_username.return_value = None

        with patch("app.models.gameservice.request") as mock_request:
            mock_request.get_cookie.return_value = None  # Simula ausência de cookie

            result = self.game_service.start_game()

        self.assertIn("error", result)

    def test_add_score_authenticated(self):
        """Testa se a pontuação é adicionada corretamente"""
        self.mock_app.is_authenticated.return_value = True
        self.mock_app.get_authenticated_username.return_value = "jogador1"
        self.mock_app.update_score.return_value = 10  # Simula nova pontuação

        with patch("app.models.gameservice.request") as mock_request:
            mock_request.get_cookie.return_value = "123"

            result = self.game_service.add_score()

        self.assertIn('"score": 10', result)

    def test_take_score_authenticated(self):
        """Testa se a pontuação é reduzida corretamente"""
        self.mock_app.is_authenticated.return_value = True
        self.mock_app.get_authenticated_username.return_value = "jogador1"
        self.mock_app.update_score.return_value = 5  # Simula nova pontuação reduzida

        with patch("app.models.gameservice.request") as mock_request:
            mock_request.get_cookie.return_value = "123"

            result = self.game_service.take_score()

        self.assertIn('"score": 5', result)

    def test_end_game(self):
        """Testa se o jogo finaliza corretamente e retorna a pontuação final"""
        self.mock_app.is_authenticated.return_value = True
        self.mock_app.get_authenticated_username.return_value = "jogador1"
        self.mock_app.get_score.return_value = 20  # Simula pontuação final

        with patch("app.models.gameservice.request") as mock_request:
            mock_request.get_cookie.return_value = "123"

            result = self.game_service.end_game()

        self.assertIn('"score": 20', result)

    def test_get_score(self):
        """Testa se a pontuação acumulada do usuário pode ser recuperada corretamente"""
        self.mock_app.is_authenticated.return_value = True
        self.mock_app.get_authenticated_username.return_value = "jogador1"
        
        # Simula a pontuação acumulada
        self.game_service.accumulated_score = 15  # Define manualmente a pontuação acumulada

        with patch("app.models.gameservice.request") as mock_request:
            mock_request.get_cookie.return_value = "123"

            result = self.game_service.get_score()

        self.assertIn('"score": 15', result)  # Agora a pontuação é 15


if __name__ == '__main__':
    unittest.main()

#comando: python3 -m unittest -v tests.gameservice_test