import logging
import re

import ldap
from ldap.ldapobject import LDAPObject
from pydantic import SecretStr

from overhave.transport.ldap.settings import OverhaveLdapClientSettings

logger = logging.getLogger(__name__)


class LDAPAuthenticator:
    """Class-client for LDAP authentication."""

    def __init__(self, settings: OverhaveLdapClientSettings) -> None:
        self._settings = settings
        self._ldap_connection: LDAPObject | None = None

    def _connect(self, login: str, password: SecretStr) -> None:
        ldap_connection = ldap.initialize(self._settings.url)
        ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
        ldap_connection.set_option(ldap.OPT_NETWORK_TIMEOUT, self._settings.timeout.seconds)
        if self._settings.tls_enabled:
            ldap_connection.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_REQUIRE_CERT)
            ldap_connection.start_tls_s()
        ldap_connection.simple_bind_s(f"{self._settings.domain}{login}", password.get_secret_value())
        self._ldap_connection = ldap_connection

    def _ask_ad_usergroups(self, login: str) -> list[str]:
        result = self._ldap_connection.search_st(  # type: ignore
            base=self._settings.dn,
            scope=ldap.SCOPE_SUBTREE,
            filterstr=f"(sAMAccountName={login})",
            attrlist=["memberOf"],
            timeout=self._settings.timeout.seconds,
        )
        member_of = result[0][1]["memberOf"]
        member_of = [m.decode("utf8") for m in member_of]

        p = re.compile("CN=(.*?),", re.IGNORECASE)
        return [
            p.match(x).group(1)  # type: ignore
            for x in list(filter(lambda x: "OU=Security Groups" in x or "OU=Mail Groups" in x, member_of))
        ]

    def get_user_groups(self, login: str, password: SecretStr) -> list[str] | None:
        try:
            self._connect(login, password)
        except ldap.INVALID_CREDENTIALS:
            logger.info("Failed LDAP auth_managers for user: %s", login)
            return None

        return self._ask_ad_usergroups(login)
