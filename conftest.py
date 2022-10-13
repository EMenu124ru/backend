import pytest
from rest_framework import test


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def auth_client(user, client):
    """Fixture for authtorized client."""
    client.force_login(user=user)
    return client


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()
