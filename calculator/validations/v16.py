from .common import AbstractVariantValidation
from calculator.dtos import Variant16Dto


class Variant16Validation(AbstractVariantValidation):
    @classmethod
    def _check_for_err(cls, value: Variant16Dto, **kwargs):
        super()._check_for_err(value, **kwargs)
        if not isinstance(value.minimal_profit, float | int):
            raise cls._exceptions.err(f'Minimal profit must be a float: {value.minimal_profit}')
        elif value.minimal_profit < 0:
            raise cls._exceptions.err(f'Minimal profit must be a positive number: {value.minimal_profit}')

    @classmethod
    def validate(cls, value: Variant16Dto, raw=False, **kwargs):
        return super().validate(value, raw, **kwargs)
