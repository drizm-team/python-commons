.PHONY: preview
preview:
	@poetry run mkdocs serve

.PHONY: format
format:
	@poetry run black ./drizm_commons

.PHONY: requirements
requirements:
	@poetry export --dev --without-hashes -f requirements.txt > requirements.txt
