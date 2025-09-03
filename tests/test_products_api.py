import uuid, allure
from tests.allure_helpers import attach_req, attach_resp

def _uuid(): return str(uuid.uuid4())

@allure.epic("Products")
@allure.feature("CRUD")
@allure.title("Позитивный CRUD поток для продуктов: POST/GET list/PATCH/GET by id/DELETE")
def test_products_happy_path(api):
    # ----- POST /products/products
    payload = {
        "name": "Apple",
        "article": _uuid(),
        "category": "VEGETABLES",
        "dictionary": "test dict",
        "price": 1,
        "qty": 2
    }
    url = f"{api.base}{api.e['products_create']}"
    with allure.step("POST /products/products — создать товар"):
        attach_req("POST /products/products", "POST", url, headers=api.s.headers, body=payload)
        r = api.create_product(payload)
        attach_resp("POST /products/products", r)
        assert r.status_code in (200, 201), r.text
        pid = r.json()["id"]

    # ----- GET /products
    url = f"{api.base}{api.e['products_list']}"
    with allure.step("GET /products — список товаров"):
        attach_req("GET /products", "GET", url, headers=api.s.headers)
        r = api.list_products()
        attach_resp("GET /products", r)
        assert r.status_code == 200
        assert any(x.get("id") == pid for x in r.json())

    # ----- PATCH /products
    patch_body = {"id": pid, "name": "Apple Green", "price": 1.5, "qty": 3}
    url = f"{api.base}{api.e['products_patch']}"
    with allure.step("PATCH /products — обновить товар"):
        attach_req("PATCH /products", "PATCH", url, headers=api.s.headers, body=patch_body)
        r = api.patch_product(patch_body)
        attach_resp("PATCH /products", r)
        assert r.status_code in (200, 204), r.text

    # ----- GET /products/{id}
    url = f"{api.base}{api.e['products_by_id']}/{pid}"
    with allure.step("GET /products/{id} — получить товар"):
        attach_req("GET /products/{id}", "GET", url, headers=api.s.headers)
        r = api.get_product(pid)
        attach_resp("GET /products/{id}", r)
        assert r.status_code == 200
        got = r.json()
        assert got["name"] == "Apple Green"
        assert float(got["price"]) == 1.5
        assert float(got["qty"]) == 3
        assert "last_qty_changed" in got

    # ----- DELETE /products/{id}
    url = f"{api.base}{api.e['products_by_id']}/{pid}"
    with allure.step("DELETE /products/{id} — удалить товар"):
        attach_req("DELETE /products/{id}", "DELETE", url, headers=api.s.headers)
        r = api.delete_product(pid)
        attach_resp("DELETE /products/{id}", r)
        assert r.status_code in (200, 204), r.text
