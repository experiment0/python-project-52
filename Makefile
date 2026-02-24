RUFF_CHECK := uv run ruff check
MANAGE := uv run python manage.py

# Загружает зависимости проекта
.PHONY: install
install:
	uv sync

# Проверяет код в папке task_manager на соответствие правилам линтера из ruff.toml
.PHONY: lint
lint:
	@$(RUFF_CHECK) task_manager

# Исправляет замечания линтера, не связанные с логикой (порядок импортов, пробелы, и т.д.)
.PHONY: fix
fix:
	@$(RUFF_CHECK) --fix task_manager

# Создает дамп данных для тестов
.PHONY: dumpdata
dumpdata:
	@$(MANAGE) dumpdata

# Запускает тесты
.PHONY: test
test:
	@$(MANAGE) test

# Проверяет ошибки линтера и запускает тесты
.PHONY: check
check: lint test

# Создает файл task_manager/locale/ru/LC_MESSAGES/django.po для перевода сообщений
.PHONY: messages
messages:
	@$(MANAGE) makemessages -l ru

# Компилирует файл task_manager/locale/ru/LC_MESSAGES/django.mo для вывода сообщений
.PHONY: compilemessages
compilemessages:
	@$(MANAGE) compilemessages --ignore=.venv

# Преобразование статических файлов
.PHONY: collectstatic
collectstatic:
	@$(MANAGE) collectstatic --no-input

# Создает файл с миграциями
.PHONY: migrations
migrations:
	@$(MANAGE) makemigrations

# Применяет миграции к БД
.PHONY: migrate
migrate:
	@$(MANAGE) migrate

# Запускает скрипт для установки uv и зависимостей проекта для платформы render.com
.PHONY: build
build:
	./build.sh

# Запускает локальный сервер
.PHONY: start
start:
	@$(MANAGE) runserver 0.0.0.0:8000

# Запускает сервер на render.com
.PHONY: render-start
render-start:
	gunicorn task_manager.wsgi
