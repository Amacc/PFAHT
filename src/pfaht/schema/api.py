"""
API Schema
==========

This module contains the schema for the API responses.
"""

# need generic and type
from typing import Generic, TypeVar, List
from urllib.parse import urlencode

from pydantic import BaseModel, Field

from . import index

T = TypeVar("T")


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

    links: dict[str, index.Link] = Field(default_factory=dict)
    """List of links to return to the user"""


class PageOptions(BaseModel):
    """Page Options

    This class is used to specify the options for a paginated response.
    """

    page: int = 1
    """Page number to return"""

    per_page: int = 100
    """Number of items per page"""

    @property
    def offset(self):
        """Calculate the offset for the query"""
        return (self.page - 1) * self.per_page


class PagedApiResponse(BaseModel, Generic[T]):
    """Paged API Response

    This class is used to return a paginated response to the user.
    """

    response: List[T] = []
    """List of items returned to the user. Default is empty"""

    message: str | None = None
    """Message to return to the user. Default is None"""

    links: dict[str, index.Link] = Field(default_factory=dict)
    """List of links to return to the user. Default is empty"""

    page_options: PageOptions = PageOptions()
    """Page options for the response"""

    def next_page_fragment(
        self,
    ):
        """Adds next page link to the response links list.

        >>> response = PagedApiResponse()
        >>> response.next_page_fragment()
        'page=2&per_page=100'
        """
        return urlencode(
            {"page": self.page_options.page + 1, "per_page": self.page_options.per_page}
        )

    def prior_page_fragment(
        self,
    ):
        """Adds prior page link to the response links list.

        >>> response = PagedApiResponse()
        >>> response.prior_page_fragment()
        'page=0&per_page=100'
        """
        return urlencode(
            {"page": self.page_options.page - 1, "per_page": self.page_options.per_page}
        )
