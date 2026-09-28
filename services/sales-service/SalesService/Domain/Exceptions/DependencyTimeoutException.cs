namespace SalesService.Domain.Exceptions;

public class DependencyTimeoutException : BaseException
{
    public DependencyTimeoutException(string message)
        : base(message, "DEPENDENCY_TIMEOUT")
    {
    }
}