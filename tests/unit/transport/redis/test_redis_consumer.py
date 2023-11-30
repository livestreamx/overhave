import walrus
from overhave.transport.redis import RedisConsumer
from overhave.transport.redis.settings import BaseRedisSettings
from overhave.metrics import BaseOverhaveMetricContainer
from overhave.transport.redis.objects import RedisStream
from overhave.transport.redis.settings import BaseRedisSettings

import pytest


class TestRedisConsumer:
    """Unit tests for :class:`RedisConsumer`."""

    @pytest.fixture()
    def settings(self) -> BaseRedisSettings:
        return BaseRedisSettings()

    @pytest.fixture()
    def metric_container(self) -> BaseOverhaveMetricContainer:
        return BaseOverhaveMetricContainer(registry="some_registry")

    @pytest.mark.parametrize(
        ("settings", "stream_name", "database", "metric_container"),
        [
            (settings, RedisStream.TEST, walrus.Database(host="localhost", port=6379, db=0), metric_container),
        ],
    )
    def test_field_initialization(
            self,
            settings: BaseRedisSettings,
            stream_name: RedisStream,
            database: walrus.Database,
            metric_container: BaseOverhaveMetricContainer,
    ) -> None:
        redis_consumer = RedisConsumer(
            settings=settings, stream_name=stream_name, database=database, metric_container=metric_container
        )

        assert redis_consumer._settings == settings
        assert redis_consumer._stream_name == stream_name
        assert redis_consumer._database == database
        assert redis_consumer._metric_container == metric_container
