RED="'\033[0;31m'"
NC="'\033[0m'"

docs-start:
	@echo "Starting Documentation Server...\n"
	@cd docs \
		&& npm start

docs-build:
	@echo "Building Documentation Server...\n"
	@cd docs \
		&& npm install @docusaurus/eslint-plugin@latest --save-dev \
		&& npm install \
		&& npm dedupe \
		&& npm run build

server:
ifdef run
	@echo "Running command in Server Environment..."
	@cd src/server \
		&& $(run)
else
	@reset
	@echo "${RED}Killing any Orphan${NC} Processes..."
	@./bin/kill_honcho.sh
	@echo "\nInstalling dependencies...\n"
	@cd src/server \
		&& uv sync
	@echo "\nBuild Static Files...\n"
	@cd src/server/vite \
		&& npm run build
	@echo "\nMaking Migrations...\n"
	@cd src/server \
		&& uv run lib/main.py makemigrations \
		&& uv run lib/main.py migrate
	@echo "\nRunning tests...\n"
	@echo "All tests passed!\n"
	@echo "Central Development Server is ready to run 🏃!\n"
	@echo "Starting Server...\n"
	@cd src/server \
		&& uv run lib/main.py vite runserver
endif

server-clean:
	@echo "${RED}Cleaning Server${NC}..."
	@echo "Deleting __pycache__ directories"
	@cd src/server/lib \
		&& find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Deleting old migration files"
	@cd src/server/lib \
		&& find . -type f -path "*/migrations/*.py" ! -name "__init__.py" -exec rm -f {} +
	@echo "Deleting default SQLite databases"
	@cd src/server \
		&& find . -type f -name "db.sqlite3" -exec rm -f {} +

superuser:
	@echo "Creating superuser for Central Backend...\n"
	@echo "Installing dependencies...\n"
	@cd src/server \
		&& uv sync
	@cd src/server \
		&& uv run lib/main.py createsuperuser