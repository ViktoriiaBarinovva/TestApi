import json, allure

def _jsonable(x):
    """Аккуратно приводим объекты к сериализуемым типам."""
    if x is None:
        return None
    # CaseInsensitiveDict и прочие мапы
    try:
        return dict(x)
    except Exception:
        pass
    # Списки/кортежи/множества
    if isinstance(x, (list, tuple, set)):
        return [ _jsonable(v) for v in x ]
    # Примитивы или уже JSON-совместимые
    try:
        json.dumps(x)
        return x
    except Exception:
        return str(x)

def attach_req(name, method, url, headers=None, body=None, params=None):
    meta = {
        "method": method,
        "url": url,
        "headers": _jsonable(headers) or {},
        "params": _jsonable(params) or {},
        "body": _jsonable(body),
    }
    allure.attach(json.dumps(meta, ensure_ascii=False, indent=2),
                  f"{name} — REQUEST.json", allure.attachment_type.JSON)

def attach_resp(name, response):
    summary = {
        "status_code": response.status_code,
        "url": getattr(response.request, "url", ""),
        "method": getattr(response.request, "method", ""),
        "request_headers": _jsonable(getattr(response.request, "headers", {})),
        "response_headers": _jsonable(response.headers),
    }
    # тело ответа: JSON или текст
    try:
        body = response.json()
        allure.attach(json.dumps(body, ensure_ascii=False, indent=2),
                      f"{name} — RESPONSE.json", allure.attachment_type.JSON)
    except Exception:
        allure.attach(response.text, f"{name} — RESPONSE.txt", allure.attachment_type.TEXT)

    allure.attach(json.dumps(summary, ensure_ascii=False, indent=2),
                  f"{name} — META.json", allure.attachment_type.JSON)