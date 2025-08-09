docs-start:
	@echo "Starting Documentation Server...\n"
	@cd docs \
		&& npm start

docs:
	@echo "Building Documentation Server...\n"
	@cd docs \
		&& npm install @docusaurus/eslint-plugin@latest --save-dev \
		&& npm install \
		&& npm dedupe \
		&& npm run build

central-start:
	@echo "Starting Central Server...\n"
	@echo "Installing dependencies...\n"
	@cd software/backend/central \
		&& uv sync
	@echo "\nMaking Migrations...\n"
	@cd software/backend/central \
		&& uv run lib/manage.py makemigrations \
		&& uv run lib/manage.py migrate
	@echo "\nRunning tests...\n"
	@echo "All tests passed!\n"
	@echo "Central Development Server is ready to run 🏃!\n"
	@echo "Starting Central Server...\n"
	@cd software/backend/central \
		&& uv run lib/manage.py runserver

central-app:
	@echo "Adding new app '$(app-name)' to Central Backend...\n"
ifndef app-name
	@echo "app-name is not set. Please set it before running this command.\n"
	@echo "Usage: make central-app app-name=your_app_name"
else
	@echo "Adding new app '$(app-name)' to Central Backend...\n"
	@echo "Installing dependencies...\n"
	@cd software/backend/central \
		&& uv sync
	@echo "\nAdding App...\n"
	@cd software/backend/central/lib \
		&& uv run django-admin startapp $(app-name) 
	@echo "\nApp '$(app-name)' added successfully to software/backend/central/lib!\n"
endif

central-install:
	@echo "Installing '$(app-name)' to Central Python Environment...\n"
ifndef app-name
	@echo "app-name is not set. Please set it before running this command.\n"
	@echo "Usage: make central-app app-name=your_app_name"
else
	@echo "Adding new app '$(app-name)' to Central Backend...\n"
	@echo "Installing dependencies...\n"
	@cd software/backend/central \
		&& uv sync
	@echo "\nAdding App...\n"
	@cd software/backend/central/lib \
		&& uv run django-admin startapp $(app-name) 
	@echo "\nApp '$(app-name)' added successfully to software/backend/central/lib!\n"
endif

superuser:
	@echo "Creating superuser for Central Backend...\n"
	@echo "Installing dependencies...\n"
	@cd software/backend/central \
		&& uv sync
	@cd software/backend/central \
		&& uv run lib/manage.py createsuperuser