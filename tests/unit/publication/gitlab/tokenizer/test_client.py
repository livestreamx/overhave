from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError

from overhave.publication.gitlab.tokenizer import TokenizerClient
from overhave.publication.gitlab.tokenizer.client import InvalidUrlException


class TestTokenizerClient:
    """Tests for :class:`TokenizerClient`."""

    @pytest.mark.parametrize(("initiator", "remote_key", "remote_key_name", "url"),
                             [("peka", "pepe", "sad-pepe", "https://ya.ru")])
    def test_tokenizer_client_get_token_works(
            self, test_tokenizer_client_factory
    ) -> None:
        client = test_tokenizer_client_factory()
        with patch.object(TokenizerClient, '_make_request', return_value=MagicMock()) as make_request:
            with patch.object(TokenizerClient, '_parse_or_raise', return_value=MagicMock()) as _parse_or_raise:
                client.get_token(4)
                make_request.assert_called_once()
                _parse_or_raise.assert_called_once()
        assert client

    @pytest.mark.parametrize(("initiator", "remote_key", "remote_key_name", "url"),
                             [("peka", "pepe", "sad-pepe", None)])
    def test_tokenizer_client_get_token_url_validation_raises_error(
            self, test_tokenizer_client_factory
    ) -> None:
        with pytest.raises(InvalidUrlException):
            test_tokenizer_client_factory().get_token(4)

    @pytest.mark.parametrize(
        ("initiator", "remote_key", "remote_key_name", "url"),
        [("kek", None, "peka", "https://ya.ru"), (None, "lol", "peka", "https://ya.ru"),
         (None, None, "pepe", "https://ya.ru")],
    )
    def test_tokenizer_settings_validation_raises_error(
            self, test_tokenizer_client_factory
    ) -> None:
        with pytest.raises(ValidationError):
            test_tokenizer_client_factory()
