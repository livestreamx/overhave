import json
import logging
from typing import cast

from overhave.transport.http import BaseHttpClient, BearerAuth
from overhave.transport.http.api_client.models import (
    ApiEmulationRunResponse,
    ApiFeatureResponse,
    ApiFeatureTypeResponse,
    ApiTagResponse,
    ApiTestRunResponse,
    ApiTestUserResponse,
)
from overhave.transport.http.api_client.settings import OverhaveApiClientSettings
from overhave.transport.http.base_client import HttpMethod

logger = logging.getLogger(__name__)


class OverhaveApiClient(BaseHttpClient[OverhaveApiClientSettings]):
    """Client for overhave api."""

    def __init__(self, settings: OverhaveApiClientSettings):
        super().__init__(settings=settings)

    def get_feature_tags_item(self, value: str) -> ApiTagResponse:
        logger.debug("Start get feature tags item with [value: %s]", value)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_feature_tags_item_url,
            params={"value": value},
            auth=BearerAuth(self._settings.auth_token),
        )

        logger.debug("Get tags item successfully")

        return cast("ApiTagResponse", self._parse_or_raise(response, ApiTagResponse))

    def get_feature_tags_list(self, value: str) -> list[ApiTagResponse]:
        logger.debug("Start get feature tags list with [value: %s]", value)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_feature_tags_list_url,
            params={"value": value},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get tags list successfully")

        return [ApiTagResponse.model_validate(data) for data in response.json()]

    def get_feature_types(self) -> list[ApiFeatureTypeResponse]:
        logger.debug("Start get feature types list")
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_feature_types_list_url,
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get feature types successfully")

        return [ApiFeatureTypeResponse.model_validate(data) for data in response.json()]

    def get_features_by_tag_id(self, tag_id: int) -> list[ApiFeatureResponse]:
        logger.debug("Start get feature with [tag_id: %s]", tag_id)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_feature_url,
            params={"tag_id": tag_id},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get feature successfully")

        return [ApiFeatureResponse.model_validate(data) for data in response.json()]

    def get_features_by_tag_value(self, tag_value: str) -> list[ApiFeatureResponse]:
        logger.debug("Start get feature with [tag_value: %s]", tag_value)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_feature_url,
            params={"tag_value": tag_value},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get feature successfully")

        return [ApiFeatureResponse.model_validate(data) for data in response.json()]

    def get_test_run(self, test_run_id: int) -> ApiTestRunResponse:
        logger.debug("Start get test run with [test_run_id: %s]", test_run_id)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_test_run_url,
            params={"test_run_id": test_run_id},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get test run successfully")

        return cast("ApiTestRunResponse", self._parse_or_raise(response, ApiTestRunResponse))

    def create_test_run(self, tag_value: str) -> list[str]:
        logger.debug("Start create test run with [tag_value: %s]", tag_value)
        response = self._make_request(
            method=HttpMethod.POST,
            url=self._settings.get_test_run_create_url,
            params={"tag_value": tag_value},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Create test run successfully")

        return cast(list[str], response.json())

    def get_emulation_runs(self, test_user_id: int) -> list[ApiEmulationRunResponse]:
        logger.debug("Start get list of EmulationRun")
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_emulation_run_list_url,
            params={"test_user_id": test_user_id},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get list of EmulationRun successfully")
        return [ApiEmulationRunResponse.model_validate(data) for data in response.json()]

    def get_test_user_by_user_id(self, user_id: int) -> ApiTestUserResponse:
        logger.debug("Start get test user by user_id: %s", user_id)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_test_user_url,
            params={"user_id": user_id},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get test user by user_id successfully")
        return cast("ApiTestUserResponse", self._parse_or_raise(response, ApiTestUserResponse))

    def get_test_user_by_user_key(self, user_key: str) -> ApiTestUserResponse:
        logger.debug("Start get test user by user_key: %s", user_key)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_test_user_url,
            params={"user_key": user_key},
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get test user by user_key successfully")
        return ApiTestUserResponse.model_validate(response.json())

    def get_test_users(self, feature_type: str, allow_update: bool) -> list[ApiTestUserResponse]:
        logger.debug("Start get test users with feature_type: %s and allow_update: %s", feature_type, allow_update)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_test_user_list_url,
            params={
                "feature_type": feature_type,
                "allow_update": allow_update,
            },
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get tests users successfully")
        return [ApiTestUserResponse.model_validate(data) for data in response.json()]

    def delete_test_user(self, user_id: int) -> None:
        logger.debug("Start delete user by user_id: %s", user_id)
        self._make_request(
            method=HttpMethod.DELETE,
            url=self._settings.get_test_user_id_url(user_id),
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Delete test user successfully")

    def get_test_user_specification(self, user_id: int) -> dict[str, str | None]:
        logger.debug("Start get user specification by user_id: %s", user_id)
        response = self._make_request(
            method=HttpMethod.GET,
            url=self._settings.get_test_user_id_spec_url(user_id),
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Get user specification successfully")
        return cast(dict[str, str | None], response.json())

    def update_test_user_specification(self, user_id: int, specification: dict[str, str | None]) -> None:
        logger.debug("Start update user specification by user_id: %s", user_id)
        self._make_request(
            method=HttpMethod.PUT,
            url=self._settings.get_test_user_id_spec_url(user_id),
            data=json.dumps(specification),
            auth=BearerAuth(self._settings.auth_token),
        )
        logger.debug("Update user specification successfully")
