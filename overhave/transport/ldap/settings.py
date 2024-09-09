from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class OverhaveLdapClientSettings(BaseSettings):
    """Settings for Overhave LDAP client."""

    model_config = SettingsConfigDict(env_prefix="OVERHAVE_LDAP_")

    url: str  # for example: "ldap://mydomain.ru"
    domain: str  # for example: "domain\\"
    dn: str  # for example: "dc=example,dc=com"
    timeout: timedelta = timedelta(seconds=10)
    tls_enabled: bool = True
