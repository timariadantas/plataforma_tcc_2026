namespace SalesService.Domain.Exceptions;

public class BusinessException : BaseException
{
    public BusinessException(string message) : base(message, "BUSINESS_ERROR")
    {
    }
}