import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_client_ip(request) -> str:
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def log_request(request, response=None, level: str = "INFO") -> None:
    """Log API request details."""
    log_data = {
        "method": request.method,
        "path": request.path,
        "user": str(request.user) if request.user.is_authenticated else "anonymous",
        "ip": get_client_ip(request),
    }
    if response:
        log_data["status_code"] = response.status_code

    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"API Request: {log_data}")
