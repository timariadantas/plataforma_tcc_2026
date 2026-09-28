using System.Net;
using CurrencyService.Application.Services;
using CurrencyService.Domain.Exceptions;
using Microsoft.Extensions.Logging.Abstractions;
using Xunit;

namespace CurrencyService.Tests;

public class CurrencyServiceTests
{
    public CurrencyServiceTests()
    {
        var cacheField =
            typeof(CurrencyService.Application.Services.CurrencyService)
                .GetField(
                    "_cache",
                    System.Reflection.BindingFlags.Static |
                    System.Reflection.BindingFlags.NonPublic);

        var lastUpdateField =
            typeof(CurrencyService.Application.Services.CurrencyService)
                .GetField(
                    "_lastUpdate",
                    System.Reflection.BindingFlags.Static |
                    System.Reflection.BindingFlags.NonPublic);

        cacheField?.SetValue(null, null);
        lastUpdateField?.SetValue(null, DateTime.MinValue);
    }

    [Fact]
    public async Task GetAllAsync_WhenProviderReturns429_ThrowsCurrencyServiceUnavailableException()
    {
        // Arrange
        var handler = new FakeHttpMessageHandler(
            HttpStatusCode.TooManyRequests);

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var exception =
            await Assert.ThrowsAsync<CurrencyServiceUnavailableException>(
                () => service.GetAllAsync());

        // Assert
        Assert.Equal(
            "Currency provider is unavailable.",
            exception.Message);
    }

    [Fact]
    public async Task GetAllAsync_WhenProviderTimesOut_ThrowsCurrencyServiceUnavailableException()
    {
        // Arrange
        var handler = new FakeTimeoutHttpMessageHandler();

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var exception =
            await Assert.ThrowsAsync<CurrencyServiceUnavailableException>(
                () => service.GetAllAsync());

        // Assert
        Assert.Equal(
            "Currency provider timeout.",
            exception.Message);
    }

    [Fact]
    public async Task GetAllAsync_WhenProviderReturns500_ThrowsCurrencyServiceUnavailableException()
    {
        // Arrange
        var handler = new FakeHttpMessageHandler(
            HttpStatusCode.InternalServerError);

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var exception =
            await Assert.ThrowsAsync<CurrencyServiceUnavailableException>(
                () => service.GetAllAsync());

        // Assert
        Assert.Equal(
            "Currency provider is unavailable.",
            exception.Message);
    }

    [Fact]
    public async Task GetAllAsync_WhenProviderThrowsHttpRequestException_ThrowsCurrencyServiceUnavailableException()
    {
        // Arrange
        var handler = new FakeHttpRequestExceptionHandler();

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var exception =
            await Assert.ThrowsAsync<CurrencyServiceUnavailableException>(
                () => service.GetAllAsync());

        // Assert
        Assert.Equal(
            "Currency provider is unavailable.",
            exception.Message);
    }

    [Fact]
    public async Task GetAllAsync_WhenProviderReturnsValidResponse_ParsesCurrencyCorrectly()
    {
        // Arrange
        var handler = new FakeSuccessHttpMessageHandler();

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var rates = await service.GetAllAsync();

        // Assert
        var usd = rates.First(rate => rate.Code == "USD");

        Assert.Equal(5.1262m, usd.Value);
    }

    [Fact]
    public async Task GetAllAsync_WhenCalledTwiceOnSameDay_UsesCache()
    {
        // Arrange
        var handler = new FakeSuccessHttpMessageHandler();

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var firstResult = await service.GetAllAsync();
        var secondResult = await service.GetAllAsync();

        // Assert
        Assert.NotNull(firstResult);
        Assert.NotNull(secondResult);

        Assert.Equal(
            1,
            handler.CallCount);
    }

    [Fact]
    public async Task GetByCodeAsync_WhenCurrencyExists_ReturnsCurrency()
    {
        // Arrange
        var handler = new FakeSuccessHttpMessageHandler();

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var rate = await service.GetByCodeAsync("USD");

        // Assert
        Assert.NotNull(rate);
        Assert.Equal("USD", rate.Code);
        Assert.Equal(5.1262m, rate.Value);
    }

    [Fact]
    public async Task GetByCodeAsync_WhenCurrencyDoesNotExist_ReturnsNull()
    {
        // Arrange
        var handler = new FakeSuccessHttpMessageHandler();

        var httpClient = new HttpClient(handler);

        var service =
            new CurrencyService.Application.Services.CurrencyService(
                httpClient,
                NullLogger<CurrencyService.Application.Services.CurrencyService>.Instance);

        // Act
        var rate = await service.GetByCodeAsync("XYZ");

        // Assert
        Assert.Null(rate);
    }

    private class FakeHttpMessageHandler : HttpMessageHandler
    {
        private readonly HttpStatusCode _statusCode;

        public FakeHttpMessageHandler(HttpStatusCode statusCode)
        {
            _statusCode = statusCode;
        }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            return Task.FromResult(
                new HttpResponseMessage(_statusCode));
        }
    }

    private class FakeTimeoutHttpMessageHandler : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            throw new TaskCanceledException(
                "Simulated timeout.");
        }
    }

    private class FakeHttpRequestExceptionHandler : HttpMessageHandler
    {
        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            throw new HttpRequestException(
                "Simulated network failure.");
        }
    }

    private class FakeSuccessHttpMessageHandler : HttpMessageHandler
    {
        public int CallCount { get; private set; }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            CallCount++;

            var json = """
            {
                "USDBRL": {
                    "bid": "5.1262"
                },
                "EURBRL": {
                    "bid": "5.9425"
                },
                "GBPBRL": {
                    "bid": "6.7100"
                },
                "CNYBRL": {
                    "bid": "0.7600"
                }
            }
            """;

            var response = new HttpResponseMessage(
                HttpStatusCode.OK);

            response.Content = new StringContent(
                json,
                System.Text.Encoding.UTF8,
                "application/json");

            return Task.FromResult(response);
        }
    }
}