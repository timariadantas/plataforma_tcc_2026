namespace CurrencyService.Domain.Exceptions;

public class CurrencyServiceUnavailableException : Exception
{
    public CurrencyServiceUnavailableException(string message)
        : base(message)
    {
    }

    public CurrencyServiceUnavailableException(
        string message,
        Exception innerException)
        : base(message, innerException)
    {
    }
}