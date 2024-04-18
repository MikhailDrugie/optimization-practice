from .common import AbstractVariantValidation
from calculator.dtos import Variant17Dto


class Variant17Validation(AbstractVariantValidation):
    @classmethod
    def validate(cls, value: Variant17Dto, _raw=False, **kwargs):
        return super().validate(value, _raw, **kwargs)
