# мы очень стараемся исправить


# import pytest
# from unittest.mock import MagicMock
#
# from overhave.publication import TokenizerClient
# from overhave.publication.gitlab.tokenizer.client import TokenizerResponse, TokenizerRequestParamsModel
# from overhave.publication.gitlab.tokenizer.settings import TokenizerClientSettings
# from overhave.transport.http.base_client import HttpMethod
#
#
# @pytest.fixture
# def mock_base_http_client():
#     return MagicMock()
#
#
# @pytest.mark.usefixtures("database")
# class TestTokenizerClient:
#     """Tests for TokenizerClient class."""
#
#     @pytest.mark.parametrize("draft_id", [1, 2, 3])
#     def test_get_token(
#             self,
#             mock_base_http_client: MagicMock,
#             draft_id: int
#     ) -> None:
#         settings = TokenizerClientSettings()
#         client = TokenizerClient(settings)
#         mock_base_http_client.return_value = TokenizerResponse(token="test_token")
#         response = client.get_token(draft_id)
#         assert response.token == "test_token"
#         mock_base_http_client.assert_called_once_with(
#             HttpMethod.POST,
#             settings.url,
#             params=TokenizerRequestParamsModel(
#                 initiator=settings.initiator,
#                 id=draft_id,
#                 remote_key=settings.remote_key
#             ).get_request_params(settings.remote_key_name)
#         )
