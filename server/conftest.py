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
        created_client.delete()


@pytest.fixture
def waiter(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.WAITER)
        yield created_employee
        created_employee.delete()


@pytest.fixture
def bartender(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.BARTENDER)
        yield created_employee
        created_employee.delete()


@pytest.fixture
def cook(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.COOK)
        yield created_employee
        created_employee.delete()


@pytest.fixture
def chef(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.CHEF)
        yield created_employee
        created_employee.delete()


@pytest.fixture
def manager(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.MANAGER)
        yield created_employee
        created_employee.delete()


@pytest.fixture
def hostess(django_db_setup, django_db_blocker):
    """Module-level fixture for employee."""
    with django_db_blocker.unblock():
        created_employee = EmployeeFactory(role=Employee.Roles.HOSTESS)
        yield created_employee
        created_employee.delete()


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()
