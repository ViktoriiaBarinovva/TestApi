import os, uuid, json, pytest, allure
from pathlib import Path
from dotenv import load_dotenv
from tests.allure_helpers import attach_req, attach_resp

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT / ".env", override=True)

def _uuid(): return str(uuid.uuid4())

@allure.epic("Orders")
@allure.feature("Full flow")
@allure.title("Позитивный поток заказов: POST/GET/PATCH/DELETE (при наличии CUSTOMER_ID)")
def test_order_full_flow(api):
    cid_raw = os.getenv("CUSTOMER_ID", "").strip()
    customer_id = int(cid_raw) if cid_raw.isdigit() else None
    if customer_id is None:
        pytest.skip("Пропущено: не задан CUSTOMER_ID (позитив требует существующего клиента).")

    # POST /products/products (подготовка товара)
    prod_payload = {"name":"Orange","article":_uuid(),"category":"FRUITS","price":2.0,"qty":50,"dictionary":"sweet"}
    url = f"{api.base}{api.e['products_create']}"
    with allure.step("POST /products/products — подготовить товар для заказа"):
        attach_req("POST /products/products", "POST", url, headers=api.s.headers, body=prod_payload)
        pr = api.create_product(prod_payload)
        attach_resp("POST /products/products", pr)
        assert pr.status_code in (200, 201), pr.text
        product_id = pr.json()["id"]

    # POST /order — создать заказ
    order_payload = {"deliveryAddress":"Test street","products":[{"id":product_id,"qty":5}]}
    url = f"{api.base}{api.e['orders_create']}"
    with allure.step("POST /order — создать заказ"):
        headers = {"customer_id": str(customer_id), **api.s.headers}
        attach_req("POST /order", "POST", url, headers=headers, body=order_payload)
        r = api.create_order(order_payload, customer_id=customer_id)
        attach_resp("POST /order", r)
        assert r.status_code in (200, 201), r.text
        order_id = None
        try:
            body = r.json()
            if isinstance(body, dict):
                order_id = body.get("orderId") or body.get("id")
        except Exception:
            pass
        if not order_id:
            order_id = r.text.strip().strip('"').strip("'")
        assert order_id, f"Не удалось определить id заказа из ответа: {r.text}"

    # GET /order/{id}
    url = f"{api.base}{api.e['orders_by_id']}/{order_id}"
    with allure.step("GET /order/{id} — получить заказ по ID"):
        headers = {"customer_id": str(customer_id), **api.s.headers}
        attach_req("GET /order/{id}", "GET", url, headers=headers)
        gr = api.get_order(order_id, customer_id=customer_id)
        attach_resp("GET /order/{id}", gr)
        assert gr.status_code == 200, gr.text

    # PATCH /order/{id}
    patch_body = {"products":[{"id":product_id,"qty":7}]}
    url = f"{api.base}{api.e['orders_by_id']}/{order_id}"
    with allure.step("PATCH /order/{id} — редактировать заказ"):
        headers = {"customer_id": str(customer_id), **api.s.headers}
        attach_req("PATCH /order/{id}", "PATCH", url, headers=headers, body=patch_body)
        prr = api.patch_order(order_id, patch_body, customer_id=customer_id)
        attach_resp("PATCH /order/{id}", prr)
        assert prr.status_code in (200, 204), prr.text

    # DELETE /order/{id}
    url = f"{api.base}{api.e['orders_by_id']}/{order_id}"
    with allure.step("DELETE /order/{id} — удалить заказ по ID"):
        headers = {"customer_id": str(customer_id), **api.s.headers}
        attach_req("DELETE /order/{id}", "DELETE", url, headers=headers)
        dr = api.delete_order(order_id, customer_id=customer_id)
        attach_resp("DELETE /order/{id}", dr)
        assert dr.status_code in (200, 204), dr.text
