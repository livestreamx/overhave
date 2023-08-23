import typer

from overhave.base_settings import DataBaseSettings, LoggingSettings
from overhave.cli.group import overhave
from overhave.factory import ConsumerFactory
from overhave.metrics import get_common_metric_container
from overhave.transport import RedisStream


def _run_consumer(stream: RedisStream) -> None:
    DataBaseSettings().setup_engine()
    LoggingSettings().setup_logging()
    ConsumerFactory(stream=stream, metric_container=get_common_metric_container()).runner.run()


@overhave.command(short_help="Run Overhave Redis consumer")
def consumer(
    stream: RedisStream = typer.Option(..., "-s", "--stream", help="Redis stream, which defines application")
) -> None:
    """Run Overhave Redis consumer."""
    _run_consumer(stream)
