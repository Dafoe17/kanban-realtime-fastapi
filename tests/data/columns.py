from uuid import uuid4

from src.schemas import ColumnCreate

from .prefixes import COLUMN_PREFIX


def generate_test_column(column_prefix=COLUMN_PREFIX):
    return ColumnCreate(title=f"{column_prefix}_{uuid4().hex[:6]}")
