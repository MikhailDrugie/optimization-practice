from abc import ABC, abstractmethod
import warnings
from ...utils.validation import ValidationError, ValidationExceptions


class AbstractValidation(ABC):
    _for: str = None
    _exceptions = ValidationExceptions
    _warnings: list[tuple[str, Warning]] = []

    def __init_subclass__(cls, _for: str = None, abstract: bool = False, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._for = _for or cls._for or (cls.__name__.replace('Validation', '') if not abstract else None)

    @classmethod
    @abstractmethod
    def _check_for_err(cls, value, **kwargs) -> None:
        pass

    @classmethod
    def _add_warning(cls, _for: str, message: str):
        cls._warnings.append((_for, cls._exceptions.warn(message)))

    @classmethod
    def __pop_warnings(cls):
        for _for, warning in cls._warnings:
            warnings.warn(f'`{_for}` — {str(warning)}' if _for else str(warning))
        cls._warnings = []

    @classmethod
    def validate(cls, value, _raw: bool = False, **kwargs) -> None:
        if _raw:
            cls._check_for_err(value, **kwargs)
            # for _for, warning in cls._warnings:
            #     warnings.warn(f'`{_for}` — {str(warning)}' if _for else str(warning))
        else:
            try:
                cls._check_for_err(value, **kwargs)
            except cls._exceptions.ERR as err:
                cls.__pop_warnings()
                raise ValidationError(str(err), cls._for)
            except cls._exceptions.WARN as warn:
                warnings.warn(f'`{cls._for}` — {str(warn)}' if cls._for else str(warn))
            except cls._exceptions.FATAL as fatal:
                cls.__pop_warnings()
                raise SystemError(str(fatal))
            finally:
                cls.__pop_warnings()
