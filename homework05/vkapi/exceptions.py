class APIError(Exception):
    def __init__(self, *args, **kwargs):
        if "message" in kwargs.keys():
            self.message = kwargs["message"]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"APIError {self.message}"
        else:
            return "APIError has been raised"
