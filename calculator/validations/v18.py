from .common import AbstractVariantValidation
from calculator.dtos import Variant18Dto


class Variant18Validation(AbstractVariantValidation):
    @classmethod
    def validate(cls, value: Variant18Dto, _raw=False, **kwargs):
        return super().validate(value, _raw, **kwargs)
