import logging
from pathlib import Path

from overhave.entities.feature.abstract import IFeatureExtractor
from overhave.entities.feature.errors import FeatureTypeExtractionError, ScenariosTestFileNotFound
from overhave.entities.settings import OverhaveFileSettings
from overhave.storage import FeatureTypeName

logger = logging.getLogger(__name__)


class FeatureExtractor(IFeatureExtractor):
    """Class for specified project's feature types resolution."""

    def __init__(self, file_settings: OverhaveFileSettings):
        self._file_settings = file_settings

        self._feature_types: list[FeatureTypeName] = []
        self._feature_type_to_dir_mapping: dict[FeatureTypeName, Path] = {}
        try:
            self._extract_project_data()
            self._check_pytest_bdd_scenarios_test_files()
        except FeatureTypeExtractionError:
            logger.exception("Extraction error while trying to collect features!")

    def _extract_project_data(self) -> None:
        try:
            feature_type_dirs = tuple(
                d
                for d in self._file_settings.features_dir.iterdir()
                if all(
                    (
                        d.is_dir(),
                        d != self._file_settings.tmp_dir,
                        not d.name.startswith("."),
                        not d.name.startswith("_"),
                    )
                )
            )
        except FileNotFoundError as err:
            raise FeatureTypeExtractionError(
                f"Could not find any subdirectory in specified features directory '{self._file_settings.features_dir}'!"
            ) from err
        self._feature_types = [FeatureTypeName(t.name) for t in feature_type_dirs]
        logger.info("Registered feature types: %s", self._feature_types)
        self._feature_type_to_dir_mapping = {FeatureTypeName(t.name): t for t in feature_type_dirs}

    def _check_pytest_bdd_scenarios_test_files(self) -> None:
        for feature_type in self._feature_types:
            scenarios_file = self._file_settings.fixtures_dir / self._file_settings.fixtures_file_template_mask.format(
                feature_type=feature_type
            )
            if scenarios_file.exists():
                continue
            raise ScenariosTestFileNotFound(
                "Could not find pytest-bdd test file with scenarios definition! "
                f"Maybe you don't created '{scenarios_file.name}' in '{scenarios_file.parent}' directory?"
            )

    @property
    def feature_types(self) -> list[FeatureTypeName]:
        return self._feature_types

    @property
    def feature_type_to_dir_mapping(self) -> dict[FeatureTypeName, Path]:
        return self._feature_type_to_dir_mapping
