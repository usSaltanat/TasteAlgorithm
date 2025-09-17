import typing

from flask import request, current_app

from storage import Storage
from storage_entities import Session


def get_session_from_cookies() -> Session | None:
    if "session_id" in request.cookies:
        storage = typing.cast(
            Storage, current_app.config["storage"]
        )  # подключение к БД
        return storage.find_session_by_uuid(request.cookies["session_id"])
    return None
