from abc import ABC
from . import StationDto, ProductDto


class AbstractVariantDto(ABC):
    __product_amount: int
    __station_amount: int

    def __init_subclass__(cls, product_amount: int = 5, station_amount: int = 3, **kwargs):
        super().__init_subclass__(**kwargs)
        if not isinstance(product_amount, int) or product_amount < 1:
            raise ValueError(f"Product amount must be a natural number: {product_amount}")
        if not isinstance(station_amount, int) or station_amount < 1:
            raise ValueError(f"Station amount must be a natural number: {station_amount}")
        cls.__product_amount = product_amount
        cls.__station_amount = station_amount

    @classmethod
    @property
    def product_amount(cls):
        return cls.__product_amount

    @classmethod
    @property
    def station_amount(cls):
        return cls.__station_amount

    def __init__(self, data: dict):
        self.products = [
            ProductDto(i + 1, data.get(f'product-{i + 1}', {})) for i in range(self.__product_amount)
            if data.get(f'product-{i + 1}')
        ]
        self.stations = [
            StationDto(i + 1, data.get(f'station-{i + 1}', {}), self.products) for i in range(self.__station_amount)
            if data.get(f'station-{i + 1}')
        ]

    @property
    def product_dict(self) -> dict[int, ProductDto]:
        return {product.id: product for product in self.products}

    @property
    def station_dict(self) -> dict[int, StationDto]:
        return {station.id: station for station in self.stations}

    @property
    def costs(self) -> list[float]:
        return [product.cost for product in self.products]

    @property
    def minimums(self) -> list[int]:
        return [product.min for product in self.products]

    @property
    def time_funds(self) -> list[float]:
        return [station.time_fund for station in self.stations]

    def _time_costs(self, station_id: int) -> list[float]:
        return ((([0] * self.product_amount) * (station_id - 1)) +
                self.station_dict[station_id].time_costs.values +
                (([0] * self.product_amount) * (self.station_amount - station_id)))

    @property
    def time_costs(self):
        return [self._time_costs(station.id) for station in self.stations]

    def __str__(self):
        products_prompts = [
            f'  #{product.id}:\n'
            f'    Min Amount: {product.min}\n'
            f'    Cost: {product.cost}\n'
            for product in self.products
        ]
        stations_prompts = [
            f'  #{station.id}:\n'
            f'    Time Fund: {station.time_fund}\n'
            f'    Time Costs:\n'
            f'{str(station.time_costs)}\n'
            for station in self.stations
        ]
        return (f"Products: \n"
                f"{''.join(products_prompts)}"
                f"Stations: \n"
                f"{''.join(stations_prompts)}")
