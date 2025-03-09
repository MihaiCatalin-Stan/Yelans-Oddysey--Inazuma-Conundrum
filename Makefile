# Makefile for Python project

# Set the Python interpreter
PYTHON = python3

# List of Python files
PY_FILES = main.py ning.py npc.py npc_in_combat.py player.py player_in_combat.py scene.py

# Default target
all: run

# Run the main.py script
run:
	$(PYTHON) -m main > output.log 2>&1

# Clean up generated files
clean:
	rm -rf __pycache__ *.pyc output.log

# Phony targets
.PHONY: all run clean
