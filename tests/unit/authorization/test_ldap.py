from pydantic import SecretStr
import ldap3
from overhave.transport import LDAPAuthenticator
from tests.unit.authorization.conftest import TEST_LDAP_GROUPS


class TestLdapAuthenticator:
    """Unit tests for :class:`LDAPAuthenticator`."""

    def test_get_user_groups(self, test_ldap_authenticator: LDAPAuthenticator) -> None:
        groups = test_ldap_authenticator.get_user_groups("kek", SecretStr("lol"))
        assert groups == TEST_LDAP_GROUPS, f"Expected {TEST_LDAP_GROUPS}, got {groups}"

    def test_connect(self, test_ldap_authenticator: LDAPAuthenticator) -> None:
        connection = test_ldap_authenticator._get_connection(login="kek", password=SecretStr("lol"))
        assert connection is not None
        assert isinstance(connection, ldap3.Connection)
