"""
API client for communicating with backend services.
Uses connection pooling via httpx.Client for optimal performance.
"""

from typing import Any

import httpx
import streamlit as st

from src.config import settings


class APIClient:
    """HTTP client for backend API communication with connection pooling."""

    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or settings.api_base_url).rstrip("/")
        self.token = token or settings.auth_token
        self._client = httpx.Client(
            timeout=settings.api_timeout,
            headers=self._get_headers(),
        )

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _update_token(self, token: str) -> None:
        """Update the auth token for subsequent requests."""
        self.token = token
        self._client.headers.update(self._get_headers())

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}

        if response.is_error:
            error_msg = data.get("message", data.get("detail", "An error occurred"))
            st.error(f"API Error ({response.status_code}): {error_msg}")
            return {"success": False, "error": error_msg}

        return {"success": True, "data": data}

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Send GET request."""
        try:
            response = self._client.get(
                f"{self.base_url}{endpoint}",
                params=params,
            )
            return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}

    def post(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send POST request."""
        try:
            response = self._client.post(
                f"{self.base_url}{endpoint}",
                json=data,
            )
            return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}

    def put(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send PUT request."""
        try:
            response = self._client.put(
                f"{self.base_url}{endpoint}",
                json=data,
            )
            return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}

    def patch(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Send PATCH request."""
        try:
            response = self._client.patch(
                f"{self.base_url}{endpoint}",
                json=data,
            )
            return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Send DELETE request."""
        try:
            response = self._client.delete(
                f"{self.base_url}{endpoint}",
            )
            return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}
