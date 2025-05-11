.PHONY: run
run:
	poetry run python -m uvicorn app.main:app --reload --proxy-headers --forwarded-allow-ips=*
