"""
FastAPI Pagination Custom Page
"""
from typing import Generic, List, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.limit_offset import LimitOffsetParams as BaseLimitOffsetParams
from pydantic.generics import GenericModel

T = TypeVar("T")


class LimitOffsetParams(BaseLimitOffsetParams):
    """Modificar limit y offset por defecto"""

    limit: int = Query(10, ge=1, le=10000, description="Query limit")
    offset: int = Query(0, ge=0, description="Query offset")


class PageResult(GenericModel, Generic[T]):
    """Resultado que contiene items, total, limit y offset"""

    total: int
    items: List[T]
    limit: int
    offset: int


class CustomPage(AbstractPage[T], Generic[T]):
    """Pagina personalizada con success y message"""

    success: bool = True
    message: str = "Success"
    result: PageResult[T]

    __params_type__ = LimitOffsetParams

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: AbstractParams):
        """Create"""

        if not isinstance(params, cls.__params_type__):
            raise TypeError(f"Params must be {cls.__params_type__}")

        return cls(
            result=PageResult(
                total=total,
                items=items,
                limit=params.limit,
                offset=params.offset,
            )
        )


def custom_page_success_false(error: Exception) -> CustomPage:
    """Crear pagina personalizada sin items, con success en falso y message con el error"""

    result = PageResult(total=0, items=[], limit=0, offset=0)
    return CustomPage(success=False, message=str(error), result=result)
