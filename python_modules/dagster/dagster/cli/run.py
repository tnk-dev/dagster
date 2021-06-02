import click
from dagster.core.instance import DagsterInstance


@click.group(name="run")
def run_cli():
    """
    Commands for working with Dagster pipeline runs.
    """


@run_cli.command(name="list", help="List the runs in the current Dagster instance.")
@click.option("--limit", help="Only list a specified number of runs", default=None, type=int)
def run_list_command(limit):
    with DagsterInstance.get() as instance:
        for run in instance.get_runs(limit=limit):
            click.echo("Run: {}".format(run.run_id))
            click.echo("     Pipeline: {}".format(run.pipeline_name))


@run_cli.command(
    name="delete",
    help="Delete a run by id and its associated event logs. Warning: Cannot be undone",
)
@click.argument("run_id")
def run_delete_command(run_id):
    with DagsterInstance.get() as instance:
        if not instance.has_run(run_id):
            click.echo(f"No run found with id {run_id}.")

        confirmation = click.prompt(
            f"Are you sure you want to delete run {run_id} and its event logs? Type DELETE"
        )
        if confirmation == "DELETE":
            instance.delete_run(run_id)
            click.echo(f"Deleted run {run_id} and its event log entries.")
        else:
            click.echo("Exiting without deleting run.")


@run_cli.command(
    name="wipe", help="Eliminate all run history and event logs. Warning: Cannot be undone"
)
def run_wipe_command():
    confirmation = click.prompt(
        "Are you sure you want to delete all run history and event logs? Type DELETE"
    )
    if confirmation == "DELETE":
        with DagsterInstance.get() as instance:
            instance.wipe()
        click.echo("Deleted all run history and event logs")
    else:
        click.echo("Exiting without deleting all run history and event logs")
