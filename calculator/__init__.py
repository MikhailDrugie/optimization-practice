from typing import Type
from .dtos import AbstractVariantDto, Variant15Dto
from .optimization import AbstractOptimizer, Variant15Optimizer


def get_dto(variant: int) -> Type[AbstractVariantDto]:
    return {
        15: Variant15Dto
    }.get(variant)


def get_optimizer(variant: int) -> Type[AbstractOptimizer]:
    return {
        15: Variant15Optimizer
    }.get(variant)
