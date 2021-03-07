python=python
manage=./manage.py

intial-setup:
	@$(python) $(manage) initial_setup

runserver:
	@$(python) $(manage) initial_setup
	@$(python) $(manage) runserver

migrate:
	@$(python) $(manage) makemigrations
	@$(python) $(manage) migrate

admin:
	@$(python) $(manage) createsuperuser

shell:
	@$(python) $(manage) shell_plus

install-depedancies:
	@virtualenv venv
	# source venv/bin/activate
	@pip install -r requirements.txt
ls:
	@source