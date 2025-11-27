from enum import Enum

class SortOrder(str, Enum):
    asc = "ASC"
    desc = "DESC"

class UserRole(str, Enum):
    guest = "guest"
    user = "user"
    manager = "manager"
    admin = "admin"
