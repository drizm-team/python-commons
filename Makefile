.PHONY: preview
preview:
	@poetry run mkdocs serve

.PHONY: format
format:
	@poetry run black ./drizm_commons
