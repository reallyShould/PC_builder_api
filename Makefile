PYTHON = python3
VENV = .venv
NORM_SCRIPT = data/normalization.py

.PHONY: all normalize install clean

all: normalize

normalize:
	@if [ -d "$(VENV)" ]; then \
		./$(VENV)/bin/python $(NORM_SCRIPT); \
	else \
		$(PYTHON) "$(NORM_SCRIPT)"; \
	fi

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
