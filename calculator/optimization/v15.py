from .common import AbstractOptimizer
from calculator.dtos import Variant15Dto
from calculator.validations import Variant15Validation


class Variant15Optimizer(AbstractOptimizer, validator=Variant15Validation):
    def __init__(self, dto: Variant15Dto):
        super().__init__(dto)

    def calculate(self):
        """TODO DEV-PRIOR"""
        print(self._dto)
