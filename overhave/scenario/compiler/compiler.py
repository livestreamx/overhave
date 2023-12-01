from typing import Sequence

import allure
from pytest_bdd import types as default_types

from overhave.entities import OverhaveLanguageSettings
from overhave.scenario.compiler.settings import OverhaveScenarioCompilerSettings
from overhave.scenario.prefix_mixin import PrefixMixin
from overhave.storage import TagModel, TestExecutorContext


def generate_task_info(tasks: list[str], header: str | None) -> str:
    if tasks and header is not None:
        return f"{header}: {', '.join(tasks)}"
    return ""


def _join_all_tags(lines: Sequence[str]) -> str:
    return " ".join(lines).replace("  ", " ")


class ScenarioCompilerError(Exception):
    """Base exception for :class:`ScenarioCompiler` errors."""


class IncorrectScenarioTextError(ScenarioCompilerError):
    """Exception for incorrect scenario text format."""


class ScenarioCompiler(PrefixMixin):
    """Class for scenario compilation from text view into pytest_bdd feature format."""

    def __init__(
        self,
        compilation_settings: OverhaveScenarioCompilerSettings,
        language_settings: OverhaveLanguageSettings,
        tasks_keyword: str | None,
    ):
        self._compilation_settings = compilation_settings
        self._language_settings = language_settings
        self._tasks_keyword = tasks_keyword

    def _get_feature_type_tag(self, scenario_text: str, tag: str) -> str:
        if f"{self._compilation_settings.tag_prefix}{tag}" in scenario_text:
            return ""
        return f"{self._compilation_settings.tag_prefix}{tag}"

    def _get_additional_tags(self, scenario_text: str, tags: list[TagModel]) -> str:
        tags_with_prefix = (f"{self._compilation_settings.tag_prefix}{tag.value}" for tag in tags)
        return f"{' '.join(tag for tag in tags_with_prefix if tag not in scenario_text)}"

    def _get_severity_tag(self, severity: allure.severity_level) -> str:
        return f"{self._compilation_settings.severity_prefix}{severity.value}"

    def _get_feature_prefix_if_specified(self, scenario_text: str) -> str | None:
        keywords: list[str] = [default_types.FEATURE]
        if self._language_settings.step_prefixes is not None:
            keywords.append(self._language_settings.step_prefixes.FEATURE)

        for key in keywords:
            if self._as_prefix(key) not in scenario_text:
                continue
            return key
        return None

    def _detect_feature_prefix_by_scenario_format(self, scenario_text: str) -> str:
        if (
            self._as_prefix(default_types.SCENARIO) in scenario_text
            or self._as_prefix(default_types.SCENARIO_OUTLINE) in scenario_text
        ):
            return default_types.FEATURE
        step_prefixes = self._language_settings.step_prefixes
        if step_prefixes is not None and (
            self._as_prefix(step_prefixes.SCENARIO) in scenario_text
            or self._as_prefix(step_prefixes.SCENARIO_OUTLINE) in scenario_text
        ):
            return step_prefixes.FEATURE
        raise IncorrectScenarioTextError(
            "Could not find any scenario prefix in scenario text, so could not compile feature header!"
        )

    def _compile_header(self, context: TestExecutorContext) -> str:
        text = context.scenario.text
        feature_prefix = self._get_feature_prefix_if_specified(scenario_text=text)
        if not feature_prefix:
            feature_prefix = self._detect_feature_prefix_by_scenario_format(scenario_text=text)
        blocks_delimiter = f" {self._compilation_settings.blocks_delimiter} "
        if context.test_run.start is None:
            raise RuntimeError
        joined_tags = _join_all_tags(
            (
                self._get_feature_type_tag(scenario_text=text, tag=context.feature.feature_type.name),
                self._get_additional_tags(scenario_text=text, tags=context.feature.feature_tags),
                self._get_severity_tag(severity=context.feature.severity),
            )
        )
        return "\n".join(
            (
                joined_tags,
                f"{self._as_prefix(feature_prefix)} {context.feature.name}",
                f"{self._compilation_settings.id_prefix} {context.feature.id}",
                (
                    f"{self._compilation_settings.created_by_prefix} {context.feature.author}"
                    f"{blocks_delimiter}"
                    f"{self._compilation_settings.last_edited_by_prefix} {context.feature.last_edited_by}"
                    f"{self._compilation_settings.time_delimiter} "
                    f"{context.feature.last_edited_at.strftime(self._compilation_settings.time_format)}"
                    f"{blocks_delimiter}"
                    f"{self._compilation_settings.published_by_prefix} {context.test_run.executed_by}"
                ),
                generate_task_info(tasks=context.feature.task, header=self._tasks_keyword),
                "",
            )
        )

    def compile(self, context: TestExecutorContext) -> str:
        return self._compile_header(context=context) + "\n" + context.scenario.text.strip("\n") + "\n"
