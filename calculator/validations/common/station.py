from .abstract import AbstractValidation
from calculator.dtos import StationDto, TimeCostsDto


class TimeCostsValidation(AbstractValidation, _for="Time Cost"):
    @classmethod
    def _check_for_err(cls, value: TimeCostsDto, station_id: int = None, **kwargs):
        if not station_id:
            raise cls._exceptions.fatal('Station ID must be provided')
        if not isinstance(value, TimeCostsDto):
            cls._add_warning(cls._for, 'DTO must be an instance of TimeCostsDto')
        cls._for += f' #{station_id}'
        for i, time_cost in value.dict.items():
            _for = f'{cls._for}-{i}'
            if not isinstance(time_cost, float | int):
                raise cls._exceptions.err(f'Must be a float: {time_cost}')
            elif time_cost < 0:
                raise cls._exceptions.err(f'Must be a positive number: {time_cost}')

    @classmethod
    def validate(cls, value: TimeCostsDto, station_id: int = None, **kwargs):
        """Only raw validation due to the only use-case is in StationValidation"""
        return super().validate(value, True, station_id=station_id, **kwargs)


class StationValidation(AbstractValidation):
    @classmethod
    def _check_for_err(cls, value: StationDto, **kwargs):
        if not isinstance(value, StationDto):
            cls._add_warning(cls._for, 'DTO must be an instance of StationDto')
        TimeCostsValidation.validate(value.time_costs, value.id)
        if not isinstance(value.time_fund, float | int):
            raise cls._exceptions.err(f'Time fund must be a float: {value.time_fund}')
        elif value.time_fund < 0:
            raise cls._exceptions.err(f'Time fund must be a positive number: {value.time_fund}')

    @classmethod
    def validate(cls, value: StationDto, **kwargs):
        return super().validate(value, True, **kwargs)
