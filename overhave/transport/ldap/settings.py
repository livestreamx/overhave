from datetime import timedelta

from pydantic_settings import BaseSettings


class OverhaveLdapClientSettings(BaseSettings):
    """Settings for Overhave LDAP client."""

    url: str  # for example: "ldap://mydomain.ru"
    domain: str  # for example: "domain\\"
    dn: str  # for example: "dc=example,dc=com"
    timeout: timedelta = timedelta(seconds=10)
    tls_enabled: bool = True

    class Config:
        env_prefix = "OVERHAVE_LDAP_"
