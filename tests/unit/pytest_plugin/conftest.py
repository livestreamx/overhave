from typing import Any, Callable, Mapping, cast
from unittest import mock

import allure
import httpx
import pytest
from _pytest.config import Config, PytestPluginManager
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from _pytest.main import Session
from _pytest.nodes import Item, Mark
from _pytest.python import Function
from faker import Faker
from pytest_bdd.parser import Feature, Scenario, Step

from overhave import (
    OverhaveDescriptionManagerSettings,
    OverhaveProjectSettings,
    OverhaveStepContextSettings,
    OverhaveTestExecutionContext,
)
from overhave.factory import ITestExecutionFactory
from overhave.factory.context.base_context import BaseFactoryContext
from overhave.pytest_plugin import DescriptionManager, StepContextRunner
from overhave.pytest_plugin.helpers import OverhaveTagController
from overhave.pytest_plugin.proxy_manager import IProxyManager
from tests.objects import get_test_feature_extractor, get_test_file_settings
from tests.unit.pytest_plugin.getoption_mock import ConfigGetOptionMock


@pytest.fixture()
def test_clean_item(faker: Faker) -> Item:
    item_mock = mock.MagicMock()
    item_mock.nodeid = faker.word()
    item_mock.feature_info = None
    return cast(Item, item_mock)


@pytest.fixture()
def test_scenario_name(faker: Faker) -> str:
    return cast(str, faker.word())


@pytest.fixture()
def test_pytest_bdd_scenario(test_scenario_name: str) -> Scenario:
    scenario = mock.create_autospec(Scenario)
    setattr(scenario, "feature", mock.create_autospec(Feature))
    setattr(
        scenario.feature,
        "filename",
        get_test_file_settings().features_dir / "feature_type_1" / "full_feature_example_en.feature",
    )
    setattr(scenario, "name", test_scenario_name)
    return scenario


@pytest.fixture()
def test_severity(request: FixtureRequest) -> allure.severity_level:
    if hasattr(request, "param"):
        return request.param
    raise NotImplementedError


@pytest.fixture()
def test_pytest_bdd_item(
    mocked_context: BaseFactoryContext,
    test_pytest_bdd_scenario: Scenario,
    test_severity: allure.severity_level | None,
    faker: Faker,
) -> Item:
    item = mock.create_autospec(Item)
    item.nodeid = faker.word()
    setattr(item, "_obj", mock.MagicMock())
    item._obj.__scenario__ = test_pytest_bdd_scenario
    if test_severity is not None:
        item.own_markers = [
            Mark(
                name=f"{mocked_context.compilation_settings.severity_keyword}{test_severity.value}",
                args=tuple(),
                kwargs={},
            )
        ]
    else:
        item.own_markers = []
    return item


@pytest.fixture()
def test_pytest_bdd_step(faker: Faker) -> Step:
    item = mock.MagicMock()
    item.keyword = faker.word()
    item._name = faker.word()
    return cast(Step, item)


@pytest.fixture()
def step_context_logs(request: FixtureRequest) -> bool:
    if hasattr(request, "param"):
        return cast(bool, request.param)
    raise NotImplementedError


@pytest.fixture()
def test_step_context_settings(step_context_logs: bool) -> OverhaveStepContextSettings:
    return OverhaveStepContextSettings(step_context_logs=step_context_logs)


@pytest.fixture()
def test_step_context_runner(test_step_context_settings: OverhaveStepContextSettings) -> StepContextRunner:
    return StepContextRunner(test_step_context_settings)


@pytest.fixture()
def clear_get_step_context_runner() -> None:
    from overhave.pytest_plugin import get_step_context_runner

    get_step_context_runner.cache_clear()


@pytest.fixture()
def test_pytest_function() -> Function:
    return mock.create_autospec(Function)


@pytest.fixture()
def test_blocks_delimiter(faker: Faker) -> str:
    return cast(str, faker.word())


@pytest.fixture()
def test_description_manager_settings(
    test_blocks_delimiter: str, enable_html: bool
) -> OverhaveDescriptionManagerSettings:
    return OverhaveDescriptionManagerSettings(blocks_delimiter=test_blocks_delimiter, html=enable_html)


@pytest.fixture()
def test_description_manager(
    test_description_manager_settings: OverhaveDescriptionManagerSettings,
) -> DescriptionManager:
    return DescriptionManager(settings=test_description_manager_settings)


