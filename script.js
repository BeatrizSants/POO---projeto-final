document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault(); // Previne o envio do formulário

        const socket = new WebSocket('ws://localhost:9999'); // Cria a conexão WebSocket

        socket.onopen = function() {
            console.log("Conexão WebSocket estabelecida.");
            const credentials = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            };

            socket.send(JSON.stringify(credentials)); // Envia as credenciais para o servidor
        };

        socket.onerror = function(error) {
            console.error("Erro de WebSocket:", error); // Log de erro no console
        };

        socket.onmessage = function(event) {
            const response = JSON.parse(event.data); // Recebe a resposta do servidor
            const loginMessage = document.getElementById('loginMessage'); // Pega a div para exibir a mensagem

            console.log(response); // Verifique a resposta recebida

            if (response.status === 'success') {
                loginMessage.innerHTML = response.message; // Mensagem de sucesso
                loginMessage.style.color = 'green'; // Cor verde para sucesso
            } else {
                loginMessage.innerHTML = response.message; // Mensagem de erro
                loginMessage.style.color = 'red'; // Cor vermelha para erro
            }
        };
    });
});