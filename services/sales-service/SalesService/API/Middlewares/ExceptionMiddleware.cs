using System.Net;
using System.Text.Json;
using SalesService.Domain.Exceptions;

namespace SalesService.API.Middlewares;

public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;
    
    public ExceptionMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task Invoke (HttpContext context)
    {
        try
        {
            await _next (context);
        }
        catch(Exception ex)
        {
            await HandleException(context, ex);
        }
    }
    private static Task HandleException(HttpContext context, Exception ex)
    {
        var statusCode = HttpStatusCode.InternalServerError;

        switch (ex)
        {
            case NotFoundException:
                statusCode = HttpStatusCode.NotFound;
                break;
            case ValidationException:
                statusCode = HttpStatusCode.BadRequest;
                break;
            case BusinessException:
                statusCode = HttpStatusCode.UnprocessableEntity;
                break;
            case ConflictException:
                statusCode = HttpStatusCode.Conflict;
                break;

            case UnauthorizedException:
                statusCode = HttpStatusCode.Unauthorized;
                break;
        }
        var response = new
        {
            sucess = false,
            error = ex.Message
        };

        var json = JsonSerializer.Serialize(response);

        context.Response.ContentType = "application/json";
        context.Response.StatusCode = (int)statusCode;

        return context.Response.WriteAsync(json);
    }



    }



