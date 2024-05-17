# telegram-bio

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

## Внутреннее устройство

### Используемые технологии

- Flask &mdash; веб-фреймворк

- PostgreSQL &mdash; БД

- SQLAlchemy &mdash; библиотека для работы с БД

- telethon &mdash; библиотека для работы с API Telegram

### Принцип работы приложения

- Скрипт, обновляющий базу данных, запущен как служба systemd
- Скрипт регулярно отправляет запрос API Telegram на получение нужной информации
- После препроцессинга данных обновления загружаются в базу данных
- При загрузке веб-страницы необходимые данные подгружаются из БД
- При авторизации происходит запрос к БД на совпадение зашифрованных паролей
- Веб-интерфейс позволяет отправить запрос на добавление пользователя в список отслеживаемых

## Архитектура

### Объекты БД

- `User`: пользователь сайта
- `Username`: имя пользователя Telegram
- `Update`: обновление статуса (время, имя пользователя и новый статус)

### Работа с API Telegram

#### `APIManager`

- `__init__` &mdash; инициализирует сессию
- `user_exists(username: Username) -> bool` &mdash; существует ли пользователь
- `get_bio(usernames: Iterable[Username]) -> Iterable[Update]` &mdash; запрашивает статусы пользователей

### Авторизация

- `load_user(id: int) -> User` &mdash; ищет пользователя в БД
- `login_user()`, `logout_user()` из `flask_login`

### Страницы и шаблоны

- /auth/login, /auth/register &mdash; авторизация
- /profile &mdash; страница пользователя
- /updates &mdash; все отслеживаемые пользователи
- /updates/\<username> &mdash; страница обновлений пользователя

### Формы

- `LoginForm`, `RegistrationForm` &mdash; авторизация
- `AddUsernameForm` &mdash; добавление пользователя в список отслеживаемых

#### Валидаторы

- `UserExists`