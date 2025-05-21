make db:
	poetry run python3 fias/scripts/load_db.py

make dev:
	poetry run fastapi dev fias/app/app.py

make run:
	poetry run fastapi run --workers 4 fias/app/app.py
