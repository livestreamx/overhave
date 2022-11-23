import pytest
from faker import Faker
from pytest_redis import factories

from overhave.entities.settings import OverhaveRedisSettings
from overhave.factory import ConsumerFactory
from overhave.transport import RedisProducer, RedisStream, TestRunTask

redis_noproc = factories.redis_noproc(port="6379")
redisdb = factories.redisdb("redis_noproc", dbnum=1)


@pytest.fixture()
def redis_consumer_factory() -> ConsumerFactory:
    return ConsumerFactory(stream=RedisStream.TEST)


@pytest.fixture()
def redis_producer() -> RedisProducer:
    return RedisProducer(settings=OverhaveRedisSettings(), mapping={TestRunTask: RedisStream.TEST})


@pytest.fixture()
def run_id(faker: Faker) -> int:
    return faker.pyint()
