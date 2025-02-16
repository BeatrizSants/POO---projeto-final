document.addEventListener("DOMContentLoaded", () => {
    let pontuacao = 0;

    function carregarPergunta() {
        fetch("/get_pergunta")
            .then(response => response.json())
            .then(data => {
                document.getElementById("pergunta").textContent = data.pergunta;
                const opcoesDiv = document.getElementById("opcoes");
                opcoesDiv.innerHTML = "";  // Limpa as opções anteriores

                data.opcoes.forEach(opcao => {
                    const button = document.createElement("button");
                    button.textContent = opcao;
                    button.onclick = () => verificarResposta(opcao, data.resposta);
                    opcoesDiv.appendChild(button);
                });
            });
    }

    function verificarResposta(escolha, respostaCorreta) {
        if (escolha === respostaCorreta) {
            pontuacao += 10;
            alert("Correto!");
        } else {
            alert("Errado! A resposta correta era: " + respostaCorreta);
        }
        document.getElementById("pontuacao").textContent = pontuacao;
        carregarPergunta();
    }

    carregarPergunta();
});