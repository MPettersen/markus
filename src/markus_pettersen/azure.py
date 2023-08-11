import os
import sys
import logging

from azure.keyvault.secrets import SecretClient

# Local imports
from src.markus_pettersen.general import check_env, password_generator


# Setup root logger
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=LOG_LEVEL,
)
LOG = logging.getLogger(__name__)


def initiate_key_vault(credential):
    global KEY_VAULT
    KEY_VAULT = SecretClient(vault_url="https://" + check_env("KEY_VAULT_NAME") + ".vault.azure.net", credential=credential)


def check_secret_exists(secret_name: str):
    try:
        KEY_VAULT.get_secret(secret_name).value
        return True
    except:
        return False


def upsert_secret(secret_name: str, value: str):
    KEY_VAULT.set_secret(secret_name, value)


def upsert_password(secret_name: str):
    if not check_secret_exists(secret_name):
        upsert_secret(secret_name, password_generator())
