class UnicornException(Exception):
    def __init__(self, error: str):
        self.error = error
