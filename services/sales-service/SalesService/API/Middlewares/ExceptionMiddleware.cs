using System.Net;
using System.Text.Json;
using SalesService.Domain.Exceptions;
using SalesService.Application.DTO.Response;
using System.Text.Json.Serialization;

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
        var startTime = DateTime.UtcNow;
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
            await HandleException(context, ex, startTime);
        }
    }
    private static async Task HandleException(HttpContext context, Exception ex , DateTime startTime)
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
                statusCode = HttpStatusCode.Conflict;
                break;
            case ConflictException:
                statusCode = HttpStatusCode.Conflict;
                break;

            case UnauthorizedException:
                statusCode = HttpStatusCode.Unauthorized;
                break;
            case DependencyTimeoutException:
                statusCode = HttpStatusCode.GatewayTimeout;
                break;
            case DependencyUnavailableException:
                statusCode = HttpStatusCode.ServiceUnavailable;
                break;
        }
       
        var elapsed = (long)(
            DateTime.UtcNow - startTime
        ).TotalMilliseconds;

         var response = new ApiResponse<object>
        {
            Message = "Request failed",
            Timestamp = DateTime.UtcNow,
            Elapsed = elapsed,
            Error = ex.Message
        };

        context.Response.StatusCode = (int)statusCode;
        context.Response.ContentType = "application/json";

        await context.Response.WriteAsJsonAsync(
            response,
            new JsonSerializerOptions
            {
                PropertyNamingPolicy = JsonNamingPolicy.CamelCase,

                DefaultIgnoreCondition =
                    JsonIgnoreCondition.WhenWritingNull
            }
        );
    }
}


