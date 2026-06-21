from pydantic_core.core_schema import is_instance_schema

from src.services.auth import AuthService


def test_decode_and_encode_access_token():
    data = {'user_id': 1}
    jwt_token = AuthService().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    pyload = AuthService().decode_token(jwt_token)
    assert pyload
    assert pyload['user_id'] == data['user_id']