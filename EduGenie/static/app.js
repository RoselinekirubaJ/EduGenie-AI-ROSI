const form = document.getElementById("edugenie-form");
const task = document.getElementById("task");
const input = document.getElementById("user-input");
const inputLabel = document.getElementById("input-label");
const levelGroup = document.getElementById("level-group");
const goalGroup = document.getElementById("goal-group");
const level = document.getElementById("level");
const goal = document.getElementById("goal");
const button = document.getElementById("submit-button");
const statusBox = document.getElementById("status");
const result = document.getElementById("result");

const taskConfig = {
  qa: { label: "Question", placeholder: "e.g. Why is the sky blue?" },
  explain: { label: "Topic", placeholder: "e.g. Pythagoras theorem" },
  quiz: { label: "Passage or topic text", placeholder: "Paste educational text to turn into 3 MCQs..." },
  summarize: { label: "Passage", placeholder: "Paste the passage you want summarized..." },
  learn: { label: "Topic", placeholder: "e.g. SQL, Python, Biology..." }
};

function updateForm() {
  const cfg = taskConfig[task.value];
  inputLabel.textContent = cfg.label;
  input.placeholder = cfg.placeholder;
  levelGroup.classList.toggle("hidden", !["explain", "learn"].includes(task.value));
  goalGroup.classList.toggle("hidden", task.value !== "learn");
}

task.addEventListener("change", updateForm);
updateForm();

function setStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.classList.remove("hidden", "error");
  if (isError) statusBox.classList.add("error");
}

function clearStatus() {
  statusBox.classList.add("hidden");
}

function renderResult(data) {
  result.classList.remove("hidden");

  if (task.value === "qa") {
    result.innerHTML = `<h2>Answer</h2><p>${escapeHtml(data.answer)}</p>`;
    return;
  }

  if (task.value === "explain") {
    result.innerHTML = `<h2>Explanation</h2><p>${escapeHtml(data.explanation)}</p><small>Engine: ${escapeHtml(data.engine)}</small>`;
    return;
  }

  if (task.value === "summarize") {
    result.innerHTML = `<h2>Summary</h2><p>${escapeHtml(data.summary)}</p>`;
    return;
  }

  if (task.value === "quiz") {
    result.innerHTML = `
      <h2>Quiz</h2>
      ${data.questions.map((q, i) => `
        <article class="quiz-item">
          <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
          ${q.options.map((option, j) => `<div class="quiz-option">${String.fromCharCode(65 + j)}. ${escapeHtml(option)}</div>`).join("")}
          <div class="answer">Correct answer: ${escapeHtml(q.correct_answer)}</div>
          <p>${escapeHtml(q.explanation)}</p>
        </article>
      `).join("")}
    `;
    return;
  }

  if (task.value === "learn") {
    result.innerHTML = `
      <h2>${escapeHtml(data.title)}</h2>
      <p><strong>Goal:</strong> ${escapeHtml(data.goal)}</p>
      <p>${escapeHtml(data.overview)}</p>
      ${data.steps.map((step, i) => `
        <article class="path-step">
          <h3>${i + 1}. ${escapeHtml(step.stage)}</h3>
          <p><strong>Duration:</strong> ${escapeHtml(step.suggested_duration)}</p>
          <p><strong>Topics:</strong> ${step.topics.map(escapeHtml).join(", ")}</p>
          <p><strong>Activities:</strong></p>
          <ul>${step.activities.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
          <p><strong>Resources:</strong></p>
          <ul>${step.resources.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
        </article>
      `).join("")}
      <h3>Study tips</h3>
      <ul>${data.study_tips.map(x => `<li>${escapeHtml(x)}</li>`).join("")}</ul>
    `;
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  button.disabled = true;
  result.classList.add("hidden");
  setStatus("EduGenie is thinking...");

  const payload = {};
  let endpoint = "";

  if (task.value === "qa") {
    endpoint = "/qa";
    payload.question = text;
  } else if (task.value === "explain") {
    endpoint = "/explain";
    payload.topic = text;
    payload.level = level.value;
  } else if (task.value === "quiz") {
    endpoint = "/quiz";
    payload.text = text;
  } else if (task.value === "summarize") {
    endpoint = "/summarize";
    payload.text = text;
  } else {
    endpoint = "/learn/recommendations";
    payload.topic = text;
    payload.level = level.value;
    payload.goal = goal.value.trim() || null;
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed.");
    }

    clearStatus();
    renderResult(data);
  } catch (error) {
    setStatus(error.message || "Something went wrong.", true);
  } finally {
    button.disabled = false;
  }
});
