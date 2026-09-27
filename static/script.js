const questionInput = document.getElementById("question");
const askButton = document.getElementById("askButton");

const loading = document.getElementById("loading");
const error = document.getElementById("error");

const answerSection = document.getElementById("answerSection");
const answerElement = document.getElementById("answer");

const sourcesSection = document.getElementById("sourcesSection");
const sourcesElement = document.getElementById("sources");

// ============================================================
// ASK QUESTION
// ============================================================

async function askQuestion() {

const question = questionInput.value.trim();

if (!question) {
    showError("Please enter a question.");
    return;
}

hideError();

answerSection.classList.add("hidden");
sourcesSection.classList.add("hidden");

loading.classList.remove("hidden");

askButton.disabled = true;
askButton.textContent = "Processing...";

try {

    const response = await fetch("/ask", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.error || "Something went wrong."
        );
    }

    displayAnswer(data.answer);
    displaySources(data.sources);

} catch (err) {

    console.error(err);
    showError(err.message);

} finally {

    loading.classList.add("hidden");

    askButton.disabled = false;
    askButton.textContent = "Ask Question";
}

}

// ============================================================
// DISPLAY ANSWER
// ============================================================

function displayAnswer(answer) {


answerElement.textContent = answer;

answerSection.classList.remove("hidden");

}

// ============================================================
// DISPLAY SOURCES
// ============================================================

function displaySources(sources) {

sourcesElement.innerHTML = "";

if (!sources || sources.length === 0) {

    sourcesElement.innerHTML = "<p>No sources available.</p>";

    sourcesSection.classList.remove("hidden");

    return;
}

sources.forEach(function (source, index) {

    const card = document.createElement("div");

    card.className = "source-card";

    card.innerHTML =
        '<div class="source-title">' +
        "Source " + (index + 1) +
        ": Section " + source.section +
        "</div>" +

        '<div class="source-info">' +

        "<strong>Title:</strong> " +
        source.title +
        "<br>" +

        "<strong>Page:</strong> " +
        source.page +
        "<br>" +

        "<strong>Document:</strong> " +
        source.source +
        "<br>" +

        "<strong>Relevance Score:</strong> " +
        Number(source.score).toFixed(3) +

        "</div>";

    sourcesElement.appendChild(card);
});

sourcesSection.classList.remove("hidden");


}

// ============================================================
// ERROR HANDLING
// ============================================================

function showError(message) {


error.textContent = message;

error.classList.remove("hidden");


}

function hideError() {

error.classList.add("hidden");

error.textContent = "";

}

// ============================================================
// BUTTON EVENT
// ============================================================

askButton.addEventListener("click", askQuestion);

// ============================================================
// CTRL + ENTER TO SUBMIT
// ============================================================

questionInput.addEventListener("keydown", function (event) {

if (event.ctrlKey && event.key === "Enter") {
    askQuestion();
}


});
