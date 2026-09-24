.PHONY: up down start stop build shell sync test smoke lint fmt jupyter publish

up:
	docker compose up -d --build

down:
	docker compose down

start:
	docker compose start

stop:
	docker compose stop

build:
	docker compose build

shell:
	docker compose exec fetta bash

sync:
	docker compose exec fetta uv sync

test:
	docker compose exec fetta uv run pytest -v

smoke:
	docker compose exec fetta uv run python scripts/smoke.py

debug:
	docker compose exec fetta uv run python -m debugpy --listen 0.0.0.0:5678 --wait-for-client scripts/smoke.py

lint:
	docker compose exec fetta uv run ruff check src tests

fmt:
	docker compose exec fetta uv run ruff format src tests

jupyter:
	docker compose exec fetta uv run jupyter lab \
		--ip=0.0.0.0 \
		--port=8888 \
		--no-browser \
		--ServerApp.token='' \
		--ServerApp.password=''

publish:
	@if [ -z "$(BUMP)" ]; then \
		echo "Usage: make publish BUMP=patch|minor|major"; \
		exit 1; \
	fi
	uv version --bump $(BUMP)
	$(eval VERSION := $(shell uv version --short))
	git add pyproject.toml uv.lock
	git commit -m "chore: release $(VERSION)"
	git tag v$(VERSION)
	git push && git push --tags
	@echo "Released $(VERSION)"

#deploy-env:
#	uv init --python 3.12 --package --name fetta
#	uv venv && source .venv/bin/activate && uv pip install -e .
#	source .venv/bin/activate && uv add "playwright==1.63.0" "beautifulsoup4>=4.12"
#	source .venv/bin/activate && uv add --dev "pytest>=8" "pytest-asyncio>=0.24" "ruff>=0.6" debugpy jupyterlab ipykernel requests-mock
