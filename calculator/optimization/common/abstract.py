from abc import ABC, abstractmethod
from typing import Type
from calculator.dtos import AbstractVariantDto
from calculator.validations import AbstractVariantValidation


class AbstractOptimizer(ABC):
    _validator: Type[AbstractVariantValidation]

    def __init_subclass__(cls, validator: Type[AbstractVariantValidation] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if not validator or not issubclass(validator, AbstractVariantValidation):
            raise TypeError(f"Validator must be subclass of AbstractVariantValidation, {type(validator)} provided")
        cls._validator = validator

    def __init__(self, dto: AbstractVariantDto):
        self._validator.validate(dto)
        self._dto = dto

    @abstractmethod
    def calculate(self):
        pass
