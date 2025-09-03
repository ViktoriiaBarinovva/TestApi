import os
import pytest
from dotenv import load_dotenv
from src.api_client import ApiClient
from src.db_client import DbClient

load_dotenv()

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ["BASE_URL"].rstrip("/")

@pytest.fixture(scope="session")
def endpoints() -> dict:
    return {
        "products_list": os.environ["PRODUCTS_LIST"].rstrip("/"),
        "products_create": os.environ["PRODUCTS_CREATE"].rstrip("/"),
        "products_patch": os.environ["PRODUCTS_PATCH"].rstrip("/"),
        "products_by_id": os.environ["PRODUCTS_BY_ID"].rstrip("/"),
        "orders_create": os.environ["ORDERS_CREATE"].rstrip("/"),
        "orders_by_id": os.environ["ORDERS_BY_ID"].rstrip("/"),
    }

@pytest.fixture(scope="session")
def api(base_url, endpoints) -> ApiClient:
    return ApiClient(base_url, endpoints)

@pytest.fixture(scope="session")
def db():
    # Если проверки в БД не используются, просто не импортируйте фикстуру db в тестах
    return DbClient(
        host=os.environ.get("PG_HOST", "localhost"),
        port=int(os.environ.get("PG_PORT", "5432")),
        database=os.environ.get("PG_DB", "postgres_db"),
        user=os.environ.get("PG_USER", "postgres_user"),
        password=os.environ.get("PG_PASSWORD", "postgres_password"),
    )
