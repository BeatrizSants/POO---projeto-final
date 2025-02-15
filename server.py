import asyncio
import websockets
import json

# Função para tratar as conexões
async def handle_login(websocket, path):
    # Receber dados do cliente
    credentials = await websocket.recv()
    credentials = json.loads(credentials)

    # Validar as credenciais (apenas exemplo simples)
    if credentials['username'] == 'Lara' and credentials['password'] == 'senha123':
        response = {
            "status": "success",
            "message": "Login bem-sucedido!"
        }
    else:
        response = {
            "status": "error",
            "message": "Credenciais inválidas!"
        }

    # Enviar resposta de volta ao cliente
    await websocket.send(json.dumps(response))

# Iniciar o servidor WebSocket
async def main():
    async with websockets.serve(handle_login, "localhost", 9999):
        await asyncio.Future()  # Mantém o servidor rodando

# Executar o servidor
asyncio.run(main())