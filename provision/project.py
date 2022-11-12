from invoke import task

from . import common, django, docker


@task
def fill_sample_data(context):
    """Prepare sample data for local usage."""
    django.manage(context, command="runscript fill_sample_data")


@task
def init(context, compose="prod"):
    """Prepare env for working with project."""
    docker.build(context, compose=compose)
    django.manage(context, command="migrate", compose=compose)
    django.createsuperuser(context, compose=compose)
    try:
        fill_sample_data(context)
    except NotImplementedError:
        common.warn(
            "Awesome, almost everything is Done! \n"
            "You're the first developer - pls generate factories \n"
            "for test data and setup development environment",
        )
