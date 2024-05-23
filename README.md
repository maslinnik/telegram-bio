# telegram-bio

![coverage badge](coverage.svg)

Второй проект курса по Python, ФПМИ МФТИ, 1 курс

Роман Первутинский, Б05-328

## Описание 

Приложение, отслеживающее обновления статуса пользователя Telegram.

### Пользовательский интерфейс

- Добавление пользователей в список отслеживаемых через панель администратора/пользователя

- Регулярное (раз в несколько минут) обновление статуса выбранных пользователей

- Публикация истории статусов на веб-сайт

### Развёртывание

- Приложение в контейнере: все процессы работают изолированно

## Запуск

Для работы требуется [Docker Compose](https://docs.docker.com/compose/).

Чтобы запустить приложение:

```shell
docker compose up
```

В файле `.env` можно задать логин и пароль от панели администратора, а также внешний порт.

### Запуск тестов

```shell
python -m unittest discover -s tests
```

Покрытие:

```shell
coverage run -m unittest discover -s tests
coverage report -m
```

## Внутреннее устройство

### Используемые технологии

- Flask &mdash; веб-фреймворк

- SQLAlchemy &mdash; библиотека для работы с БД

- telethon &mdash; библиотека для работы с API Telegram

### Принцип работы приложения

- Скрипт, обновляющий базу данных, запущен в отдельном контейнере
- Скрипт регулярно отправляет запрос к странице t.me/username на получение нужной информации
- После препроцессинга данных обновления загружаются в базу данных
- При загрузке веб-страницы необходимые данные подгружаются из БД
- При авторизации происходит запрос к БД на совпадение зашифрованных паролей
- Веб-интерфейс позволяет отправить запрос на добавление пользователя в список отслеживаемых

### Telegram API

Telegram Bot API не позволяет получать информацию о пользователе по юзернейму.
API Telegram, работающее с протоколом MTProto, даёт такую возможность, но поскольку
оно предоставлено для создания клиентов, регулярное получение данных через него может привести к бану.

Вместо этого в приложении используется скрейпинг страниц вида t.me/username.
Альтернативный вариант, работающий через MTProto, представлен в `app/api_managers.py` как `MTProtoAPIManager`.
