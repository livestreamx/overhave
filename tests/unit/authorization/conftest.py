from typing import Any, Iterator
from unittest import mock

import pytest
from ldap.ldapobject import LDAPObject

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


def mocked_ldap_connection(*args: Any, **kwargs: Any) -> LDAPObject:
    member_groups = [
        bytes(f"CN={TEST_LDAP_GROUPS[0]},OU=dep1,OU=Security Groups,DC=mydomain,DC=ru", encoding="utf-8"),
        bytes(f"CN={TEST_LDAP_GROUPS[1]},OU=dep2,OU=Security Groups,DC=mydomain,DC=ru", encoding="utf-8"),
    ]
    ldap_connection = mock.MagicMock()
    ldap_connection.search_st.return_value = [
        (
            "CN=Very cool member,OU=dep1,DC=mydomain,DC=ru",
            {"memberOf": member_groups},
        )
    ]
    return ldap_connection


@pytest.fixture()
def test_ldap_authenticator(test_ldap_client_settings: OverhaveLdapClientSettings) -> Iterator[LDAPAuthenticator]:
    with mock.patch("overhave.transport.ldap.authenticator.ldap.initialize") as initialize:
        initialize.return_value = mocked_ldap_connection()
        yield LDAPAuthenticator(settings=test_ldap_client_settings)
