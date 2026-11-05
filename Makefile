PY ?= python3

.PHONY: help check test import import-check validate links board board-check qc-all

help:
	@echo "make check        tests + import check + validate + links (what CI runs)"
	@echo "make test         unit and integration tests"
	@echo "make import       re-normalize data/source snapshots (offline)"
	@echo "make validate     repository integrity"
	@echo "make board        regenerate reports/content-board.md"
	@echo "make qc-all       automated QC summary for every content item"

check: test import-check validate links board-check

test:
	$(PY) -m unittest discover -s tests

import:
	$(PY) scripts/import_sheet.py

import-check:
	$(PY) scripts/import_sheet.py --check

validate:
	$(PY) scripts/validate_content.py

links:
	$(PY) scripts/check_links.py

board:
	$(PY) scripts/generate_board.py

board-check:
	$(PY) scripts/generate_board.py --check

qc-all:
	$(PY) scripts/qc_content.py run --all
