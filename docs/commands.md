python ai_system/scripts/fine_tune.py

python3 -m ai_system.app.training.trainer

curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"query": "What is a variable?"}' > response.md
