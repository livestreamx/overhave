from typing import Callable

import pytest
from pydantic import ValidationError

from overhave.publication import TokenizerClient
from overhave.publication.gitlab import TokenizerClientSettings
from overhave.publication.gitlab.tokenizer.client import InvalidUrlException, \
    InvalidRemoteKeyNameException


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

    @pytest.mark.parametrize(("url", "initiator", "remote_key", "remote_key_name"),
                             [(None, "lol", "pepe", "angry-pepe")])
    def test_tokenizer_client_get_token_invalid_url(
            self, test_tokenizer_client_settings_disabled_factory: Callable[[], TokenizerClientSettings]
    ) -> None:
        settings = test_tokenizer_client_settings_disabled_factory()

        client = TokenizerClient(settings)

        with pytest.raises(InvalidUrlException):
            client.get_token(777)

    @pytest.mark.parametrize(("url", "initiator", "remote_key", "remote_key_name"),
                             [("https://lol.ru", "pepe", "peka", None)])
    def test_tokenizer_client_get_token_invalid_remote_key_name(
            self, test_tokenizer_client_settings_disabled_factory: Callable[[], TokenizerClientSettings]
    ) -> None:
        settings = test_tokenizer_client_settings_disabled_factory()

        client = TokenizerClient(settings)

        with pytest.raises(InvalidRemoteKeyNameException):
            client.get_token(777)
