start: 
	python manage.py start

format:
	black .

t: 
	TEST_MODE=1 pytest --cov

