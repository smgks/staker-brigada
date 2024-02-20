
from fastapi import HTTPException


class UniqueConstraintException(HTTPException):
    def __init__(self):
        super().__init__(400, "Violates Unique constraint")

class ItemNotFound(HTTPException):
    def __init__(self):
        super().__init__(404, "Item not found")

