# Название проекта: Parser reviews 2Gis

## Инструкции по установке и запуску в Docker:

### 1.1 Eсли вы используете готовый образ из Docker Hub::

docker pull iskandar54/gis_parser:1.0

### 1.2 Или скачиваем с Git Hub:

git clone https://github.com/Iskandar54/gis-parser.git
cd 2gis-parser

### 2. Создайте `.env` файл с настройками:

BRANCH_URLS=url1,url2,url3
TG_BOT_TOKEN=your_token
TG_CHAT_ID=your_chat_id

### 3. Соберите Docker-образ:

docker build -t gis-parser .

### 4. Запустите контейнер с использованием .env:

docker run -d --env-file "Ваш путь до\.env" --name gis-parser gis-parser

### 4.2 Если используете образ из Docker Hub:

docker run -d --env-file "Ваш путь до\.env" --name gis-parser iskandar54/gis-parser:latest


## Как добавить новые филиалы:

### Открываем .env:

#### В переменной BRANCH_URLS добавьте новые ссылки, разделяя их запятыми

Но учтите, что скрипт написан на ThreadPoolExecutor, так что поток ограничен

## Как проверить результаты:

### 1. Проверить логи cron:

docker exec -it gis-parser tail -f /app/logs/cron.log

### 2. Проверить логи приложения:

docker exec -it gis-parser tail -f /app/logs/logger_config.log

### 3. Проверить содержимое базы данных SQLite:

docker exec -it gis-parser sqlite3 /app/reviews.db

#### Пример:

SELECT * FROM reviews ORDER BY date DESC LIMIT 10;

## Telegram уведомления:

### Скрипт отправляет уведомления о новых отзывах в указанный вами Telegram-чат:

#### Создайте бота через @BotFather 

#### Получите TG_BOT_TOKEN

#### Добавьте бота в чат и узнайте TG_CHAT_ID, чтобы скрипт мог отправлять вам уведомления

##### Примечние: если не начинать диалог с ботов, вероятнее всего он не сможет отправлять вам уведомления

## Расписание запуска

### Периодичность можно изменить в init_cron.py

#### Текущее значение: 0 10 * * *   - каждый день в 10:00 по Москве
