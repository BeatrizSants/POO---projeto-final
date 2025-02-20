
document.addEventListener('DOMContentLoaded', () => {

    const moles = document.querySelectorAll('.mole');
    const traps = document.querySelectorAll('.trap');
    let gameInterval;
    let gameTimeout;

    // Atualiza a pontuação na interface
    function updateScoreDisplay(score) {
        document.getElementById('score').textContent = score;  // Atualiza a pontuação no HTML
    }

    // Obtém a pontuação do servidor e atualiza a tela
    function loadScore() {
        fetch('/get_score', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            updateScoreDisplay(data.score || 0);  // Chama a função para atualizar a pontuação
        })
        .catch(error => console.error('Erro ao carregar pontuação:', error));
    }

    function randomHoles() {
        moles.forEach(mole => mole.style.display = 'none');
        traps.forEach(trap => trap.style.display = 'none');
    
        const occupiedHoles = new Set();  // Mantém o controle dos buracos ocupados
    
        const numMoles = Math.floor(Math.random() * 3) + 1;
        for (let i = 0; i < numMoles; i++) {
            let moleIndex;
            do {
                moleIndex = Math.floor(Math.random() * moles.length);
            } while (occupiedHoles.has(moleIndex));  // Garante que o buraco não esteja ocupado
    
            moles[moleIndex].style.display = 'block';
            occupiedHoles.add(moleIndex);  // Marca o buraco como ocupado
        }
    
        if (Math.random() < 0.5) {
            let trapIndex;
            do {
                trapIndex = Math.floor(Math.random() * traps.length);
            } while (occupiedHoles.has(trapIndex));  // Garante que o buraco não esteja ocupado
    
            traps[trapIndex].style.display = 'block';
        }
    }
    
    function handleMoleClick(mole) {
        fetch('/add_score', { method: 'POST' }).then(loadScore);  // Envia o incremento de pontos ao backend
        mole.style.display = 'none';
    }

    function handleTrapClick(trap) {
        fetch('/take_score', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.accumulated_score !== undefined) {
                    console.log(`Pontos subtraídos: ${data.accumulated_score}`);
                } else {
                    console.error("Erro: Pontuação acumulada não encontrada na resposta");
                }
                loadScore();  // Atualiza a pontuação na tela
            })
            .catch(error => console.error('Erro ao subtrair pontos:', error));
    
        trap.style.display = 'none';  // Esconde a armadilha
    }

    moles.forEach(mole => mole.addEventListener('click', () => handleMoleClick(mole)));
    traps.forEach(trap => trap.addEventListener('click', () => handleTrapClick(trap)));

    function startGame() {
        document.querySelector('.conteiner').style.display = 'none';
        document.querySelector('.game').style.display = 'block';
    
        clearInterval(gameInterval);
        clearTimeout(gameTimeout);
        
        fetch('/start_game', { method: 'POST' }).then(loadScore);
    
        const gameTime = parseInt(document.getElementById('game-time').value);
        let timeLeft = gameTime;
    
        const timerElement = document.getElementById('timer');
        if (!timerElement) {
            console.error("Elemento 'timer' não encontrado!");
            return;
        }
    
        timerElement.textContent = timeLeft + 's';
    
        if (window.timerInterval) {
            clearInterval(window.timerInterval);  // Garante que não há múltiplos intervalos rodando
        }
    
        window.timerInterval = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
                timerElement.textContent = timeLeft + 's';
            } else {
                clearInterval(window.timerInterval);
            }
        }, 1000);
    
        gameInterval = setInterval(randomHoles, 500);
        gameTimeout = setTimeout(() => {
            fetch('/end_game', { method: 'POST' }) // Obtém a pontuação final do backend
                .then(response => response.json())
                .then(data => {
                    if (data.score !== undefined) {
                        document.getElementById('final-score').textContent = data.score;
                    } else {
                        console.error("Erro: Resposta do servidor não contém 'score'");
                    }
                })
                .catch(error => console.error('Erro ao obter pontuação final:', error));
        
            document.querySelector('.end-game').style.display = 'block';
            document.querySelector('.game').style.display = 'none';
        
            clearInterval(gameInterval);
            clearInterval(window.timerInterval);
        }, gameTime * 1000);
        
    }
    
    function restartGame() {
        document.querySelector('.end-game').style.display = 'none';
        document.querySelector('.conteiner').style.display = 'flex';
    }

    window.startGame = startGame;
    window.restartGame = restartGame; 
    loadScore();  // Carregar pontuação ao iniciar
});
