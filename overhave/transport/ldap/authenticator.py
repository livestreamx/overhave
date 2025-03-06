import logging
import re
import typing

import ldap3
from ldap3.core.exceptions import LDAPExceptionError
from pydantic import SecretStr

from overhave.transport.ldap.settings import OverhaveLdapClientSettings

logger = logging.getLogger(__name__)


class LdapUserSearchAttributes(typing.TypedDict):
    """LDAP user search attributes."""

    memberOf: list[str]  # noqa: N815


class LDAPAuthenticator:
    """Overhave LDAP client."""

    def __init__(self, settings: OverhaveLdapClientSettings) -> None:
        self._server = ldap3.Server(
            settings.url,
            use_ssl=True,
            connect_timeout=settings.timeout.seconds,
        )
        self._settings = settings

    def _get_connection(self, login: str, password: SecretStr) -> ldap3.Connection:
        return ldap3.Connection(
            self._server,
            user=f"{self._settings.domain}{login}",
            password=password.get_secret_value(),
            receive_timeout=self._settings.timeout.seconds,
            read_only=True,
            auto_referrals=False,
            auto_bind=True,
        )

    def _ask_ad_usergroups(self, connection: ldap3.Connection, login: str) -> list[str]:
        # Выполнение поискового запроса
        connection.search(
            search_base=self._settings.dn,
            search_filter=f"(sAMAccountName={login})",
            search_scope=ldap3.SUBTREE,
            attributes=["memberOf"],
            time_limit=self._settings.timeout.seconds,
        )
        if connection.result.get("result", 1) != 0:
            return []
        if connection.response is None:  # pragma: no cover
            # should not happen - result was 0
            raise ValueError

        members_of: list[LdapUserSearchAttributes] = [
            el["attributes"].get("memberOf", []) for el in connection.response if "attributes" in el
        ]

        if len(members_of) != 1:
            raise ValueError("Multiple or zero users with the same login")

        member_of = members_of[0]

        p = re.compile("CN=(.*?),", re.IGNORECASE)
        return [
            p.match(x).group(1)  # type: ignore[union-attr]
            for x in list(filter(lambda x: "OU=Security Groups" in x or "OU=Mail Groups" in x, member_of))
        ]

    def get_user_groups(self, login: str, password: SecretStr) -> list[str] | None:
        try:
            with self._get_connection(login, password) as conn:
                return self._ask_ad_usergroups(conn, login)
        except LDAPExceptionError:
            logger.debug("Failed LDAP authorization for user: %s", login)
        return None
