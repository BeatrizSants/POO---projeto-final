document.addEventListener('DOMContentLoaded', () => {
    const moles = document.querySelectorAll('.mole');
    const traps = document.querySelectorAll('.trap');
    let score = 0;
    let gameInterval;
    let gameTimeout;

    // Função para randomizar os buracos (moles e traps)
    function randomHoles() {
        moles.forEach(mole => mole.style.display = 'none');
        traps.forEach(trap => trap.style.display = 'none');

        const numMoles = Math.floor(Math.random() * 3) + 1;

        for (let i = 0; i < numMoles; i++) {
            const moleIndex = Math.floor(Math.random() * moles.length);
            if (moles[moleIndex]) { 
                moles[moleIndex].style.display = 'block';
            }
        }

        if (Math.random() < 0.5) {
            const trapIndex = Math.floor(Math.random() * traps.length);
            if (traps[trapIndex]) { 
                traps[trapIndex].style.display = 'block';
            }
        }
    }

    // Função para lidar com a interação dos moles (aumentar a pontuação)
    function handleMoleClick(mole) {
        score++;
        updateScoreDisplay();
        mole.style.display = 'none';
    }

    // Função para lidar com a interação das traps (diminuir a pontuação)
    function handleTrapClick(trap) {
        score = Math.max(0, score - 1);
        updateScoreDisplay();
        trap.style.display = 'none';
    }

    // Função para atualizar a pontuação na interface
    function updateScoreDisplay() {
        document.getElementById('score').textContent = score;
    }

    moles.forEach(mole => {
        mole.addEventListener('click', () => handleMoleClick(mole));
    });

    // Adicionando os event listeners para as traps
    traps.forEach(trap => {
        trap.addEventListener('click', () => handleTrapClick(trap));
    });

    // Função para iniciar o jogo
    function startGame() {
        clearInterval(gameInterval);
        clearTimeout(gameTimeout);

        const gameTime = parseInt(document.getElementById('game-time').value) * 1000;

        gameInterval = setInterval(randomHoles, 1000);
        gameTimeout = setTimeout(() => {
            clearInterval(gameInterval);
            alert('Fim do jogo! Pontuação final: ' + score);
            sendScoreToServer();
        }, gameTime);
    }
// Expondo a função `startGame` para ser chamada no HTML
    window.startGame = startGame;
    // Função para enviar a pontuação para o servidor
    function sendScoreToServer() {
        fetch('/update_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                score: score // Removido o username
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Erro ao atualizar pontuação:', error);
        });
    }

    // Função para carregar a pontuação salva ao carregar a página
    function loadScore() {
        fetch('/get_score', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            score = data.score || 0; 
            updateScoreDisplay();
        })
        .catch(error => {
            console.error('Erro ao carregar pontuação:', error);
        });
    }

    // Adicionando os event listeners para os moles
    

    // Carregar a pontuação salva ao carregar a página
    loadScore();
});
