from unittest.mock import patch, MagicMock

import pytest

from overhave.publication.gitlab.tokenizer import TokenizerClient
from overhave.publication.gitlab.tokenizer.client import InvalidUrlException


class TestTokenizerClient:
    """Tests for :class:`TokenizerClient`."""

    @pytest.mark.parametrize('test_tokenizer_client',
                             [{"initiator": "peka", "remote_key": "pepe", "remote_key_name": "sad-pepe",
                               "url": "https://ya.ru"}], indirect=True)
    def test_tokenizer_client_get_token_works(
            self, test_tokenizer_client
    ) -> None:
        token_mock = "magic_token"
        draft_id_mock = 4

        client = test_tokenizer_client

        request_mock = MagicMock()
        request_mock.json = MagicMock(return_value={"token": token_mock})

        with patch.object(TokenizerClient, '_make_request', return_value=request_mock) as make_request:
            tokenizerClient = client.get_token(draft_id_mock)
            assert tokenizerClient.token == token_mock
            make_request.assert_called_once()

    @pytest.mark.parametrize('test_tokenizer_client',
                             [{"initiator": "peka", "remote_key": "pepe", "remote_key_name": "sad-pepe"}],
                             indirect=True)
    def test_tokenizer_client_get_token_url_validation_raises_error(
            self, test_tokenizer_client
    ) -> None:
        draft_id_mock = 4

        with pytest.raises(InvalidUrlException):
            test_tokenizer_client.get_token(draft_id_mock)
