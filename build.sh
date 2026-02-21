#!/usr/bin/env bash

# Для немедленного выхода в случае ошибки
set -o errexit

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Команды для установки проекта.
# (установка зависимостей, сборка статики, применение миграций и др.)
make install && make collectstatic && make migrate