from time import perf_counter


class ResponseTimeMiddleware:
    """最小的自訂 middleware：量測整個後續 request/response 鏈耗時。

    `MIDDLEWARE` 的順序很重要：request 由上往下進入、response 由下往上返回。
    這個範例只加入觀察用 header，不把效能資料寫入資料庫，避免每次請求又製造額外 I/O。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = perf_counter()
        response = self.get_response(request)
        elapsed_ms = (perf_counter() - started) * 1000
        response["X-Response-Time"] = f"{elapsed_ms:.2f}ms"
        return response
