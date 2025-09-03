# BR-001: POST /order возвращает plain text вместо JSON

**Окружение:** локально, Docker (evgen73ul/warehouse:ms6), macOS, сервис http://localhost:8080  
**Предусловия:** существует активный клиент (customer_id=1), доступный товар

## Шаги воспроизведения (позитив)
1) POST /products/products — создать товар с валидным payload  
2) POST /order (Header `customer_id: 1`), тело:
   ```json
   {
     "deliveryAddress": "Test street",
     "products": [{"id": "<ID созданного товара>", "qty": 5}]
   }

#Ожидаемо (для позитивного успешного создания):

HTTP 201/200,

Content-Type: application/json,

тело — JSON с идентификатором заказа ({"id": "..."} или {"orderId": "..."}) и/или краткой сводкой.

Фактически:

HTTP 200/201 (успешно),

Content-Type не JSON (вероятно text/plain),

тело — строка с ID, из-за чего r.json() падает. Мы вынуждены парсить как текст.

Доказательства:

Allure шаг “POST /order — создать заказ” в тесте test_order_full_flow:

вложение POST /order — RESPONSE.txt — виден строковый ID;

вложение POST /order — META.json — заголовок ответа (Content-Type) не application/json (проверь в отчёте; приложи скрин).

Влияние: Клиентские обёртки/SDK и автотесты ожидают JSON-контракт; требуется спец-обработка строкового ответа.

Серьёзность: Minor/Medium (функционально заказ создаётся, но контракт нестабилен).

Рекомендация: Возвращать JSON c полем id/orderId и корректным Content-Type: application/json.