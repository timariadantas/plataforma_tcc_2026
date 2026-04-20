namespace SalesService.Domain.Exceptions;

public class ValidationException : BaseException
{
    public ValidationException(string message) : base(message, "VALIDATION_ERROR")
    {
    }
}