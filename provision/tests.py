from invoke import task

from . import common, docker


@task
def pytest(context, service="django", params=""):
    """Run django tests."""
    common.success("Tests running")
    docker.docker_compose_run(context, service=service, command=f"pytest {params}")
