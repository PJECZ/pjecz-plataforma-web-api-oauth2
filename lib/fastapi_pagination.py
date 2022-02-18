"""
FastAPI Pagination
"""
from typing import TypeVar, Generic
from fastapi import Query
from fastapi_pagination.limit_offset import LimitOffsetPage as BasePage, LimitOffsetParams as BaseParams

T = TypeVar("T")


class LimitOffsetParams(BaseParams):
    """Ajuste para que por defecto sean 50 resultados y 2000 como maximo"""

    limit: int = Query(50, ge=1, le=2000, description="Page size limit")
    offset: int = Query(0, ge=0, description="Page offset")


class LimitOffsetPage(BasePage[T], Generic[T]):
    """Tomar nuevos valores por defecto"""

    __params_type__ = LimitOffsetParams
