# Менеджер задач

## Статусы

### Статусы workflow actions

[![Actions Status](https://github.com/experiment0/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/experiment0/python-project-52/actions)
[![Django CI](https://github.com/experiment0/python-project-52/actions/workflows/django-ci.yml/badge.svg)](https://github.com/experiment0/python-project-52/actions/workflows/django-ci.yml)

### Статусы [SonarQube](https://sonarcloud.io/)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=bugs)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=experiment0_python-project-52&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=experiment0_python-project-52)

## О проекте

Данный проект создан в процессе прохождения курса [Python-разработчик](https://ru.hexlet.io/programs/python).\
В нем реализовано web-приложение на Django для управления задачами.\
Оно позволяет создавать задачи, назначать исполнителей, добавлять статусы и метки. \
Для работы с приложением требуется регистрация и аутентификация.

## Демонстрация работы

Проект развернут на платформе [render.com](https://render.com/) и доступен по ссылке: \
https://task-manager-pq7o.onrender.com/

> **Примечание.** \
> Поскольку для деплоя сайта используется бесплатный тариф, \
> платформа `render.com` утилизует ресурсы, которые не используются какое-то время.\
> Поэтому при открытии сайта, возможно, загрузка сайта начнется с процесса его сборки \
> и нужно будет подождать ее окончания.

[Видео с демо работы сайта](https://disk.yandex.ru/i/j9xmhYSlfsV_bA)

## Инструкция по локальному запуску

1. Проверить, установлена ли утилита `uv`:

   ```sh
   uv --version
   ```

   Если не установлена, то нужно установить [по инструкции](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).

2. Проверить, установлена ли утилита `make`:

   ```sh
   make --version
   ```

   Если не установлена, то установить [на windows](https://stackoverflow.com/questions/32127524/how-can-i-install-and-use-make-in-windows) или [на ubuntu](https://andreyex.ru/ubuntu/kak-ustanovit-make-na-ubuntu/).

3. ```sh
   # Клонировать проект
   git clone https://github.com/experiment0/python-project-52.git

   # Перейти в папку с проектом
   cd python-project-52

   # Установить зависимости
   make install
   ```

4. Создать в корне проекта файл `.env` для переменных среды.

   ```sh
   touch .env
   ```

   И добавить в него переменные среды по аналогии с образцом из файла [.env-example](./.env-example) \
   В переменной `DATABASE_URL` указывается путь для соединения с БД.\
   Можно указать `sqlite:///db.sqlite3`.\
   Либо установить PostgreSQL [по инструкции](https://tproger.ru/articles/osnovy-postgresql-dlya-nachinayushhih--ot-ustanovki-do-pervyh-zaprosov-250851)
   и указать путь для БД PostgreSQL.

5. Далее нужно применить миграции к БД.

   ```sh
   make migrate
   ```

6. Для получения токена `ROLLBAR_ACCESS_TOKEN` можно зарегистрироваться на https://app.rollbar.com/ и добавить данный проект.\
Но можно этого не делать, проект все равно будет работать.

7. Запустить локальный сервер
   ```sh
   make start
   ```
   Перейти по ссылке http://127.0.0.1:8000
