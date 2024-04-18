from .abstract import AbstractValidation
from calculator.dtos import ProductDto


class ProductValidation(AbstractValidation):
    @classmethod
    def _check_for_err(cls, value: ProductDto, **kwargs):
        cls._for += f' #{value.id}'
        if not isinstance(value, ProductDto):
            cls._add_warning(cls._for, 'DTO is not a ProductDto instance')
        if not isinstance(value.min, int):
            raise cls._exceptions.err(f'Min value must be an integer: {value.min}')
        elif value.min < 0:
            raise cls._exceptions.err(f'Min value must be a positive number: {value.min}')
        if not isinstance(value.cost, float | int):
            raise cls._exceptions.err(f'Cost value must be a float: {value.cost}')
        elif value.cost < 0:
            raise cls._exceptions.err(f'Cost value must be a positive number: {value.cost}')

    @classmethod
    def validate(cls, value: ProductDto, **kwargs):
        return super().validate(value, True, **kwargs)
