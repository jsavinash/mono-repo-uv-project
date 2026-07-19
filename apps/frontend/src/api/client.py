"""
API client for communicating with backend services.
"""

from typing import Any

import httpx
import streamlit as st

from src.config import settings


class APIClient:
    """HTTP client for backend API communication."""

    def __init__(self, base_url: str | None = None, token: str | None = None):
        self.base_url = (base_url or settings.api_base_url).rstrip("/")
        self.token = token or settings.auth_token

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

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
            with httpx.Client(timeout=settings.api_timeout) as client:
                response = client.get(
                    f"{self.base_url}{endpoint}",
                    headers=self._get_headers(),
                    params=params,
                )
                return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}

    def post(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send POST request."""
        try:
            with httpx.Client(timeout=settings.api_timeout) as client:
                response = client.post(
                    f"{self.base_url}{endpoint}",
                    headers=self._get_headers(),
                    json=data,
                )
                return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}

    def put(self, endpoint: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send PUT request."""
        try:
            with httpx.Client(timeout=settings.api_timeout) as client:
                response = client.put(
                    f"{self.base_url}{endpoint}",
                    headers=self._get_headers(),
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
            with httpx.Client(timeout=settings.api_timeout) as client:
                response = client.patch(
                    f"{self.base_url}{endpoint}",
                    headers=self._get_headers(),
                    json=data,
                )
                return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}

    def delete(self, endpoint: str) -> dict[str, Any]:
        """Send DELETE request."""
        try:
            with httpx.Client(timeout=settings.api_timeout) as client:
                response = client.delete(
                    f"{self.base_url}{endpoint}",
                    headers=self._get_headers(),
                )
                return self._handle_response(response)
        except httpx.RequestError as e:
            st.error(f"Connection error: {e}")
            return {"success": False, "error": str(e)}
