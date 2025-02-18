let questions = [];
let currentQuestionIndex = 0;

document.addEventListener("DOMContentLoaded", async function() {
    await fetchQuestions();
    showQuestion();
});

async function fetchQuestions() {
    const response = await fetch("/get_questions");
    questions = await response.json();
}

function showQuestion() {
    if (currentQuestionIndex >= questions.length) {
        document.getElementById("quiz-container").innerHTML = "<h2>Quiz finalizado!</h2>";
        return;
    }

    const questionData = questions[currentQuestionIndex];
    document.getElementById("question-text").innerText = questionData.pergunta;
    
    const optionsContainer = document.getElementById("options");
    optionsContainer.innerHTML = "";

    questionData.opcoes.forEach(option => {
        const button = document.createElement("button");
        button.innerText = option;
        button.onclick = () => checkAnswer(option, questionData.resposta);
        optionsContainer.appendChild(button);
    });

    document.getElementById("next-btn").disabled = true;
}

function checkAnswer(selected, correct) {
    if (selected === correct) {
        alert("Resposta correta!");
    } else {
        alert("Resposta errada!");
    }
    document.getElementById("next-btn").disabled = false;
}

document.getElementById("next-btn").addEventListener("click", () => {
    currentQuestionIndex++;
    showQuestion();
});