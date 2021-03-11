python=python
manage=./manage.py

runserver:
	@$(python) $(manage) runserver

intial-setup:
	@$(python) $(manage) initial_setup


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