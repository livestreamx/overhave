import pytest
from faker import Faker
from httpx import HTTPStatusError

from overhave import db
from overhave.storage import TagModel
from overhave.transport.http.api_client.client import OverhaveApiClient


@pytest.mark.parametrize("test_user_role", [db.Role.user], indirect=True)
class TestFeatureTagsApiClient:
    """Integration tests for Overhave Tags API Client."""

    def test_get_feature_tags_item(
        self,
        overhave_api_client: OverhaveApiClient,
        test_tag: TagModel,
    ) -> None:
        item = overhave_api_client.get_feature_tags_item(value=test_tag.value)
        assert item.model_dump() == test_tag.model_dump()

    def test_get_feature_tags_with_unknown_value(
        self,
        overhave_api_client: OverhaveApiClient,
        faker: Faker,
    ) -> None:
        with pytest.raises(HTTPStatusError):
            overhave_api_client.get_feature_tags_item(value=faker.word())

    def test_get_feature_tags_list(
        self,
        overhave_api_client: OverhaveApiClient,
        test_tag: TagModel,
    ) -> None:
        items = overhave_api_client.get_feature_tags_list(value=test_tag.value)
        assert len(items) >= 1
        assert items[0].model_dump() == test_tag.model_dump()

    def test_get_feature_tags_list_with_unknown_value(
        self,
        overhave_api_client: OverhaveApiClient,
        faker: Faker,
    ) -> None:
        items = overhave_api_client.get_feature_tags_list(value=faker.word())
        assert len(items) == 0
