# ===== DEFAULT ======
default: radon bandit ruff mypy

radon:
	@echo "Cyclo Analysis"
	@radon mi . -s

bandit:
	@echo "Code Analysis"
	@bandit -r . -ll

ruff:
	@echo "Format and Linting"
	@ruff check . --fix