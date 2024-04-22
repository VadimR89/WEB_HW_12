from unittest.mock import Mock, patch
import pytest
from src.services.auth import auth_service


def test_get_contacts(client, get_token):
    """
The test_get_contacts function tests the GET /api/contacts endpoint.
It does so by first mocking out the redis cache, and then making a request to
the endpoint with an Authorization header containing a valid JWT token. The
response is checked for status code 200 (OK), and then its JSON data is checked
to ensure that it contains no contacts.

:param client: Make requests to the flask app
:param get_token: Get a valid token for the test
:return: An empty list
:doc-author: Trelent
"""
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_create_contact(client, get_token, monkeypatch):
    """
The test_create_contact function tests the creation of a contact.
    It does this by first patching the auth_service's cache object to return None, which is what it would do if there was no token in the cache.
    Then, it creates a token using get_token and stores that in headers as an authorization header.
    Next, it sends a POST request to /api/contacts with headers containing our authorization header and json data containing title: test and description: test.
    Finally, we assert that response status code is 201 (created), then we store response data into variable 'data'. We assert that id exists

:param client: Make requests to the api
:param get_token: Get a valid token for the test
:param monkeypatch: Patch the cache object in auth_service
:return: A 201 status code and the contact data
:doc-author: Trelent
"""
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post(
            "/api/contacts", headers=headers, json={"title": "test", "description": "test"}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert 'id' in data
        assert data["title"] == "test"
        assert data["description"] == "test"
