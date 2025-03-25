import pytest
from typing import List

from storage import ProductView

from main import app


class StorageMock:
    def __init__(self, dictionary: dict) -> None:
        for k, v in dictionary.items():
            setattr(self, k, v)
