from .common import AbstractVariantDto


class Variant16Dto(AbstractVariantDto):
    def __init__(self, data):
        super().__init__(data)
        self.minimal_profit = data.get('minimal-profit')
