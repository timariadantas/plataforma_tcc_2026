using System.Net;
using System.Net.Http;
using Microsoft.Extensions.Logging;
using Xunit;
using SalesService.Application.Services;

namespace SalesServices.Tests.Application.Services;

public class CurrencyServiceTests
{
    [Fact]
    public async Task GetAllRates_Should_Return_Currency_Rates()
    {
      // Arrange
        var handler = new FakeHttpMessageHandler(
            """
            {
                "message": "Currency rates retrieved successfully",
                "timestamp": "2026-09-26T12:00:00Z",
                "elapsed": 10,
                "data": [
                    {
                        "code": "USD",
                        "value": 5.10,
                        "createdAt": "2026-09-26T12:00:00Z"
                    },
                    {
                        "code": "EUR",
                        "value": 5.50,
                        "createdAt": "2026-09-26T12:00:00Z"
                    },
                    {
                        "code": "BRL",
                        "value": 1.00,
                        "createdAt": "2026-09-26T12:00:00Z"
                    }
                ]
            }
            """);

        var httpClient = new HttpClient(handler)
        {
            BaseAddress = new Uri("http://currency-service")
        };

        using var loggerFactory =
            LoggerFactory.Create(builder => { });

        var logger =
            loggerFactory.CreateLogger<CurrencyServiceClient>();

        var service =
            new CurrencyServiceClient(httpClient, logger);

        // Act
        var result = await service.GetAllRates();

        // Assert
        Assert.NotNull(result);

        Assert.Equal(3, result.Count);

        Assert.Equal(5.10m, result["USD"]);
        Assert.Equal(5.50m, result["EUR"]);
        Assert.Equal(1.00m, result["BRL"]);
  }

    private class FakeHttpMessageHandler : HttpMessageHandler
    {
        private readonly string _responseContent;

        public FakeHttpMessageHandler(string responseContent)
        {
            _responseContent = responseContent;
        }

        protected override Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            var response = new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = new StringContent(
                    _responseContent,
                    System.Text.Encoding.UTF8,
                    "application/json")
            };

            return Task.FromResult(response);
        }
    }
}