from typing import Callable
from unittest.mock import patch, MagicMock

import pytest
from pydantic import ValidationError

from overhave.publication import TokenizerClient
from overhave.publication.gitlab import TokenizerClientSettings
from overhave.publication.gitlab.tokenizer.client import InvalidRemoteKeyNameException, InvalidUrlException


class TestTokenizerClient:
    """Tests for :class:`TokenizerClient`."""

    @pytest.mark.parametrize(
        ("initiator", "remote_key", "remote_key_name"),
        [("kek", None, "peka"), (None, "lol", "peka"), (None, None, "pepe")],
    )
    def test_tokenizer_settings_validation_raises_error(
        self, test_tokenizer_client_settings_factory: Callable[[], TokenizerClientSettings]
    ) -> None:
        with pytest.raises(ValidationError):
            test_tokenizer_client_settings_factory()

    @pytest.mark.parametrize(("initiator", "remote_key", "remote_key_name"), [("peka", "pepe", "sad-pepe")])
    def test_tokenizer_settings_validation_not_raises_error(
        self, test_tokenizer_client_settings_factory: Callable[[], TokenizerClientSettings]
    ) -> None:
        test_tokenizer_client_settings_factory()

    @pytest.mark.parametrize(("url", "remote_key_name"), [(None, "pepega"), (None, None)])
    def test_tokenizer_client_get_token_raises_error_with_none_url(
            self, test_tokenizer_client: TokenizerClient
    ) -> None:
        with pytest.raises(InvalidUrlException):
            test_tokenizer_client.get_token(1)

    @pytest.mark.parametrize(("url", "remote_key_name"), [("http://kek.com", None)])
    def test_tokenizer_client_get_token_raises_error_with_none_remote_key_name(
            self, test_tokenizer_client: TokenizerClient
    ) -> None:
        with pytest.raises(InvalidRemoteKeyNameException):
            test_tokenizer_client.get_token(1)

    @pytest.mark.parametrize(("url", "remote_key_name"), [("https://kek.com", "lol")])
    def test_tokenizer_client_get_token_not_raises_error(
            self, test_tokenizer_client: TokenizerClient
    ) -> None:
        with patch.object(TokenizerClient, '_make_request', return_value=MagicMock()):
            with patch.object(TokenizerClient, '_parse_or_raise', return_value=MagicMock()):
                test_tokenizer_client.get_token(1)
