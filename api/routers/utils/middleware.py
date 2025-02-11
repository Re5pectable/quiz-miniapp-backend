from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from traceback import format_exc
from ...config import DEBUG


class TryExceptMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            print(str(e))
            if DEBUG:
                format_exc()
            return JSONResponse(status_code=409, content={"detail": "Sorry, something went wrong."})
