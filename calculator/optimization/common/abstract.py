from abc import ABC, abstractmethod
from typing import Type
from copy import deepcopy
from calculator.dtos import AbstractVariantDto
from calculator.validations import AbstractVariantValidation


class AbstractOptimizer(ABC):
    _validator: Type[AbstractVariantValidation]
    __MORE: str = '>'
    __LESS: str = '<'

    def __init_subclass__(cls, validator: Type[AbstractVariantValidation] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if not validator or not issubclass(validator, AbstractVariantValidation):
            raise TypeError(f"Validator must be subclass of AbstractVariantValidation, {type(validator)} provided")
        cls._validator = validator

    @classmethod
    def __set_limits(cls, _type: str, limits: list[int | float]):
        return [(_type, i) for i in limits]

    @classmethod
    def _set_more(cls, limits: list[int | float]):
        return cls.__set_limits(cls.__MORE, limits)

    @classmethod
    def _set_less(cls, limits: list[int | float]):
        return cls.__set_limits(cls.__LESS, limits)

    def __init__(self, dto: AbstractVariantDto):
        self._validator.validate(dto)
        self._dto = dto

    @property
    def func_coeffs(self):
        """func var coefficients"""
        return self._dto.costs * self._dto.station_amount

    @property
    def ineq_lims(self):
        """TODO DEV-PRIOR: update in variant 16
        inequalities' limits
        order: time, amount"""
        return self._set_less(self._dto.time_funds) + self._set_more(self._dto.minimums)

    @property
    def ineq_coeffs(self):
        """TODO DEV-PRIOR: update in variant 16
        inequalities' coefficients
        order: time, amount"""
        return self._dto.time_costs + [
            [1 if i == j else 0 for i, product in enumerate(self._dto.products)] * self._dto.station_amount
            for j in range(self._dto.product_amount)
        ]

    @property
    def canonical_with_basis(self) -> list[list[float | int]]:
        """TODO DEV-PRIOR: update in variant 16"""
        return [
            [k * (1 if ineq == self.__LESS else -1) for k in self.ineq_coeffs[j]] +
            [1 if i == j else 0 for i in range(len(self.ineq_lims))] +
            [lim * (1 if ineq == self.__LESS else -1)]
            for j, (ineq, lim) in enumerate(self.ineq_lims)
        ]

    @property
    def __base_offset(self) -> int:
        return len(self.func_coeffs)

    @property
    def canonical(self) -> list[list[float | int]]:
        return (self.canonical_with_basis +
                [self.func_coeffs + [0] * (len(self.canonical_with_basis[0]) - self.__base_offset)])

    @property
    def __basis_length(self) -> int:
        return len(self.ineq_lims)

    @classmethod
    def check_basis(cls, matrix: list[list[float | int]]):
        basises = [i[-1] for i in matrix[:-1]]
        _min = min(basises)
        index = basises.index(_min)
        without_basis = matrix[index][:-1]
        swap_index = len(without_basis) - without_basis[::-1].index(min(without_basis)) - 1
        return (_min < 0, matrix[index].index(1), swap_index, index) if _min < 0 else (_min < 0, None, None, None)

    @property
    def first_basis(self):
        return self.check_basis(self.canonical)

    @property
    def solid_basis(self):
        matrix = self.canonical
        matrix2 = self.canonical
        swap_check, basis_i, swap_i, ineq_i = self.first_basis
        while swap_check is True:
            div = matrix[ineq_i][swap_i]
            ineq_i_items = matrix2[ineq_i]
            for i, items in enumerate(matrix2):
                items = matrix[i]
                mult2 = items[swap_i]
                for j, item in enumerate(items):
                    mult1 = ineq_i_items[j]
                    matrix[i][j] = (item / div) if ineq_i == i else (item - (mult1 * mult2) / div)
                    matrix[i][j] = round(matrix[i][j], 2)
                    # print(f'{item} - ({mult1} * {mult2}) / {div} | {item} / {div} | {matrix[i][j]}')
                # print()
            matrix2 = deepcopy(matrix)
            swap_check, basis_i, swap_i, ineq_i = self.check_basis(matrix)
        return matrix

    def calculate(self):
        """TODO DEV-PRIOR
               p - products
               s - stations
               the objective function: sum(*[x[i] * p[i].cost for i in range(len(p))]) -> max
               f(x0, x1, x2, x3, x4) = x0 * 0.1 + x1 * 0.2 + x2 * 0.3 + x3 * 0.4 + x4 * 0.5
               limitations:
               - x[i] >= p[i].min, for i in range(len(p))
               - for j in range(len(s)):
                 - sum(*[x[i] * s[j].time_costs[i] for i in range(len(p))]) <= s[j].time_fund
               sensitivity on: p.cost

           """
        print(self.func_coeffs)
        print(self.ineq_coeffs)
        print(self.ineq_lims)
        print()
        for row in self.canonical:
            print(row)
        print()
        # print(self.first_basis)
        # print()
        for row in self.solid_basis:
            print(row)
        print()
        print()
        #
        # matrix, plan = self.solid_basis
        # matrix[-1][-1] = 0
        # for i, item in enumerate(matrix[-1]):
        #     matrix[-1][i] = -item
        # checks = [i <= 0 for i in plan.values()]
        # if True in checks:
        #     sorted_basic = [v for k, v in sorted(plan.items(), key=lambda x: x[0])] + [0] * self.__base_offset
        #     return None, sorted_basic
        #
        # raise NotImplementedError("Simplex method")
