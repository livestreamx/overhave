# flake8: noqa

from typing import Callable

import pytest
from pydantic import ValidationError

from overhave.publication.gitlab import TokenizerClientSettings
from overhave.publication.gitlab.tokenizer.client import (
    InvalidRemoteKeyNameException,
    InvalidUrlException,
    TokenizerClient,
    TokenizerRequestParamsModel,
)


class TestTokenizerClient:
    """Tests for :class:TokenizerClient."""

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

    @pytest.mark.parametrize(
        ("enabled", "url", "initiator", "remote_key", "remote_key_name"), [(False, None, "Overhave", "a", None)]
    )
    def test_tokenizer_client_validation_raises_error_when_url_is_none(
        self, enabled: bool, url: str, initiator: str, remote_key: str, remote_key_name: str
    ) -> None:
        settings = TokenizerClientSettings(
            enabled=enabled, url=url, initiator=initiator, remote_key=remote_key, remote_key_name=remote_key_name
        )
        with pytest.raises(InvalidUrlException):
            TokenizerClient(settings=settings).get_token(1)

    @pytest.mark.parametrize(
        ("enabled", "url", "initiator", "remote_key", "remote_key_name"), [(False, "edu.ru", "Overhave", "abaca", None)]
    )
    def test_tokenizer_client_validation_raises_error_when_remote_key_name_is_none(
        self, enabled: bool, url: str, initiator: str, remote_key: str, remote_key_name: str
    ) -> None:
        settings = TokenizerClientSettings(
            enabled=enabled, url=url, initiator=initiator, remote_key=remote_key, remote_key_name=remote_key_name
        )
        with pytest.raises(InvalidRemoteKeyNameException):
            TokenizerClient(settings=settings).get_token(1)

    @pytest.mark.parametrize(("initiator", "id", "remote_key", "remote_key_name"), [("Danil", 59, "Overhave", "abaca")])
    def test_tokenizer_req_params_sets_fields_correct(
        self, initiator: str, id: int, remote_key: str, remote_key_name: str
    ) -> None:
        model = TokenizerRequestParamsModel(initiator=initiator, id=id, remote_key=remote_key)

        assert model.initiator == initiator
        assert model.id == id
        assert model.remote_key == remote_key

    @pytest.mark.parametrize(("initiator", "id", "remote_key", "remote_key_name"), [("Danil", 59, "Overhave", "abaca")])
    def test_tokenizer_req_get_request_works_correct(
        self, initiator: str, id: int, remote_key: str, remote_key_name: str
    ) -> None:
        model = TokenizerRequestParamsModel(initiator=initiator, id=id, remote_key=remote_key)

        req_params = model.get_request_params(remote_key_name=remote_key_name)
        assert req_params is not None
        assert req_params["initiator"] == initiator
        assert req_params["id"] == id
        assert req_params[remote_key_name] == remote_key
