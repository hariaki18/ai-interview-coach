from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get('/api/health').json() == {'status': 'ok'}


def test_question_calls_ai():
    with patch('app.main.ask_model', return_value='How do Playwright fixtures work?') as model:
        response = client.post('/api/question', json={'role': 'QA Engineer', 'topic': 'Playwright'})
    assert response.status_code == 200
    assert response.json()['question'] == 'How do Playwright fixtures work?'
    model.assert_called_once()


def test_feedback_rejects_empty_answer():
    response = client.post('/api/feedback', json={
        'role': 'QA Engineer', 'topic': 'Playwright', 'question': 'Explain fixtures.', 'answer': ''
    })
    assert response.status_code == 422
