import pytest
import walrus

from overhave.metrics import BaseOverhaveMetricContainer
from overhave.transport.redis import RedisConsumer
from overhave.transport.redis.objects import RedisStream
from overhave.transport.redis.settings import BaseRedisSettings


class TestRedisConsumer:
    """Unit tests for redis-consumer."""

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

    @pytest.mark.parametrize(
        ("settings", "stream_name", "database", "metric_container"),
        [
            (settings, RedisStream.EMULATION, walrus.Database(host="localhost", port=6379, db=0), metric_container),
        ],
    )
    def test_consumer_group_with_empty_keys(
        self,
        settings: BaseRedisSettings,
        stream_name: RedisStream,
        database: walrus.Database,
        metric_container: BaseOverhaveMetricContainer,
    ) -> None:
        redis_consumer = RedisConsumer(
            settings=settings, stream_name=stream_name, database=database, metric_container=metric_container
        )

        cg = redis_consumer._consumer_group
        assert len(cg.emulation) == 0

    @pytest.mark.parametrize(
        ("settings", "stream_name", "database", "metric_container"),
        [
            (settings, RedisStream.TEST, walrus.Database(host="localhost", port=6379, db=0), metric_container),
        ],
    )
    def test_consumer_group_with_not_empty_keys(
        self,
        settings: BaseRedisSettings,
        stream_name: RedisStream,
        database: walrus.Database,
        metric_container: BaseOverhaveMetricContainer,
    ) -> None:
        redis_consumer = RedisConsumer(
            settings=settings, stream_name=stream_name, database=database, metric_container=metric_container
        )

        cg = redis_consumer._consumer_group
        cg.test.add({"message": "new faq beach"})

        assert len(cg.test.read()) != 0

    @pytest.mark.parametrize(
        ("settings", "stream_name", "database", "metric_container"),
        [
            (settings, RedisStream.PUBLICATION, walrus.Database(host="localhost", port=6379, db=0), metric_container),
        ],
    )
    def test_stream(
        self,
        settings: BaseRedisSettings,
        stream_name: RedisStream,
        database: walrus.Database,
        metric_container: BaseOverhaveMetricContainer,
    ) -> None:
        redis_consumer = RedisConsumer(
            settings=settings, stream_name=stream_name, database=database, metric_container=metric_container
        )

        assert redis_consumer._stream.pending() == redis_consumer._consumer_group.publication.pending()

    @pytest.mark.parametrize(
        ("settings", "stream_name", "database", "metric_container"),
        [
            (settings, RedisStream.TEST, walrus.Database(host="localhost", port=6379, db=0), metric_container),
        ],
    )
    def test_clean_pending_with_msgs(
        self,
        settings: BaseRedisSettings,
        stream_name: RedisStream,
        database: walrus.Database,
        metric_container: BaseOverhaveMetricContainer,
    ) -> None:
        redis_consumer = RedisConsumer(
            settings=settings, stream_name=stream_name, database=database, metric_container=metric_container
        )

        cg = redis_consumer._consumer_group
        cg.test.add({"message": "new faq beach"})
        assert len(cg.test.read()) > 0

        redis_consumer._clean_pending()
        assert len(redis_consumer._stream.pending()) == 0

    @pytest.mark.parametrize(
        ("settings", "stream_name", "database", "metric_container"),
        [
            (settings, RedisStream.PUBLICATION, walrus.Database(host="localhost", port=6379, db=0), metric_container),
        ],
    )
    def test_clean_consume_with_no_msgs(
        self,
        settings: BaseRedisSettings,
        stream_name: RedisStream,
        database: walrus.Database,
        metric_container: BaseOverhaveMetricContainer,
    ) -> None:
        redis_consumer = RedisConsumer(
            settings=settings, stream_name=stream_name, database=database, metric_container=metric_container
        )

        redis_consumer._clean_pending()
        assert len(redis_consumer._stream.pending()) == 0

    @pytest.mark.parametrize(
        ("settings", "stream_name", "database", "metric_container"),
        [
            (
                BaseRedisSettings(read_count=3),
                RedisStream.TEST,
                walrus.Database(host="localhost", port=6379, db=0),
                metric_container,
            ),
        ],
    )
    def test_clean_consume_with_msgs(
        self,
        settings: BaseRedisSettings,
        stream_name: RedisStream,
        database: walrus.Database(host="localhost", port=6379, db=0),
        metric_container: BaseOverhaveMetricContainer,
    ) -> None:
        redis_consumer = RedisConsumer(
            settings=settings, stream_name=stream_name, database=database, metric_container=metric_container
        )

        cg = redis_consumer._consumer_group
        cg.test.add({"message": "new faq beach"})
        cg.test.add({"message": "I REGRET EVERYTHING IVE DONE. DJ SORROW"})
        cg.test.add({"message": "DJ SORROW TURN THE FUCK UP"})

        assert len(redis_consumer._consume()) == 3
