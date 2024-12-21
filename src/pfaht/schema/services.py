from pydantic import BaseModel, computed_field, ConfigDict, Field
from typing import TypeVar, Generic, List
from . import api

T = TypeVar("T")


class ServiceResponse(BaseModel, Generic[T]):
    """Service Response Class"""

    data: T | None = None
    db: any = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ServiceResponseList(BaseModel, Generic[T]):
    """Paged Service Response Class"""

    data: List[T] = Field(default_factory=list)
    db: any = None
    page_options: api.PageOptions | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
