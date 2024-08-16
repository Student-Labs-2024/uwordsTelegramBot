# UWORDS TELEGRAM BOT
Интеграция Uwords - телеграмм бот для прослушивания сообщений пользователя и их отправки в приложение Uwords для дальнейшего изучения

![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)


## Stack
Python 3.11, PostgreSQL, Docker

## Packages
aiohhtp, aiogram

## Запуск проекта
Чтобы сделать миграцию к БД, нужно прописать в контейнере docker следующую команду
```shell
alembic -c src/alembic.ini revision --autogenerate -m "комментарий для миграции"
```

Применить миграции
```shell
alembic -c src/alembic.ini upgrade head
```

Запуск проекта на локальной машине
```shell
docker-compose -f "docker-compose.dev.yml" up --build
```

Настройка локального окружения pre-commit:
```shell
pre-commit install
pre-commit run --all-files
pre-commit install --hook-type commit-msg
```

Перед коммитом проверять код линтером Black
```shell
python -m black ./src --check
```

В случае замечаний линтера выполнить команду
```shell
python -m black ./src
```

Пример .env можно увидеть в следующих файлах:
- env.dev.example
- env.dev.db.example

## Authors
Daniil Kolevatykh - CTO, python software developer

Azamat Aubakirov - python software developer

Dmitry Prasolov - python software developer
