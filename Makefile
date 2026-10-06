.PHONY: install backend frontend test lint docs

install:
	python -m pip install -r backend/requirements.txt

backend:
	cd backend && PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm install && npm run dev -- --host 0.0.0.0 --port 3000

test:
	cd backend && PYTHONPATH=. pytest ../backend/tests -q

lint:
	cd backend && ruff check app tests
	cd frontend && npm run build

help:
	@echo "Available targets: install, backend, frontend, test, lint"
