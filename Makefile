PYTHON := uv run python
SRC_DIR := src
OUTPUT_DIR := output
DATA_DIR := data
CACHE_DIR := .local_cache

all: run

run:
	@echo "running callmemaybe program..."
	@export UV_CACHE_DIR=$(CACHE_DIR)/uv && export HF_HOME=$(CACHE_DIR)/hf && $(PYTHON) -Bm $(SRC_DIR) # <--- 2. UPDATE THIS LINE

clean:
	@echo "🧹 Cleaning up generated files and cache..."
	rm -rf $(OUTPUT_DIR)
	rm -rf $(CACHE_DIR) # <--- 3. ADD THIS LINE TO DELETE CACHE
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Clean complete."

lint:
	@echo "checking flake"
	flake8 $(SRC_DIR)
	@echo "checking mypy"
	mypy $(SRC_DIR) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --follow-imports=skip
	echo "✅ checking done"

lint-strict:
	@echo "checking flake"
	flake8 $(SRC_DIR)
	@echo "checking mypy"
	mypy $(SRC_DIR) --strict --follow-imports=skip
	echo "✅ checking done"

install:
	@echo "installing required dependecies through uv..."
	@export UV_CACHE_DIR=$(CACHE_DIR)/uv && export HF_HOME=$(CACHE_DIR)/hf && uv sync # <--- 4. UPDATE THIS LINE
	@echo "syncing done succesfully, you can run make install"

debug:
	echo "running python debugger"
	pdb3 $(SRC_DIR)/__main__.py


.PHONY: all run clean format lint help