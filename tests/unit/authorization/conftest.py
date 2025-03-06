from typing import Iterator
from unittest import mock

import pytest
import ldap3

from overhave.transport import LDAPAuthenticator, OverhaveLdapClientSettings


@pytest.fixture(scope="module")
def envs_for_mock() -> dict[str, str | None]:
    return {
        "OVERHAVE_LDAP_URL": "ldap://mydomain.ru",
        "OVERHAVE_LDAP_DOMAIN": "domain\\",
        "OVERHAVE_LDAP_DN": "dc=example,dc=ru",
    }


@pytest.fixture(scope="module")
def mock_default_value() -> str:
    return "http://dummy"


@pytest.fixture()
def test_ldap_client_settings(mock_envs) -> OverhaveLdapClientSettings:
    return OverhaveLdapClientSettings()


TEST_LDAP_GROUPS = ["group1", "group2"]


@pytest.fixture()
def mocked_ldap_connection() -> ldap3.Connection:
    member_groups = [
        f"CN={TEST_LDAP_GROUPS[0]},OU=dep1,OU=Security Groups,DC=mydomain,DC=ru",
        f"CN={TEST_LDAP_GROUPS[1]},OU=dep2,OU=Security Groups,DC=mydomain,DC=ru",
    ]

    connection = mock.MagicMock(spec=ldap3.Connection)
    connection.search.return_value = True
    connection.result = {"result": 0}
    connection.response = [
        {
            "attributes": {"memberOf": member_groups}
        }
    ]
    return connection


@pytest.fixture()
def test_ldap_authenticator(
        test_ldap_client_settings: OverhaveLdapClientSettings, mocked_ldap_connection: ldap3.Connection
) -> Iterator[LDAPAuthenticator]:
    with mock.patch("ldap3.Connection", return_value=mocked_ldap_connection):
        yield LDAPAuthenticator(settings=test_ldap_client_settings)
