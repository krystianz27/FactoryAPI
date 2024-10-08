from dotenv import load_dotenv

from .fixtures import client, db_session  # noqa: F401
from .utils.pytest_utils import pytest_collection_modifyitems  # noqa: F401

load_dotenv()
