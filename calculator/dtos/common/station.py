from .product import ProductDto


class TimeCostsDto:
    def __init__(self, data: dict, products: list[ProductDto]):
        self.dict = {}
        for product in products:
            if hasattr(product, 'id'):
                self.dict[product.id] = data.get(f'time-cost-{product.id}')

    def __getitem__(self, item: ProductDto):
        return self.dict.get(item.id)

    @property
    def values(self):
        return list(self.dict.values())

    def __str__(self):
        return '\n'.join([f'      ({i}) - {tc}' for i, tc in self.dict.items()])


class StationDto:
    def __init__(self, _id: int, data: dict, products: list[ProductDto]):
        self.id = _id
        data = data if isinstance(data, dict) else {}
        self.time_fund = data.get('time-fund')
        self.time_costs = TimeCostsDto(data, products)
