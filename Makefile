# ARTPARK MCP Server — common commands
VENV := ~/pyenv/onehealth-artpark-mcp
PYTHON := $(VENV)/bin/python
PORT := 8000

.PHONY: help run test lint docker docker-up docker-down clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

run: ## Start the MCP server (http://localhost:8000/mcp)
	$(PYTHON) artpark_server.py

test: ## Run the test suite (40 tests)
	$(PYTHON) -m pytest tests/ -v --tb=short

test-quick: ## Run tests without verbose output
	$(PYTHON) -m pytest tests/ -q

lint: ## Check for linting issues
	$(PYTHON) -m py_compile artpark_server.py
	$(PYTHON) -m py_compile artpark/client.py
	@echo "No syntax errors found."

check: ## Verify all datasets load and tools register
	@$(PYTHON) -c "\
	from artpark.client import ARTPARKData; \
	c = ARTPARKData(); \
	cat = c.get_catalogue(); \
	print(f'Datasets: {len(cat)}'); \
	[print(f'  {did}: {len(info[\"tables\"])} tables, {len(info[\"csv_files\"])} CSVs') for did, info in sorted(cat.items())]; \
	import asyncio, artpark_server; \
	tools = asyncio.run(artpark_server.mcp.list_tools()); \
	print(f'Tools: {len(tools)}'); \
	[print(f'  {t.name}') for t in tools]; \
	print('All checks passed.');"

docker: ## Build Docker image
	docker build -t artpark-mcp .

docker-up: ## Start server + Jaeger with docker compose
	docker compose up -d
	@echo "Server:    http://localhost:$(PORT)/mcp"
	@echo "Health:    http://localhost:$(PORT)/health"
	@echo "Jaeger UI: http://localhost:16686"

docker-down: ## Stop docker compose services
	docker compose down

clean: ## Remove Python cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache
