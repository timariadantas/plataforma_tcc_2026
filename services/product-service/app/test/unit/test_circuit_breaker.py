import pytest

from infrastructure.resilience.circuit_breaker import CircuitBreaker
from infrastructure.errors.service_errors import (
    DatabaseUnavailableError,
    ProductNotFoundError
)

def test_circuit_opens_after_failure_threshold():

    breaker = CircuitBreaker(
        failure_threshold=3,
        failure_exceptions=(DatabaseUnavailableError,)
    )

    def failure():
        raise DatabaseUnavailableError(
            "Database unavailable"
        )

    for _ in range(3):

        with pytest.raises(DatabaseUnavailableError):
            breaker.call(failure)

    assert breaker.state == "OPEN"
    assert breaker.failure_count == 3
    
def test_open_circuit_blocks_call():

    breaker = CircuitBreaker(
        failure_threshold=1,
        failure_exceptions=(DatabaseUnavailableError,)
    )

    def failure():
        raise DatabaseUnavailableError(
            "Database unavailable"
        )

    with pytest.raises(DatabaseUnavailableError):
        breaker.call(failure)

    assert breaker.state == "OPEN"

    with pytest.raises(DatabaseUnavailableError):
        breaker.call(failure)

def test_success_closes_circuit():

    breaker = CircuitBreaker(
        failure_threshold=1,
        recovery_timeout=0,
        failure_exceptions=(DatabaseUnavailableError,)
    )

    def failure():
        raise DatabaseUnavailableError(
            "Database unavailable"
        )

    def success():
        return "ok"

    with pytest.raises(DatabaseUnavailableError):
        breaker.call(failure)

    assert breaker.state == "OPEN"

    result = breaker.call(success)

    assert result == "ok"
    assert breaker.state == "CLOSED"
    assert breaker.failure_count == 0
    
def test_business_error_does_not_open_circuit():

    breaker = CircuitBreaker(
        failure_threshold=3,
        failure_exceptions=(DatabaseUnavailableError,)
    )

    def business_error():
        raise ProductNotFoundError(
            "Product not found"
        )

    for _ in range(5):

        with pytest.raises(ProductNotFoundError):
            breaker.call(business_error)

    assert breaker.state == "CLOSED"
    assert breaker.failure_count == 0