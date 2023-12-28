from pydantic import SecretStr

from overhave import OverhaveApiAuthenticator, OverhaveApiAuthenticatorSettings
from overhave.storage import AuthStorage
from overhave.transport.http.api_client.client import *


if __name__ == '__main__':
    auth = OverhaveApiAuthenticator(OverhaveApiAuthenticatorSettings(url='http://localhost:8000'), AuthStorage())
    token = auth.get_bearer_auth('admin', SecretStr('86f2551dd8cb4dc18308916a5a7edc6a'))
    settings = OverhaveApiClientSettings(url='http://localhost:8000', auth_token=token.token)
    client = OverhaveApiClient(settings=settings)
    print(client.get_features_by_tag_id(3))
    print(client.get_features_by_tag_value('chatbot'))
