import logging
from os import chdir
from typing import Any, Callable, cast
from unittest import mock

import pytest
import werkzeug
from _pytest.fixtures import FixtureRequest
from faker import Faker
from flask import Flask

from demo.demo import _run_demo_admin
from demo.settings import OverhaveDemoAppLanguage, OverhaveDemoSettingsGenerator
from overhave import OverhaveDBSettings, db
from overhave.admin.views.feature import _SCENARIO_PREFIX, FeatureView
from overhave.factory import IAdminFactory, ISynchronizerFactory
from overhave.pytest_plugin import IProxyManager
from overhave.storage import FeatureModel, ScenarioModel, SystemUserModel, TestRunModel
from tests.db_utils import create_test_session
from tests.objects import PROJECT_WORKDIR, FeatureTestContainer

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def envs_for_mock(db_settings: OverhaveDBSettings) -> dict[str, str | None]:
    return {
        "OVERHAVE_DB_URL": db_settings.db_url,
        "OVERHAVE_WORK_DIR": PROJECT_WORKDIR.as_posix(),
    }


@pytest.fixture(scope="module")
def mock_default_value() -> str:
    return ""


@pytest.fixture()
def test_proxy_manager(clean_proxy_manager: Callable[[], IProxyManager]) -> IProxyManager:
    return clean_proxy_manager()


@pytest.fixture()
def test_system_user_login(request: FixtureRequest, faker: Faker) -> str:
    if hasattr(request, "param"):
        return cast(str, request.param)
    return faker.word()


@pytest.fixture()
def test_db_user(database: None, test_system_user_login: str) -> SystemUserModel:
    with create_test_session() as session:
        db_user = db.UserRole(login=test_system_user_login, password="test_password", role=db.Role.user)
        session.add(db_user)
        session.flush()
        return SystemUserModel.model_validate(db_user)


@pytest.fixture()
def test_db_feature(test_feature_container: FeatureTestContainer, test_db_user: SystemUserModel) -> FeatureModel:
    with create_test_session() as session:
        db_feature = session.query(db.Feature).filter(db.Feature.file_path == test_feature_container.file_path).one()
        return FeatureModel.model_validate(db_feature)


@pytest.fixture()
def test_db_scenario(test_db_feature: FeatureModel, test_db_user: SystemUserModel) -> ScenarioModel:
    with create_test_session() as session:
        db_scenario = session.query(db.Scenario).filter(db.Scenario.feature_id == test_db_feature.id).one()
        return ScenarioModel.model_validate(db_scenario)


@pytest.fixture()
def test_db_test_run(test_db_scenario: ScenarioModel) -> TestRunModel:
    with create_test_session() as session:
        db_test_run: db.TestRun | None = (  # noqa: ECE001
            session.query(db.TestRun)
            .filter(db.TestRun.scenario_id == test_db_scenario.id)
            .order_by(db.TestRun.id.desc())
            .first()
        )
        if db_test_run is None:
            raise RuntimeError("TestRun should not be None!")
        return TestRunModel.model_validate(db_test_run)


@pytest.fixture()
def flask_run_mock() -> mock.MagicMock:
    with mock.patch.object(Flask, "run", return_value=mock.MagicMock()) as flask_run_handler:
        yield flask_run_handler


@pytest.fixture(scope="module")
def test_feature_types() -> tuple[str, ...]:
    return "feature_type_1", "feature_type_2", "feature_type_3"


@pytest.fixture()
def test_admin_factory(clean_admin_factory: Callable[[], IAdminFactory]) -> IAdminFactory:
    return clean_admin_factory()


@pytest.fixture()
def test_synchronizer_factory(clean_synchronizer_factory: Callable[[], ISynchronizerFactory]) -> ISynchronizerFactory:
    return clean_synchronizer_factory()


@pytest.fixture()
def test_demo_language(request: FixtureRequest) -> str | None:
    if hasattr(request, "param"):
        return cast(OverhaveDemoAppLanguage, request.param)
    raise NotImplementedError


@pytest.fixture()
def test_demo_settings_generator(test_demo_language: OverhaveDemoAppLanguage) -> OverhaveDemoSettingsGenerator:
    logger.debug("Test demo language: %s", test_demo_language)
    return OverhaveDemoSettingsGenerator(
        admin_host="localhost", admin_port=8076, language=test_demo_language, threadpool=False
    )


@pytest.fixture(scope="module")
def mocked_git_repo() -> mock.MagicMock:
    with mock.patch("git.Repo", return_value=mock.MagicMock()) as git_repo:
        yield git_repo


@pytest.fixture()
def test_resolved_admin_proxy_manager(
    flask_run_mock: mock.MagicMock,
    mocked_git_repo: mock.MagicMock,
    test_synchronizer_factory: ISynchronizerFactory,
    test_admin_factory: IAdminFactory,
    test_proxy_manager: IProxyManager,
    mock_envs: None,
    database: None,
    test_demo_settings_generator: OverhaveDemoSettingsGenerator,
) -> IProxyManager:
    chdir(PROJECT_WORKDIR)
    with create_test_session():
        _run_demo_admin(settings_generator=test_demo_settings_generator)
    return test_proxy_manager


@pytest.fixture()
def flask_flash_handler_mock() -> mock.MagicMock:
    with mock.patch("flask.flash", return_value=mock.MagicMock()) as flask_run_handler:
        yield flask_run_handler


@pytest.fixture()
def flask_urlfor_handler_mock(test_db_scenario: ScenarioModel) -> mock.MagicMock:
    with mock.patch(
        "flask.url_for", return_value=f"/testrun/details/?id={test_db_scenario.id}"
    ) as flask_urlfor_handler:
        yield flask_urlfor_handler


@pytest.fixture(scope="module")
def test_rendered_featureview() -> mock.MagicMock:
    return mock.create_autospec(werkzeug.Response)


@pytest.fixture()
def redisproducer_addtask_mock(test_resolved_admin_proxy_manager: IProxyManager) -> mock.MagicMock:
    with mock.patch.object(
        test_resolved_admin_proxy_manager.factory.redis_producer, "add_task", return_value=mock.MagicMock()
    ) as mocked_redisproducer_addtask:
        yield mocked_redisproducer_addtask


@pytest.fixture()
def flask_currentuser_mock(test_db_user: SystemUserModel) -> mock.MagicMock:
    with mock.patch("overhave.admin.views.feature.current_user", return_value=mock.MagicMock()) as mocked:
        mocked.login = test_db_user.login
        yield mocked


@pytest.fixture()
def runtest_data(test_db_scenario: ScenarioModel, request: FixtureRequest) -> dict[str, Any]:
    if hasattr(request, "param"):
        return cast(dict[str, Any], request.param)
    # regular data
    return {
        f"{_SCENARIO_PREFIX}-id": test_db_scenario.id,
        f"{_SCENARIO_PREFIX}-text": test_db_scenario.text,
    }


@pytest.fixture()
def test_featureview_runtest_result(
    test_rendered_featureview: mock.MagicMock,
    test_resolved_admin_proxy_manager: IProxyManager,
    test_db_scenario: ScenarioModel,
    flask_flash_handler_mock: mock.MagicMock,
    flask_urlfor_handler_mock: mock.MagicMock,
    redisproducer_addtask_mock: mock.MagicMock,
    flask_currentuser_mock: mock.MagicMock,
    runtest_data: dict[str, Any],
) -> werkzeug.Response:
    with create_test_session():
        return FeatureView._run_test(data=runtest_data, rendered=test_rendered_featureview)
