# AI Interview Coach — application only

An AI interview practice web app. Choose a role and topic, generate a question, answer it, and get feedback from Amazon Bedrock.

## Run on Windows PowerShell

Install Python 3.12 and AWS CLI, then open this folder in a terminal:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:AWS_REGION="ap-south-1"
$env:BEDROCK_MODEL_ID="YOUR_AVAILABLE_MODEL_OR_INFERENCE_PROFILE_ID"
uvicorn app.main:app --reload --port 8080
```

Open http://localhost:8080 in your browser. To use AI features, sign in with AWS CLI credentials that can invoke your chosen Bedrock model in that region. You can test the health endpoint at http://localhost:8080/api/health without AWS access. Bedrock requests may incur charges.

## Run tests (optional)

```powershell
pip install -r requirements-dev.txt
pytest -q
```

Project files: `app/main.py` (API), `app/static/index.html` (web page), `tests/test_app.py` (tests).
