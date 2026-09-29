from unittest.mock import patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_validation_rejects_empty_question(client):
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422


def test_qa(client):
    with patch(
        "qna.generate_text",
        return_value="The answer is that photosynthesis converts light energy into chemical energy.",
    ):
        response = client.post(
            "/qa",
            json={"question": "What is photosynthesis?"},
        )
    assert response.status_code == 200
    assert "photosynthesis" in response.json()["answer"]


def test_explain(client):
    with patch(
        "explanation_module.generate_text",
        return_value="A triangle with a right angle follows a² + b² = c².",
    ):
        response = client.post(
            "/explain",
            json={"topic": "Pythagoras theorem", "level": "beginner"},
        )
    assert response.status_code == 200
    assert "triangle" in response.json()["explanation"]


def test_quiz(client):
    raw = """{
      "questions": [
        {"question":"Q1","options":["A","B","C","D"],"correct_answer":"A","explanation":"Because A."},
        {"question":"Q2","options":["A","B","C","D"],"correct_answer":"B","explanation":"Because B."},
        {"question":"Q3","options":["A","B","C","D"],"correct_answer":"C","explanation":"Because C."}
      ]
    }"""
    with patch("quiz_module.generate_text", return_value=raw):
        response = client.post("/quiz", json={"text": "A short educational passage."})
    assert response.status_code == 200
    assert len(response.json()["questions"]) == 3
    assert all(len(q["options"]) == 4 for q in response.json()["questions"])


def test_summary(client):
    with patch("summary_module.generate_text", return_value="A concise summary."):
        response = client.post(
            "/summarize",
            json={"text": "This is an educational passage about a topic."},
        )
    assert response.status_code == 200
    assert response.json()["summary"] == "A concise summary."


def test_learning_path(client):
    raw = """{
      "title":"SQL Path",
      "goal":"Become job-ready",
      "overview":"Learn SQL from foundations to practical querying.",
      "steps":[
        {"stage":"Beginner","topics":["SELECT"],"suggested_duration":"1 week","activities":["Practice queries"],"resources":["Official docs"]},
        {"stage":"Intermediate","topics":["JOIN"],"suggested_duration":"1 week","activities":["Build exercises"],"resources":["Tutorials"]},
        {"stage":"Advanced","topics":["Optimization"],"suggested_duration":"2 weeks","activities":["Analyze queries"],"resources":["Books"]}
      ],
      "study_tips":["Practice every day."]
    }"""
    with patch("learning_path.generate_text", return_value=raw):
        response = client.post(
            "/learn/recommendations",
            json={"topic": "SQL", "level": "beginner", "goal": "Become job-ready"},
        )
    assert response.status_code == 200
    assert len(response.json()["steps"]) >= 3
