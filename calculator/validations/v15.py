from .common import AbstractVariantValidation
from calculator.dtos import Variant15Dto


class Variant15Validation(AbstractVariantValidation):
    @classmethod
    def validate(cls, value: Variant15Dto, _raw=False, **kwargs):
        return super().validate(value, _raw, **kwargs)
