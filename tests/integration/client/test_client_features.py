import allure
import pytest

from overhave import db
from overhave.storage import FeatureModel, TagModel
from overhave.transport.http.api_client.client import OverhaveApiClient


@pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
class TestFeatureApiClient:
    """Integration tests for Overhave FeatureTypes API Client."""

    @pytest.mark.parametrize("test_severity", [allure.severity_level.NORMAL], indirect=True)
    def test_get_feature_by_tag_id(
        self,
        api_client: OverhaveApiClient,
        test_tag: TagModel,
        test_feature_with_tag: FeatureModel,
    ) -> None:
        features = api_client.get_features_by_tag_id(tag_id=test_tag.id)
        assert len(features) == 1
        assert features[0].model_dump() == test_feature_with_tag.model_dump()

    @pytest.mark.parametrize("test_severity", [allure.severity_level.NORMAL], indirect=True)
    def test_get_feature_by_tag_value(
        self,
        api_client: OverhaveApiClient,
        test_tag: TagModel,
        test_feature_with_tag: FeatureModel,
    ) -> None:
        features = api_client.get_features_by_tag_value(tag_value=test_tag.value)
        assert len(features) == 1
        assert features[0].model_dump() == test_feature_with_tag.model_dump()
