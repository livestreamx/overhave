import allure
from markupsafe import Markup

from overhave.entities import OverhaveDescriptionManagerSettings


class DescriptionManager:
    """Class for test-suit custom description management and setting to Allure report."""

    def __init__(self, settings: OverhaveDescriptionManagerSettings):
        self._settings = settings
        self._description: list[str] = []

    def apply_description(self) -> None:
        if self._description:
            joined_description = self._settings.blocks_delimiter.join(self._description)
            if not self._settings.html:
                allure.dynamic.description(joined_description)
                return
            allure.dynamic.description_html(Markup(joined_description))

    def add_description(self, value: str) -> None:
        self._description.append(value)

    def add_description_above(self, value: str) -> None:
        self._description.insert(0, value)
