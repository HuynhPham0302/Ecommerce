.DEFAULT_GOAL := run

run:
	python3 application.py

seed:
	python3 seed_db.py

.PHONY: run seed