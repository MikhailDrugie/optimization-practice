class ValidationError(Exception):
    def __init__(self, message: str, _for: str = None):
        message = message if not _for else f'`{_for}` — {message}'
        super().__init__(message)
        self._for = _for

    @property
    def subj(self):
        return self._for
