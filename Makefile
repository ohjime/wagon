RED="'\033[0;31m'"
NC="'\033[0m'"

env:
ifdef for
ifeq ($(for),macos)
	@echo "Installing Development Dependencies for MacOS"
	@echo "\nInstalling Homebrew...\n"
	@/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || true
	@brew update || true
	@echo "\nAdding Homebrew to PATH...\n"
	@export PATH="/usr/local/bin:$PATH"
	@echo "\nInstalling npm...\n"
	@brew install npm || true
	@echo "\nInstalling uv...\n"
	@brew install uv || true
	@echo "\nInstalling PostgreSQL...\n"
	@brew install postgresql || true
	@echo "\nStarting PostgreSQL service...\n"
	@brew services start postgresql || true
	@echo "\nInstalling PostGIS...\n"
	@brew install postgis || true
	@echo "\nInstalling GDAL, PROJ, and GEOS...\n"
	@brew install gdal proj geos || true
	@echo "\nMacOS Development Environment Setup Complete\n"
else
	@echo "\n'${for}' is not a recognized platform\n"
	@echo "Supported platforms are:\n1. macos\n2. linux\n3. windows"
endif
else
	@echo "\n No platform specified. Supported platforms are:"
	@echo "\n\t1. macos\n\t2. linux\n\t3. windows"
	@echo "\n Please re-run your command with an appropriate platform flag. For example:\n"
	@echo ">>> make dependencies for=macos\n"
endif

doc:
	@echo "Starting Documentation Server...\n"
	@cd docs \
		&& npm start

server:
ifdef run
	@echo "Running command in Server Environment..."
	@cd src/server \
		&& $(run)
else
	@reset
	@echo "${RED}Killing Orphaned Django Processes...${NC}"
	@./bin/kill_honcho.sh
	@echo "\nInstalling dependencies...\n"
	@cd src/server \
		&& uv sync
	@echo "\nBuilding Vite Assets..."
	@cd src/server/vite \
		&& npm install \
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

superuser:
	@echo "Creating superuser for Central Backend...\n"
	@echo "Installing dependencies...\n"
	@cd src/server \
		&& uv sync
	@cd src/server \
		&& uv run lib/main.py createsuperuser

db:
	@echo "\nSetting up Database from src/server/.env ...\n"
	@dotenv -f src/server/.env run -- sh -c 'psql -h localhost -p 5432 -U $$USER -d postgres -c \
		"CREATE USER $$DB_USER WITH PASSWORD '\''$$DB_PASSWORD'\'';" || \
		echo "Skipping User Creation..." && \
		psql -h localhost -p 5432 -U $$USER -d postgres -c \
		"ALTER USER $$DB_USER WITH PASSWORD '\''$$DB_PASSWORD'\'';"'
	@dotenv -f src/server/.env run -- sh -c 'psql -h localhost -p 5432 -U $$USER -d postgres -c \
		"ALTER USER $$DB_USER WITH SUPERUSER;"'
	@dotenv -f src/server/.env run -- sh -c 'psql -h localhost -p 5432 -U $$USER -d postgres -c \
		"CREATE DATABASE $$DB_NAME OWNER $$DB_USER;" || \
		echo "Skipping Database Creation..." && \
		psql -h localhost -p 5432 -U $$USER -d postgres -c \
		"ALTER USER $$DB_USER WITH PASSWORD '\''$$DB_PASSWORD'\'';"'
	@dotenv -f src/server/.env run -- sh -c 'psql -h localhost -p 5432 -U $$USER -d postgres -c \
		"ALTER DATABASE $$DB_NAME OWNER TO $$DB_USER;"'
	@echo "\nDatabase setup complete.\n"

data:
	@echo "Generating mock server data...\n"
	@cd src/server \
		&& WAGON_SKIP_GOOGLE=1 printf "from core.fake import generate\ngenerate(40)\n" | uv run lib/main.py shell
	
clean:
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
	@echo "Wiping PostgreSQL  and dropping all tables..."
	@cd src/server \
		&& psql -h localhost -p 5432 -U $(USER) -d postgres -c "DROP DATABASE IF EXISTS wagon_db;" \
		&& psql -h localhost -p 5432 -U $(USER) -d postgres -c 'DROP OWNED BY admin CASCADE;' || true \
		&& psql -h localhost -p 5432 -U $(USER) -d postgres -c 'DROP USER IF EXISTS admin;' || true