using System.Net;
using System.Text.Json;
using System.Text.Json.Serialization;
using CurrencyService.Domain.Exceptions;
using CurrencyService.Application.DTO.Response;

namespace CurrencyService.Infrastructure.Middleware;

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

    public async Task Invoke(HttpContext context)
    {
        var startTime = DateTime.UtcNow;

        try
        {
            await _next(context);
        }
        catch (CurrencyServiceUnavailableException ex)
        {
            _logger.LogError(
                ex,
                "Currency provider unavailable.");

            var elapsed =
                (long)(DateTime.UtcNow - startTime).TotalMilliseconds;

            context.Response.StatusCode =
                (int)HttpStatusCode.ServiceUnavailable;

            context.Response.ContentType =
                "application/json";

            var response = new ApiResponse<object>
            {
                Message = "Currency provider unavailable",
                Timestamp = DateTime.UtcNow,
                Elapsed = elapsed,
                Error = ex.Message
            };

            await context.Response.WriteAsJsonAsync(
                response,
                new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
                    DefaultIgnoreCondition =
                        JsonIgnoreCondition.WhenWritingNull
                });
        }
        catch (Exception ex)
        {
            _logger.LogError(
                ex,
                "Unexpected error in Currency Service.");

            var elapsed =
                (long)(DateTime.UtcNow - startTime).TotalMilliseconds;

            context.Response.StatusCode =
                (int)HttpStatusCode.InternalServerError;

            context.Response.ContentType =
                "application/json";

            var response = new ApiResponse<object>
            {
                Message = "Internal server error",
                Timestamp = DateTime.UtcNow,
                Elapsed = elapsed,
                Error = ex.Message
            };

            await context.Response.WriteAsJsonAsync(
                response,
                new JsonSerializerOptions
                {
                    PropertyNamingPolicy =
                        JsonNamingPolicy.CamelCase,

                    DefaultIgnoreCondition =
                        JsonIgnoreCondition.WhenWritingNull
                });
        }
    }
}