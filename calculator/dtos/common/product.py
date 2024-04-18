class ProductDto:
    def __init__(self, _id: int, data: dict):
        self.id = _id
        data = data if isinstance(data, dict) else {}
        self.min = data.get('min')
        self.cost = data.get('cost')
