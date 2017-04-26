PYTHON3=python3
VENV_DIR=venv3
NAME=Extract Keywords URLs
ECHO=@echo

.PHONY: help

help:
	$(ECHO) "$(NAME)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m=> %s\n", $$1, $$2}'


$(VENV_DIR):
	$(PYTHON3) -m venv $(VENV_DIR)

install: $(VENV_DIR) ## install dependencies
	$(VENV_DIR)/bin/pip install -Ur requirements.txt

run: install	
	$(VENV_DIR)/bin/python extract_keywords_url.py -i urls.csv
