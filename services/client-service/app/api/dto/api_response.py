from datetime import datetime, timezone
from typing import Generic, TypeVar

T = TypeVar("T")


class ApiResponse(Generic[T]):
    def __init__(
        self,
        message: str,
        elapsed: int,
        data: T | None = None,
        error: str | None = None
    ):
        self.message = message
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.elapsed = elapsed
        self.data = data
        self.error = error

    def to_dict(self):
        response = {
            "message": self.message,
            "timestamp": self.timestamp,
            "elapsed": self.elapsed
        }

        if self.data is not None:
            response["data"] = self.data

        if self.error is not None:
            response["error"] = self.error

        return response
    