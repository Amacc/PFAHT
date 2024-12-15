"""
API Schema
==========

This module contains the schema for the API responses.
"""
# need generic and type
from typing import Generic, TypeVar

from pydantic import BaseModel

from . import index

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """
    API Response Class

    This class is used to return a consistent response interface to the user.
    So that when we return a response from the api we can also add arbitrary
    data, such as links, messages, etc.
    """
    response: T | None = None
    """Reponse returned to the user"""

    message: str | None = None
    """Message to return to the user"""

    links: list[index.Link] = []
    """List of links to return to the user"""
