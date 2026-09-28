namespace SalesService.Domain.Exceptions;

public class DependencyUnavailableException : Exception
{
    public DependencyUnavailableException(string message)
        : base(message)
    {
    }
}