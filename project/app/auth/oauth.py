from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from app.config import get_settings


# Set up oauth
config_data = {
    "GOOGLE_CLIENT_ID": get_settings().google_client_id,
    "GOOGLE_CLIENT_SECRET": get_settings().google_client_secret,
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
