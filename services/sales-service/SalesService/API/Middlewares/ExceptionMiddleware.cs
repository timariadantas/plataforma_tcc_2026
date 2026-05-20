using System.Net;
using System.Text.Json;
using SalesService.Domain.Exceptions;
using SalesService.Application.DTO.Response;

namespace SalesService.API.Middlewares;

public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionMiddleware> _logger;
    
    public ExceptionMiddleware(
        RequestDelegate next,
        ILogger<ExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task Invoke (HttpContext context)
    {
        try
        {
            await _next (context);
        }
        catch(Exception ex)
        {
            _logger.LogError(
                ex,
                "Unhandled exception: {Message}",
                ex.Message);
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
          var response = new ApiResponse<object>
        {
            Message = "Request failed",
            Elapsed = 0,
            Error = ex.Message,
            Data = null
        };

        var json = JsonSerializer.Serialize(response);

        context.Response.ContentType = "application/json";
        context.Response.StatusCode = (int)statusCode;

        return context.Response.WriteAsync(json);
    }



    }



