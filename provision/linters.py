from invoke import Exit, UnexpectedExit, task

from . import common, docker, git

DEFAULT_FOLDERS = "."


@task
def isort(
    context,
    path=DEFAULT_FOLDERS,
    service="django",
    params="",
    compose="dev",
):
    """Command to fix imports formatting."""
    common.success("Linters: ISort running")
    docker.docker_compose_run(context, service, f"isort {path} {params}", compose)


@task
def black(context, path=DEFAULT_FOLDERS, service="django", compose="dev"):
    """Run `black` linter."""
    common.success("Linters: Black running")
    docker.docker_compose_run(context, service, f"black {path}", compose)


@task
def flake8(context, path=DEFAULT_FOLDERS, service="django", compose="dev"):
    """Run `flake8` linter."""
    common.success("Linters: Flake8 running")
    docker.docker_compose_run(context, service, "flake8 --config=./setup.cfg", compose)


@task
def all(context, path=DEFAULT_FOLDERS):
    """Run all linters."""
    common.success("Linters: Running all linters")
    linters = (isort, black, flake8)
    failed = []
    for linter in linters:
        try:
            linter(context, path)
        except UnexpectedExit:
            failed.append(linter.__name__)
    if failed:
        common.error(
            f"Linters failed: {', '.join(map(str.capitalize, failed))}",
        )
        raise Exit(code=1)
