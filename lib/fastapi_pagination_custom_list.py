"""
FastAPI Pagination Custom List
"""
from typing import Generic, List, Sequence, TypeVar

from fastapi import Query
from fastapi_pagination.bases import AbstractPage, AbstractParams
from fastapi_pagination.default import Params as BaseParams
from pydantic.generics import GenericModel

T = TypeVar("T")


class ListParams(BaseParams):
    """Modificar size por defecto"""

    size: int = Query(100, ge=1, le=10000, description="Page size")


class ListResult(GenericModel, Generic[T]):
    """Resultado que contiene items, total y size"""

    total: int
    items: List[T]
    size: int


class CustomList(AbstractPage[T], Generic[T]):
    """Lista personalizada con success y message"""

    success: bool = True
    message: str = "Success"
    result: ListResult[T]

    __params_type__ = ListParams

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: AbstractParams):
        """Create"""

        if not isinstance(params, cls.__params_type__):
            raise TypeError(f"Params must be {cls.__params_type__}")

        return cls(
            result=ListResult(
                total=total,
                items=items,
                size=params.size,
            )
        )


def custom_list_success_false(error: Exception) -> CustomList:
    """Crear lista personalizada sin items, con success en falso y message con el error"""

    result = ListResult(total=0, items=[], size=0)
    return CustomList(success=False, message=str(error), result=result)
