from pydantic import SecretStr

from overhave.transport import LDAPAuthenticator
from tests.unit.authorization.conftest import TEST_LDAP_GROUPS


class TestLdapAuthenticator:
    """Unit tests for :class:`LDAPAuthenticator`."""

    def test_get_user_groups(self, test_ldap_authenticator: LDAPAuthenticator) -> None:
        assert test_ldap_authenticator.get_user_groups("kek", SecretStr("lol")) == TEST_LDAP_GROUPS

    def test_connect(self, test_ldap_authenticator: LDAPAuthenticator) -> None:
        test_ldap_authenticator._get_connection(login="kek", password=SecretStr("lol"))
