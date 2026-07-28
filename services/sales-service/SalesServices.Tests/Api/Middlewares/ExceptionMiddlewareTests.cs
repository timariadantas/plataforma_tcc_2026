using System.Net;
using System.Text.Json;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

using SalesService.API.Middlewares;
using SalesService.Application.DTO.Response;
using SalesService.Domain.Exceptions;

namespace SalesServices.Tests.Api.Middlewares;

public class ExceptionMiddlewareTests
{
    private readonly Mock<ILogger<ExceptionMiddleware>> _logger;

    public ExceptionMiddlewareTests()
    {
        _logger = new Mock<ILogger<ExceptionMiddleware>>();
    }

    [Fact]
    public async Task Invoke_Should_Return_404_When_NotFoundException_Is_Thrown()
    {
        // Arrange
        RequestDelegate next = context =>
            throw new NotFoundException("Sale not found");

        var middleware = new ExceptionMiddleware(next, _logger.Object);

        var context = new DefaultHttpContext();
        context.Response.Body = new MemoryStream();

        // Act
        await middleware.Invoke(context);

        // Assert
        Assert.Equal((int)HttpStatusCode.NotFound, context.Response.StatusCode);

        context.Response.Body.Position = 0;

        var body = await new StreamReader(context.Response.Body).ReadToEndAsync();

        var response =
            JsonSerializer.Deserialize<ApiResponse<object>>(body);

        Assert.NotNull(response);
        Assert.Equal("Sale not found", response!.Error);
    }

    [Fact]
    public async Task Invoke_Should_Return_400_When_ValidationException_Is_Thrown()
    {
        RequestDelegate next = context =>
            throw new ValidationException("Invalid quantity");

        var middleware = new ExceptionMiddleware(next, _logger.Object);

        var context = new DefaultHttpContext();
        context.Response.Body = new MemoryStream();

        await middleware.Invoke(context);

        Assert.Equal((int)HttpStatusCode.BadRequest,
            context.Response.StatusCode);
    }

    [Fact]
    public async Task Invoke_Should_Return_422_When_BusinessException_Is_Thrown()
    {
        RequestDelegate next = context =>
            throw new BusinessException("Business error");

        var middleware = new ExceptionMiddleware(next, _logger.Object);

        var context = new DefaultHttpContext();
        context.Response.Body = new MemoryStream();

        await middleware.Invoke(context);

        Assert.Equal((int)HttpStatusCode.UnprocessableEntity,
            context.Response.StatusCode);
    }

    [Fact]
    public async Task Invoke_Should_Return_409_When_ConflictException_Is_Thrown()
    {
        RequestDelegate next = context =>
            throw new ConflictException("Conflict");

        var middleware = new ExceptionMiddleware(next, _logger.Object);

        var context = new DefaultHttpContext();
        context.Response.Body = new MemoryStream();

        await middleware.Invoke(context);

        Assert.Equal((int)HttpStatusCode.Conflict,
            context.Response.StatusCode);
    }

    [Fact]
    public async Task Invoke_Should_Return_401_When_UnauthorizedException_Is_Thrown()
    {
        RequestDelegate next = context =>
            throw new UnauthorizedException("Unauthorized");

        var middleware = new ExceptionMiddleware(next, _logger.Object);

        var context = new DefaultHttpContext();
        context.Response.Body = new MemoryStream();

        await middleware.Invoke(context);

        Assert.Equal((int)HttpStatusCode.Unauthorized,
            context.Response.StatusCode);
    }

    [Fact]
    public async Task Invoke_Should_Return_500_When_Generic_Exception_Is_Thrown()
    {
        RequestDelegate next = context =>
            throw new Exception("Unexpected error");

        var middleware = new ExceptionMiddleware(next, _logger.Object);

        var context = new DefaultHttpContext();
        context.Response.Body = new MemoryStream();

        await middleware.Invoke(context);

        Assert.Equal((int)HttpStatusCode.InternalServerError,
            context.Response.StatusCode);
    }

    [Fact]
    public async Task Invoke_Should_Call_Next_When_No_Exception_Is_Thrown()
    {
        var executed = false;

        RequestDelegate next = context =>
        {
            executed = true;
            return Task.CompletedTask;
        };

        var middleware = new ExceptionMiddleware(next, _logger.Object);

        var context = new DefaultHttpContext();

        await middleware.Invoke(context);

        Assert.True(executed);
    }
}