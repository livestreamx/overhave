import pytest

from overhave import db
from overhave.storage import FeatureTypeModel
from overhave.transport.http.api_client.client import OverhaveApiClient


@pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
class TestFeatureTypesApiClient:
    """Integration tests for Overhave FeatureTypes API Client."""

    def test_get_feature_types(
        self, overhave_api_client: OverhaveApiClient, test_feature_type: FeatureTypeModel
    ) -> None:
        feature_types = overhave_api_client.get_feature_types()
        assert len(feature_types) == 1
        assert feature_types[0].model_dump() == test_feature_type.model_dump()
