#!/usr/bin/env bash

# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Команды для установки проекта.
# (установка зависимостей, сборка статики, применение миграций и др.)
# && make collectstatic
make install && make migrate