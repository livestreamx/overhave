from typing import Callable

import gitlab
import pytest

from overhave.transport.http.gitlab_client import TokenType
from overhave.transport.http.gitlab_client.utils import InvalidTokenTypeError


class TestGitlabPythonClient:
    """Unit tests for gitlab-python utils."""

    @pytest.mark.parametrize(("token_type", "token"), [("gotcha", "peka")])
    def test_get_gitlab_python_client_raises_error(
        self,
        test_gitlab_python_client_factory: Callable[[], gitlab.Gitlab]
    ) -> None:
        with pytest.raises(InvalidTokenTypeError):
            test_gitlab_python_client_factory()

    @pytest.mark.parametrize(("token_type", "token"),
                             [(TokenType.OAUTH, "oauth_token")])
    def test_get_gitlab_python_client_raises_error(
            self,
            test_gitlab_python_client_factory_valid: gitlab.Gitlab
    ) -> None:
        client = test_gitlab_python_client_factory_valid
        assert client.url == "http://example.com"
        assert client.oauth_token == "oauth_token"
