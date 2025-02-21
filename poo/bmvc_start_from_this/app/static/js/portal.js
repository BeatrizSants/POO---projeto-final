
function showSignup() {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('signupSection').style.display = 'block';
}

function showLogin() {
    document.getElementById('signupSection').style.display = 'none';
    document.getElementById('loginSection').style.display = 'block';
}


document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            fetch('/portal', {
                method: 'POST',
                body: new URLSearchParams({
                    'username': username,
                    'password': password
                })
            })
            .then(response => {
                if (response.redirected) {
                    // A autenticação foi bem-sucedida, agora conecta ao WebSocket
                    const ws = new WebSocket("ws://localhost:8080/ws_login");

                    ws.onopen = function() {
                        console.log("Conexão WebSocket estabelecida");
                        // Envia a mensagem de login bem-sucedido após a autenticação
                        ws.send("login_success");
                    };

                    ws.onmessage = function(event) {
                        const data = JSON.parse(event.data);
                        console.log("Mensagem do servidor: ", data);

                        // Exibe um alerta se o login for bem-sucedido
                        if (data.status === 'success') {
                            alert(data.message);  // Exibe o alerta de login bem-sucedido
                            // Redireciona para a página de lobby após o alerta
                            window.location.href = response.url;
                        } else if (data.status === 'error') {
                            alert(data.message);  // Exibe o alerta de erro de login
                        }
                    };

                    ws.onclose = function() {
                        console.log("Conexão WebSocket fechada");
                    };
                } else {
                    alert("Login inválido!");  // Exibe alerta se a autenticação falhar
                }
            });
        });
    }

    
        // Lógica para o cadastro
        if (signupForm) {
            signupForm.addEventListener('submit', function(e) {
                e.preventDefault();
    
                const usernameInput = document.getElementById('signupUsername');
                const passwordInput = document.getElementById('signupPassword');
                
                if (usernameInput && passwordInput) {
                    const username = usernameInput.value;
                    const password = passwordInput.value;
    
                    fetch('/signup', {
                        method: 'POST',
                        body: new URLSearchParams({
                            'username': username,
                            'password': password
                        })
                    })
                    .then(response => {
                        if (response.redirected) {
                            // Cadastro bem-sucedido, agora conecta ao WebSocket
                            const ws = new WebSocket("ws://localhost:8080/ws_signup");
    
                            ws.onopen = function() {
                                console.log("Conexão WebSocket estabelecida");
    
                                // Envia a mensagem de signup bem-sucedido
                                ws.send("signup_success");
                            };
    
                            ws.onmessage = function(event) {
                                const data = JSON.parse(event.data);
                                console.log("Mensagem do servidor: ", data);
    
                                // Exibe um alerta conforme o status do cadastro
                                if (data.status === 'success') {
                                    alert("Cadastro bem-sucedido!");
                                    window.location.href = '/';  // Redireciona para a página inicial após sucesso
                                } else if (data.status === 'error') {
                                    alert("Cadastro inválido: " + data.message);  // Exibe erro
                                }
                            };
    
                            ws.onclose = function() {
                                console.log("Conexão WebSocket fechada");
                            };
                        } else {
                            alert("Erro ao cadastrar!");  // Exibe alerta se o cadastro falhar
                        }
                    })
                    .catch(error => {
                        console.error('Erro no cadastro:', error);
                    });
                } else {
                    console.error("Os campos de cadastro não foram encontrados.");
                }
            });
        }
    
        
});
