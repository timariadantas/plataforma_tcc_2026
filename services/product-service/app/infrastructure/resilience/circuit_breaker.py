import time


from infrastructure.errors.service_errors import (
    DatabaseUnavailableError
)

class CircuitBreaker:

    def __init__(
        self,
        failure_threshold=3,
        recovery_timeout=30,
        failure_exceptions=(Exception,)
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_exceptions = failure_exceptions

        self.failure_count = 0
        self.last_failure_time = None

        self.state = "CLOSED"

    def call(self, function, *args, **kwargs):

        if self.state == "OPEN":

            if self._should_try_recovery():
                self.state = "HALF_OPEN"

            else:
                raise DatabaseUnavailableError("Database circuit breaker is open")
        try:

            result = function(*args, **kwargs)

            self._on_success()

            return result

        except self.failure_exceptions:

            self._on_failure()

            raise

        except Exception:

            # Erros que não pertencem à infraestrutura
            # não alteram o estado do circuito.
            raise

    def _on_success(self):

        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def _on_failure(self):

        self.failure_count += 1
        self.last_failure_time = time.monotonic()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def _should_try_recovery(self):

        if self.last_failure_time is None:
            return False

        elapsed = (
            time.monotonic()
            - self.last_failure_time
        )

        return elapsed >= self.recovery_timeout