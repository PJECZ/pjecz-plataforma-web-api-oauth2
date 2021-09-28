"""
FastAPI Pagination
"""
from typing import TypeVar, Generic
from fastapi import Query
from fastapi_pagination.limit_offset import LimitOffsetPage as BasePage, LimitOffsetParams as BaseParams

T = TypeVar("T")


class LimitOffsetParams(BaseParams):
    """Ajuste para que por defecto sean 500 resultados y 1000 como maximo"""

    limit: int = Query(500, ge=1, le=1000, description="Page size limit")
    offset: int = Query(0, ge=0, description="Page offset")


class LimitOffsetPage(BasePage[T], Generic[T]):
    """Tomar nuevos valores por defecto"""

    __params_type__ = LimitOffsetParams
