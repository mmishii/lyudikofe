from pydantic import AliasGenerator
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import alias_generators
from typing import Type, Generic, TypeVar


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=alias_generators.to_camel),
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class PaginationSchema(BaseModel):
    offset: int
    limit: int
   
T = TypeVar('T', bound=BaseModel)

class ResponsePaginationSchema(BaseSchema, Generic[T]):
    items: list[T] | T
    len_items: int
    left_limit: int | None
    left_offset: int | None
    right_limit: int | None
    right_offset: int | None
