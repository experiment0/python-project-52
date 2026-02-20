RUFF_CHECK := uv run ruff check
MANAGE := uv run python manage.py

# Загружает зависимости проекта
install:
	uv sync

# Проверяет код в папке task_manager на соответствие правилам линтера из ruff.toml
lint:
	@$(RUFF_CHECK) task_manager

# Исправляет замечания линтера, не связанные с логикой (порядок импортов, пробелы, и т.д.)
fix:
	@$(RUFF_CHECK) --fix task_manager

# Создает файл с миграциями
migrations:
	@$(MANAGE) makemigrations

# Применяет миграции к БД
migrate:
	@$(MANAGE) migrate

# Запускает скрипт для установки uv и зависимостей проекта для платформы render.com
build:
	./build.sh

# Запускает локальный сервер
start:
	@$(MANAGE) runserver 0.0.0.0:8000

# Запускает сервер на render.com
render-start:
	gunicorn task_manager.wsgi

# Команды, которые могут совпадать с именами директорий и не должны быть с ними перепутаны
.PHONY: install lint fix migrations migrate build start render-start