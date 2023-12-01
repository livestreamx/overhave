from logging import Logger
from unittest import mock

import pytest
from allure_commons._allure import StepContext
from faker import Faker

from overhave.pytest_plugin import StepContextNotDefinedError, StepContextRunner


@pytest.mark.parametrize("step_context_logs", [False, True], indirect=True)
class TestStepContextRunner:
    """Unit tests for StepContextRunner."""

    def test_set_title(self, test_step_context_runner: StepContextRunner, faker: Faker) -> None:
        test_step_context_runner.set_title(faker.word())
        assert isinstance(test_step_context_runner._step, StepContext)

    def test_start_failed_without_title(self, test_step_context_runner: StepContextRunner) -> None:
        with pytest.raises(StepContextNotDefinedError):
            test_step_context_runner.start()

    def test_start(self, step_context_logs: bool, test_step_context_runner: StepContextRunner, faker: Faker) -> None:
        test_step_context_runner.set_title(faker.word())
        test_step_context_runner.start()
        if step_context_logs:
            assert isinstance(test_step_context_runner._logger, Logger)
        else:
            assert isinstance(test_step_context_runner._logger, mock.MagicMock)

    @pytest.mark.parametrize("exception", [None, Exception])
    def test_stop_failed(self, test_step_context_runner: StepContextRunner, exception: BaseException | None) -> None:
        with pytest.raises(StepContextNotDefinedError):
            test_step_context_runner.stop(exception)

    @pytest.mark.parametrize("exception", [None, Exception])
    def test_stop(
        self, test_step_context_runner: StepContextRunner, faker: Faker, exception: BaseException | None
    ) -> None:
        test_step_context_runner.set_title(faker.word())
        test_step_context_runner.stop(exception)

    @pytest.mark.parametrize("exception", [None, Exception])
    def test_start_and_stop(
        self, test_step_context_runner: StepContextRunner, faker: Faker, exception: BaseException | None
    ) -> None:
        test_step_context_runner.set_title(faker.word())
        test_step_context_runner.start()
        test_step_context_runner.stop(exception)
