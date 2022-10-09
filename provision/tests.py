from invoke import task

from . import common, docker


@task
def pytest(context, service="server", compose="dev"):
    """Run django tests."""
    common.success("Tests running")
    docker.docker_compose_exec(context, service, "pytest", compose)
