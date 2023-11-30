from http import HTTPStatus
from pathlib import Path

from fastapi.testclient import TestClient

from overhave.api.deps import get_admin_files_dir


class TestExtraAPI:
    """Integration tests for Overhave Extra API."""

    def test_get_favicon(self, test_api_client: TestClient) -> None:
        response = test_api_client.get("/favicon.ico")

        assert response.status_code == HTTPStatus.OK
        assert response.read() == \
               Path(get_admin_files_dir() / "favicon.ico").read_bytes()
