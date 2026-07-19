"""
Logging Middleware
"""

import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()

            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    process_time = time.time() - start_time
                    logger.info(
                        f"{scope['method']} {scope['path']} - {process_time:.3f}s"
                    )
                await send(message)

            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)
