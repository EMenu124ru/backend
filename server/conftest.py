import pytest
from rest_framework import test

from apps.users.factories import ClientFactory, EmployeeFactory
from apps.users.models import Employee


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def client(django_db_setup, django_db_blocker):
    """Module-level fixture for client."""
    with django_db_blocker.unblock():
        created_client = ClientFactory()
        yield created_client
        created_client.user.delete()
        created_client.delete()


@pytest.fixture
def waiter(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.WAITER)
        if created_employee.user.is_client:
            created_employee.user.client.delete()
        yield created_employee
        created_employee.user.delete()
        created_employee.delete()


@pytest.fixture
def cook(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.COOK)
        if created_employee.user.is_client:
            created_employee.user.client.delete()
        yield created_employee
        created_employee.user.delete()
        created_employee.delete()


@pytest.fixture
def chef(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.CHEF)
        if created_employee.user.is_client:
            created_employee.user.client.delete()
        yield created_employee
        created_employee.user.delete()
        created_employee.delete()


@pytest.fixture
def sous_chef(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.SOUS_CHEF)
        if created_employee.user.is_client:
            created_employee.user.client.delete()
        yield created_employee
        created_employee.user.delete()
        created_employee.delete()


@pytest.fixture
def manager(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.MANAGER)
        if created_employee.user.is_client:
            created_employee.user.client.delete()
        yield created_employee
        created_employee.user.delete()
        created_employee.delete()


@pytest.fixture
def hostess(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.HOSTESS)
        if created_employee.user.is_client:
            created_employee.user.client.delete()
        yield created_employee
        created_employee.user.delete()
        created_employee.delete()


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()
