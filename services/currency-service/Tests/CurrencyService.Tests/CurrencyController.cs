using System.Net;
using System.Net.Http.Json;
using CurrencyService.Application.DTO.Response;
using CurrencyService.Application.Services;
using CurrencyService.Domain;
using CurrencyService.Domain.Exceptions;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.Extensions.DependencyInjection;
using Moq;
using Xunit;

namespace CurrencyService.Tests;

public class CurrencyControllerTests
{
    [Fact]
    public async Task GetAll_WhenCurrencyProviderIsUnavailable_Returns503WithStandardError()
    {
        // Arrange
        var mockCurrencyService = new Mock<ICurrencyService>();

        mockCurrencyService
            .Setup(service => service.GetAllAsync())
            .ThrowsAsync(
                new CurrencyServiceUnavailableException(
                    "Currency provider is unavailable."));

        await using var factory =
            new WebApplicationFactory<Program>()
                .WithWebHostBuilder(builder =>
                {
                    builder.ConfigureServices(services =>
                    {
                        services.AddSingleton(
                            mockCurrencyService.Object);
                    });
                });

        var client = factory.CreateClient();

        // Act
        var response = await client.GetAsync("/currency");

        // Assert
        Assert.Equal(
            HttpStatusCode.ServiceUnavailable,
            response.StatusCode);

        var body =
            await response.Content.ReadFromJsonAsync<ApiResponse<object>>();

        Assert.NotNull(body);

        Assert.Equal(
            "Currency provider unavailable",
            body!.Message);

        Assert.Equal(
            "Currency provider is unavailable.",
            body.Error);

        Assert.True(body.Elapsed >= 0);
        Assert.NotEqual(default, body.Timestamp);
    }

    [Fact]
    public async Task GetByCode_WhenCurrencyDoesNotExist_Returns404WithStandardError()
    {
        // Arrange
        var mockCurrencyService = new Mock<ICurrencyService>();

        mockCurrencyService
            .Setup(service => service.GetByCodeAsync("XYZ"))
            .ReturnsAsync((CurrencyRate?)null);

        await using var factory =
            new WebApplicationFactory<Program>()
                .WithWebHostBuilder(builder =>
                {
                    builder.ConfigureServices(services =>
                    {
                        services.AddSingleton(
                            mockCurrencyService.Object);
                    });
                });

        var client = factory.CreateClient();

        // Act
        var response = await client.GetAsync("/currency/XYZ");

        // Assert
        Assert.Equal(
            HttpStatusCode.NotFound,
            response.StatusCode);

        var body =
            await response.Content.ReadFromJsonAsync<ApiResponse<object>>();

        Assert.NotNull(body);

        Assert.Equal(
            "Currency not found",
            body!.Message);

        Assert.Equal(
            "Invalid currency code",
            body.Error);

        Assert.True(body.Elapsed >= 0);
        Assert.NotEqual(default, body.Timestamp);
    }

    [Fact]
    public async Task GetAll_WhenCurrenciesAreFound_Returns200WithStandardResponse()
    {
        // Arrange
        var rates = new List<CurrencyRate>
        {
            new CurrencyRate
            {
                Code = "USD",
                Value = 5.1262m,
                CreatedAt = DateTime.UtcNow
            },
            new CurrencyRate
            {
                Code = "EUR",
                Value = 5.9425m,
                CreatedAt = DateTime.UtcNow
            }
        };

        var mockCurrencyService = new Mock<ICurrencyService>();

        mockCurrencyService
            .Setup(service => service.GetAllAsync())
            .ReturnsAsync(rates);

        await using var factory =
            new WebApplicationFactory<Program>()
                .WithWebHostBuilder(builder =>
                {
                    builder.ConfigureServices(services =>
                    {
                        services.AddSingleton(
                            mockCurrencyService.Object);
                    });
                });

        var client = factory.CreateClient();

        // Act
        var response = await client.GetAsync("/currency");

        // Assert
        Assert.Equal(
            HttpStatusCode.OK,
            response.StatusCode);

        var body =
            await response.Content
                .ReadFromJsonAsync<ApiResponse<List<CurrencyRate>>>();

        Assert.NotNull(body);

        Assert.Equal(
            "Currencies found",
            body!.Message);

        Assert.NotNull(body.Data);

        Assert.Equal(2, body.Data.Count);

        Assert.Equal("USD", body.Data[0].Code);
        Assert.Equal(5.1262m, body.Data[0].Value);

        Assert.Equal("EUR", body.Data[1].Code);
        Assert.Equal(5.9425m, body.Data[1].Value);

        Assert.True(body.Elapsed >= 0);
        Assert.NotEqual(default, body.Timestamp);
    }
}