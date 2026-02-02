"""
Rate Limiting Middleware
"""
from fastapi import Request, HTTPException
from item.app.core.config.settings import settings
import time

class RateLimitMiddleware:
    def __init__(self, app):
        self.app = app
        self.requests = {}
    
    async def __call__(self, scope, receive, send):
        if not settings.RATE_LIMIT_ENABLED:
            await self.app(scope, receive, send)
            return
        
        if scope["type"] == "http":
            client_ip = scope["client"][0]
            current_time = time.time()
            
            # Clean old requests
            self.requests = {k: v for k, v in self.requests.items() if current_time - v < 60}
            
            # Check rate limit
            if client_ip in self.requests and len([r for r in self.requests.values() if r >= current_time - 60]) > settings.RATE_LIMIT_PER_MINUTE:
                raise HTTPException(status_code=429, detail="Too many requests")
            
            self.requests[client_ip] = current_time
        
        await self.app(scope, receive, send)
