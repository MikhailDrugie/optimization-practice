class ValidationExceptions:
    __ERR = ValueError
    __WARN = Warning
    __FATAL = Exception

    @classmethod
    @property
    def ERR(cls):
        return cls.__ERR

    @classmethod
    @property
    def WARN(cls):
        return cls.__WARN

    @classmethod
    @property
    def FATAL(cls):
        return cls.__FATAL

    @classmethod
    def err(cls, message: str):
        return cls.__ERR(message)

    @classmethod
    def warn(cls, message: str):
        return cls.__WARN(message)

    @classmethod
    def fatal(cls, message: str):
        return cls.__FATAL(message)
