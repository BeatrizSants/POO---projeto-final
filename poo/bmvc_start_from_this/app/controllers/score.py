
#classe responsavel por gerenciar atualização de pontuação
class Score:
    def __init__(self,data_record):
        self.data_record=data_record

    def update_score(self, session_id, points):
        if self.data_record.update_score(session_id, points):
            return {"status":"success", "message": "Pontuação atualizada"}
        else:
            return {"status":"error", "message": "Falha ao atualizar pontuação"}
        
    def get_score(self,session_id):
        if session_id:
            return self.data_record.get_score(session_id)
        return {"status": "error", "message": "Sessão não encontrada"}

    def get_ranking(self):
        users = self.data_record.get_all_users()
        return sorted(users, key=lambda x: x['score'], reverse=True)  # Ordenando por score
