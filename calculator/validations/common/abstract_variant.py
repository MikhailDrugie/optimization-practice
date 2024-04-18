from typing import Type
from .abstract import AbstractValidation
from .product import ProductValidation
from .station import StationValidation
from calculator.dtos import AbstractVariantDto


class AbstractVariantValidation(AbstractValidation, abstract=True):
    @classmethod
    def _check_for_err(cls, value: AbstractVariantDto, **kwargs) -> None:
        if not isinstance(value, AbstractVariantDto):
            cls._add_warning(cls._for, 'DTO is not an AbstractVariantDto instance')
        if len(value.products) < value.product_amount:
            raise cls._exceptions.err(f"Couldn't find and load {value.product_amount - len(value.products)} "
                                      f"products to DTO")
        if len(value.stations) < value.station_amount:
            raise cls._exceptions.err(f"Couldn't find and load {value.station_amount - len(value.stations)} "
                                      f"stations to DTO")
        for product in value.products:
            ProductValidation.validate(product, **kwargs.get('product', {}))
        for station in value.stations:
            StationValidation.validate(station, **kwargs.get('station', {}))

    @classmethod
    def validate(cls, value: AbstractVariantDto, _raw=False, **kwargs):
        return super().validate(value, _raw, **kwargs)
