from unittest.mock import Mock, patch, AsyncMock
import pytest
from src.services.auth import auth_service


def test_get_me(client, get_token, monkeypatch):
    """
The test_get_me function tests the /api/users/me endpoint.
It does so by first patching the auth_service's cache with a mock redis object, and then setting up mocks for
the FastAPILimiter class' redis, identifier, and http_callback methods. It then creates a token using get_token
and adds it to an Authorization header before sending a GET request to /api/users/me. Finally it asserts that the
response status code is 200.

:param client: Make requests to the api
:param get_token: Get the token from the fixture
:param monkeypatch: Mock the redis, identifier and http_callback functions
:return: The user's information
:doc-author: Trelent
"""    
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/users/me", headers=headers)
        assert response.status_code == 200, response.text
