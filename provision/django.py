from invoke import task

from . import common, docker


@task
def manage(context, service="django", command="", compose="dev"):
    """Base template for commands with python manage.py."""
    docker.docker_compose_run(context, service, f"python manage.py {command}", compose)


@task
def makemigrations(context, command=""):
    """Run makemigrations command and chown created migrations."""
    common.success("Django: Make migrations")
    manage(context, f"makemigrations {command}")


@task
def migrate(context, app_name=""):
    """Run ``migrate`` command."""
    common.success("Django: Apply migrations")
    manage(context, f"migrate {app_name}")


@task
def createsuperuser(
    context,
    compose,
    username="root",
    password="root",
    email="root@root.com",
):
    """Create superuser."""
    manage(
        context,
        command=f"createsuperuser2 --username {username} --password {password} --noinput --email {email}",
        compose=compose,
    )


@task
def resetdb(context, apply_migrations=True):
    """Reset database to initial state (including test DB)."""
    common.success("Reset database to its initial state")
    manage(context, "drop_test_database --noinput")
    manage(context, "reset_db -c --noinput")
    if not apply_migrations:
        return
    makemigrations(context)
    migrate(context)
    createsuperuser(context)


@task
def shell(context, params=""):
    """Shortcut for manage.py shell_plus command.

    Additional params available here:
        https://django-extensions.readthedocs.io/en/latest/shell_plus.html
    """
    common.success("Entering Django Shell")
    manage(context, command="shell")
