import requests
from typing import Any, Dict

class ApiClient:
    def __init__(self, base_url: str, endpoints: Dict[str, str]):
        self.base = base_url.rstrip("/")
        self.e = endpoints
        self.s = requests.Session()
        self.s.headers.update({"Content-Type": "application/json"})

    # ------- Products -------
    def create_product(self, payload: Dict[str, Any]):
        # POST /products/products
        return self.s.post(f"{self.base}{self.e['products_create']}", json=payload)

    def list_products(self, params=None):
        # GET /products
        return self.s.get(f"{self.base}{self.e['products_list']}", params=params)

    def get_product(self, product_id: str):
        # GET /products/{{id}}
        return self.s.get(f"{self.base}{self.e['products_by_id']}/{product_id}")

    def patch_product(self, payload: Dict[str, Any]):
        # PATCH /products  (payload должен содержать id)
        return self.s.patch(f"{self.base}{self.e['products_patch']}", json=payload)

    def delete_product(self, product_id: str):
        # DELETE /products/{{id}}
        return self.s.delete(f"{self.base}{self.e['products_by_id']}/{product_id}")

    # ------- Orders (обязателен header customer_id) -------
    def create_order(self, payload: Dict[str, Any], customer_id: int):
        # POST /order
        return self.s.post(
            f"{self.base}{self.e['orders_create']}",
            json=payload,
            headers={"customer_id": str(customer_id)},
        )

    def get_order(self, order_id: str, customer_id: int):
        # GET /order/{{id}}
        return self.s.get(
            f"{self.base}{self.e['orders_by_id']}/{order_id}",
            headers={"customer_id": str(customer_id)},
        )

    def delete_order(self, order_id: str, customer_id: int):
        # DELETE /order/{{id}}
        return self.s.delete(
            f"{self.base}{self.e['orders_by_id']}/{order_id}",
            headers={"customer_id": str(customer_id)},
        )

    def patch_order(self, order_id: str, payload: Dict[str, Any], customer_id: int):
        # PATCH /order/{{id}}
        return self.s.patch(
            f"{self.base}{self.e['orders_by_id']}/{order_id}",
            json=payload,
            headers={"customer_id": str(customer_id)},
        )