@pytest.fixture()
def description_handler_mock(enable_html: bool) -> mock.MagicMock:
    if enable_html:
        with mock.patch("allure.dynamic.description_html", return_value=mock.MagicMock()) as mocked_description_handler:
            yield mocked_description_handler
            return
    with mock.patch("allure.dynamic.description", return_value=mock.MagicMock()) as mocked_description_handler:
        yield mocked_description_handler


@pytest.fixture()
def link_handler_mock() -> mock.MagicMock:
    with mock.patch("allure.dynamic.link", return_value=mock.MagicMock()) as mocked_link_handler:
        yield mocked_link_handler


@pytest.fixture()
def clear_get_description_manager() -> None:
    from overhave.pytest_plugin import get_description_manager

    get_description_manager.cache_clear()


@pytest.fixture()
def terminal_writer_mock() -> mock.MagicMock:
    with mock.patch("_pytest.config.create_terminal_writer", return_value=mock.MagicMock()) as terminal_writer:
        yield terminal_writer


@pytest.fixture()
def test_prepared_config(terminal_writer_mock: mock.MagicMock) -> Config:
    config = Config(PytestPluginManager())
    test_pytest_parser = Parser(
        usage="%(prog)s [options] [file_or_dir] [file_or_dir] [...]", processopt=config._processopt
    )
    config._parser = test_pytest_parser
    return config


@pytest.fixture()
def getoption_mapping(request: FixtureRequest) -> Mapping[str, Any]:
    if hasattr(request, "param"):
        return cast(Mapping[str, Any], request.param)
    return {}


@pytest.fixture()
def getoption_mock(getoption_mapping: Mapping[str, Any], test_prepared_config: Config) -> ConfigGetOptionMock:
    getoption_mock = ConfigGetOptionMock(getoption_mapping)
    with mock.patch.object(test_prepared_config, "getoption", new=getoption_mock.getoption):
        yield getoption_mock


@pytest.fixture()
def test_pytest_clean_session(test_clean_item: Item) -> Session:
    session = mock.create_autospec(Session)
    setattr(session, "items", [test_clean_item])
    return session


@pytest.fixture()
def test_pytest_bdd_session(test_clean_item: Item, test_pytest_bdd_item: Item, test_prepared_config: Config) -> Session:
    session = mock.create_autospec(Session)
    setattr(session, "items", [test_clean_item, test_pytest_bdd_item])
    setattr(session, "config", test_prepared_config)
    return session


@pytest.fixture()
def severity_prefix(mocked_context: BaseFactoryContext, request: FixtureRequest) -> str:
    if hasattr(request, "param"):
        return cast(str, request.param)
    return mocked_context.compilation_settings.severity_prefix


@pytest.fixture()
def admin_url(request: FixtureRequest) -> httpx.URL | None:
    if hasattr(request, "param"):
        return cast(httpx.URL | None, request.param)
    return None


@pytest.fixture()
def patched_hook_test_execution_factory(
    mocked_context: OverhaveTestExecutionContext,
    clean_test_execution_factory: Callable[[], ITestExecutionFactory],
    severity_prefix: str,
    admin_url: httpx.URL | None,
    test_project_settings: OverhaveProjectSettings,
) -> ITestExecutionFactory:
    factory = clean_test_execution_factory()
    factory.set_context(mocked_context)
    factory.context.project_settings = test_project_settings
    factory._feature_extractor = get_test_feature_extractor()
    factory.context.compilation_settings.severity_prefix = severity_prefix
    factory.context.admin_link_settings.admin_url = admin_url
    return factory


@pytest.fixture()
def patched_hook_admin_proxy_manager(
    clean_proxy_manager: Callable[[], IProxyManager], patched_admin_factory
) -> IProxyManager:
    proxy_manager = clean_proxy_manager()
    proxy_manager.set_factory(patched_admin_factory)
    return proxy_manager


@pytest.fixture()
def patched_hook_test_execution_proxy_manager(
    clean_proxy_manager: Callable[[], IProxyManager],
    patched_hook_test_execution_factory: ITestExecutionFactory,
) -> IProxyManager:
    proxy_manager = clean_proxy_manager()
    proxy_manager.set_factory(patched_hook_test_execution_factory)
    return proxy_manager


@pytest.fixture()
def severity_handler_mock() -> mock.MagicMock:
    with mock.patch("allure.dynamic.severity", return_value=mock.MagicMock()) as mocked_severity_handler:
        yield mocked_severity_handler


@pytest.fixture(scope="module")
def tag_controller() -> OverhaveTagController:
    return OverhaveTagController()
