# AQA Tests — MediaSoft Warehouse API

Автоматизированные API-тесты для тестового задания MediaSoft.  
Тесты покрывают все методы, представленные в Swagger UI сервиса warehouse.

---

## 📋 Содержание
1. [Предусловия](#предусловия)  
2. [Стек](#стек)  
3. [Структура проекта](#структура-проекта)  
4. [Установка и запуск](#установка-и-запуск)  
5. [Переменные окружения (.env)](#переменные-окружения-env)  
6. [Запуск отчёта Allure](#запуск-отчёта-allure)  
7. [Покрытие тестами](#покрытие-тестами)  
8. [Баг-репорты](#баг-репорты)  
9. [Видео](#видео)

---

## Предусловия
- Установлен [Docker Desktop](https://www.docker.com/products/docker-desktop/).  
- Сервис поднят командой:
  ```bash
  docker compose up -d
Swagger доступен по адресу: http://localhost:8080/swagger-ui/index.html

Установлен Python 3.10+ и pip.

Установлен Allure CLI (для отчётов):

bash
Копировать код
brew install allure
Стек
pytest — тестовый раннер

requests — HTTP-клиент

allure-pytest — отчёты

python-dotenv — конфиги через .env

psycopg2-binary — подключение к PostgreSQL для предусловий

Структура проекта
bash
Копировать код
aqa-tests/
├─ src/                   # клиент API и DB
│  ├─ api_client.py
│  └─ db_client.py
├─ tests/                 # автотесты
│  ├─ test_products_api.py
│  ├─ test_orders_api.py
│  └─ allure_helpers.py
├─ reports/
│  ├─ bugs/               # баг-репорты
│  │   └─ BR-001-post-order-plain-text.md
│  └─ screenshots/        # скриншоты из Allure
├─ .env                   # настройки окружения
├─ requirements.txt
├─ pytest.ini
└─ README.md
Установка и запуск
bash
Копировать код
# 1. Клонировать проект
git clone <url-репозитория>
cd aqa-tests

# 2. Создать и активировать venv
python3 -m venv .venv
source .venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить тесты
pytest
Переменные окружения (.env)
Пример .env:

env
Копировать код
BASE_URL=http://localhost:8080

# Products
PRODUCTS_LIST=/products
PRODUCTS_CREATE=/products/products
PRODUCTS_PATCH=/products
PRODUCTS_BY_ID=/products

# Orders
ORDERS_CREATE=/order
ORDERS_BY_ID=/order

# Для заказов нужен активный клиент
CUSTOMER_ID=1

# Подключение к Postgres
PG_HOST=localhost
PG_PORT=5432
PG_DB=postgres_db
PG_USER=postgres_user
PG_PASSWORD=postgres_password
⚠️ Если CUSTOMER_ID не задан или в БД нет клиента с таким id — позитивные тесты заказов будут SKIP. Это корректное предусловие.

Запуск отчёта Allure
bash
Копировать код
pytest
allure serve allure-results
В отчёте для каждого метода API видно:

шаг (например: POST /products/products — создать товар, GET /order/{id} — получить заказ),

вложения:

REQUEST.json — метод, URL, заголовки, тело запроса,

RESPONSE.json/txt — тело ответа,

META.json — статус, заголовки запроса/ответа.

Покрытие тестами
Модуль	Метод/путь	Проверяется в тесте
Products	POST /products/products	test_products_api.py
Products	GET /products	test_products_api.py
Products	PATCH /products	test_products_api.py
Products	GET /products/{id}	test_products_api.py
Products	DELETE /products/{id}	test_products_api.py
Orders	POST /order	test_orders_api.py
Orders	GET /order/{id}	test_orders_api.py
Orders	PATCH /order/{id}	test_orders_api.py
Orders	DELETE /order/{id}	test_orders_api.py

Баг-репорты
Все баги по позитивным сценариям находятся в reports/bugs.

BR-001: POST /order возвращает plain text вместо JSON
→ фактически заказ создаётся, но контракт API нестабилен (ожидался JSON с id, пришла строка).
Скриншоты и вложения — в reports/screenshots.

Видео
К записи демонстрации включены:

Swagger UI со всеми методами.

Запуск pytest (оба теста passed).

Отчёт Allure с шагами и вложениями.

Демонстрация баг-репорта в папке reports/bugs/.