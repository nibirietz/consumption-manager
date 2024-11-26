from datetime import datetime
from pydantic.dataclasses import dataclass
from typing import Optional


@dataclass
class Income:
    name: str
    date: datetime


@dataclass
class Purchase:
    name: str
    cost: float
    date: datetime
