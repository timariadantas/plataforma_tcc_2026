namespace SalesService.Domain.Exceptions;

public abstract class BaseException : Exception
{
    public string Code {get;}
    protected BaseException(string message, string code) : base(message){
        Code = code;
    }
}

// Base de todas 