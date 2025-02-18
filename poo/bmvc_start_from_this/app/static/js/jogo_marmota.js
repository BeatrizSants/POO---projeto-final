document.addEventListener('DOMContentLoaded', () => {
    const moles = document.querySelectorAll('.mole');
    const traps = document.querySelectorAll('.trap');
    let gameInterval;
    let gameTimeout;

    // Atualiza a pontuação na interface
    function updateScoreDisplay(score) {
        document.getElementById('score').textContent = score;
    }

    // Obtém a pontuação do servidor e atualiza a tela
    function loadScore() {
        fetch('/get_score', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            updateScoreDisplay(data.score || 0);
        })
        .catch(error => console.error('Erro ao carregar pontuação:', error));
    }

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

    function handleMoleClick(mole) {
        fetch('/add_score', { method: 'POST' }).then(loadScore);
        mole.style.display = 'none';
        
    }

    function handleTrapClick(trap) {
        fetch('/take_score', { method: 'POST' }).then(loadScore);
        trap.style.display = 'none';
        
    }

    moles.forEach(mole => mole.addEventListener('click', () => handleMoleClick(mole)));
    traps.forEach(trap => trap.addEventListener('click', () => handleTrapClick(trap)));

    function startGame() {
        clearInterval(gameInterval);
        clearTimeout(gameTimeout);

        fetch('/start_game', { method: 'POST' }).then(loadScore);

        const gameTime = parseInt(document.getElementById('game-time').value) * 1000;
        gameInterval = setInterval(randomHoles, 1000);
        gameTimeout = setTimeout(() => {
            clearInterval(gameInterval);
            fetch('/end_game', { method: 'POST' })
                .then(response => response.json())
                .then(data => alert('Fim do jogo! Pontuação final: ' + data.score))
                .catch(error => console.error('Erro ao finalizar jogo:', error));
        }, gameTime);
    }

    window.startGame = startGame;
    loadScore(); // Carregar pontuação ao iniciar
});
