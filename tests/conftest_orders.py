# tests/conftest_orders.py
import uuid
import pytest

CUSTOMER_ID = 1

@pytest.fixture(scope="session", autouse=True)
def ensure_active_customer(db):
    # если таблица/роль называется иначе — скажи, поправлю SQL
    row = db.fetchone("SELECT id, is_active FROM customer WHERE id=%s;", (CUSTOMER_ID,))
    if row:
        db.execute("UPDATE customer SET is_active=true WHERE id=%s;", (CUSTOMER_ID,))
        return

    login = f"autotest_{uuid.uuid4().hex[:8]}"
    email = f"{login}@example.com"
    db.execute("""
        INSERT INTO customer (id, login, email, is_active)
        VALUES (%s, %s, %s, true)
    """, (CUSTOMER_ID, login, email))
