from unittest import TestCase
from unittest.mock import MagicMock, patch

from overhave.publication.gitlab.tokenizer import TokenizerClient
from overhave.publication.gitlab.tokenizer.client import (
    InvalidRemoteKeyNameException,
    InvalidUrlException,
    TokenizerResponse,
)
from overhave.publication.gitlab.tokenizer.settings import TokenizerClientSettings


class TestTokenizerClient(TestCase):
    def setUp(self):
        self.settings = TokenizerClientSettings(
            url="http://example.com", initiator="test", remote_key="key", remote_key_name="remote_key"
        )
        self.client = TokenizerClient(self.settings)

    @patch("overhave.transport.http.base_client.BaseHttpClient._make_request")
    @patch("overhave.transport.http.base_client.BaseHttpClient._parse_or_raise")
    def test_get_token_success(self, mock_parse_or_raise: MagicMock, mock_make_request: MagicMock):
        token_response = TokenizerResponse(token="token")
        mock_parse_or_raise.return_value = token_response
        draft_id = 1
        response = self.client.get_token(draft_id)
        self.assertEqual(response, token_response)

    def test_get_token_invalid_url(self):
        self.client._settings.url = None
        with self.assertRaises(InvalidUrlException):
            self.client.get_token(1)

    def test_get_token_invalid_remote_key_name(self):
        self.client._settings.remote_key_name = None
        with self.assertRaises(InvalidRemoteKeyNameException):
            self.client.get_token(1)
