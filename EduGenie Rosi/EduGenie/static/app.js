const task = document.getElementById("task");
const level = document.getElementById("level");
const levelLabel = document.getElementById("levelLabel");
const inputText = document.getElementById("inputText");
const numQuestions = document.getElementById("numQuestions");
const button = document.getElementById("submitBtn");
const status = document.getElementById("status");
const result = document.getElementById("result");

function updateForm() {
  const needsLevel = task.value === "explain" || task.value === "learn";
  levelLabel.style.display = needsLevel ? "block" : "none";
  level.style.display = needsLevel ? "block" : "none";
  numQuestions.parentElement.style.display = task.value === "quiz" ? "block" : "none";
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[ch]));
}

function render(data) {
  if (data.questions) {
    result.innerHTML = data.questions.map((q, i) => `
      <div class="quiz-item">
        <strong>${i + 1}. ${escapeHtml(q.question)}</strong>
        ${q.options.map(o => `<div class="quiz-option">${escapeHtml(o)}</div>`).join("")}
        <div><strong>Answer:</strong> ${escapeHtml(q.answer)}</div>
        <div><strong>Why:</strong> ${escapeHtml(q.explanation || "")}</div>
      </div>
    `).join("");
  } else if (data.result) {
    result.textContent = data.result;
  } else {
    result.innerHTML = `<span class="error">${escapeHtml(data.error || "No result returned.")}</span>`;
  }
}

task.addEventListener("change", updateForm);

button.addEventListener("click", async () => {
  const text = inputText.value.trim();
  if (!text) {
    status.textContent = "Please enter some text first.";
    return;
  }

  const endpoints = {
    qa: "/qa",
    explain: "/explain",
    quiz: "/quiz",
    summarize: "/summarize",
    learn: "/learn/recommendations"
  };

  let body;
  if (task.value === "qa") body = { question: text };
  if (task.value === "explain") body = { topic: text, level: level.value };
  if (task.value === "quiz") body = { text, num_questions: Number(numQuestions.value) };
  if (task.value === "summarize") body = { text };
  if (task.value === "learn") body = { topic: text, level: level.value };

  button.disabled = true;
  status.textContent = "Generating...";
  result.textContent = "";

  try {
    const response = await fetch(endpoints[task.value], {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(body)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed.");
    render(data);
    status.textContent = "Completed.";
  } catch (err) {
    status.textContent = "Request failed.";
    result.innerHTML = `<span class="error">${escapeHtml(err.message)}</span>`;
  } finally {
    button.disabled = false;
  }
});

updateForm();
