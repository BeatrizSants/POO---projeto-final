from app.controllers.score import Score
import unittest
from unittest.mock import MagicMock

class TestScore(unittest.TestCase):

    def setUp(self):
        """ Configuração inicial: cria um mock para data_record """
        self.mock_data_record = MagicMock()
        self.score = Score(self.mock_data_record)  # Instância da classe Score com o mock

    def test_update_score_success(self):
        #Testa atualização de pontuação bem-sucedida
        self.mock_data_record.update_score.return_value = True  # Simula sucesso

        result = self.score.update_score("session123", 50)

        self.assertEqual(result, {"status": "success", "message": "Pontuação atualizada"})
        self.mock_data_record.update_score.assert_called_once_with("session123", 50)

    def test_update_score_failure(self):
        #Testa falha ao atualizar pontuação
        self.mock_data_record.update_score.return_value = False  # Simula falha

        result = self.score.update_score("session123", 50)

        self.assertEqual(result, {"status": "error", "message": "Falha ao atualizar pontuação"})
        self.mock_data_record.update_score.assert_called_once_with("session123", 50)

    def test_get_score_success(self):
        #Testa a recuperação da pontuação do usuário 
        self.mock_data_record.get_score.return_value = 100  # Simula pontuação do usuário

        result = self.score.get_score("session123")

        self.assertEqual(result, 100)
        self.mock_data_record.get_score.assert_called_once_with("session123")

    def test_get_score_no_session(self):
        #Testa a recuperação da pontuação sem sessão válida
        result = self.score.get_score(None)

        self.assertEqual(result, {"status": "error", "message": "Sessão não encontrada"})

    def test_get_ranking(self):
        #esta a ordenação do ranking
        mock_users = [
            {"username": "Alice", "score": 150},
            {"username": "Bob", "score": 200},
            {"username": "Charlie", "score": 100}
        ]
        self.mock_data_record.get_all_users.return_value = mock_users

        ranking = self.score.get_ranking()

        expected_ranking = [
            {"username": "Bob", "score": 200},
            {"username": "Alice", "score": 150},
            {"username": "Charlie", "score": 100}
        ]
        self.assertEqual(ranking, expected_ranking)
        self.mock_data_record.get_all_users.assert_called_once()

if __name__ == '__main__':
    unittest.main()

#comando: python3 -m unittest -v tests.score_test