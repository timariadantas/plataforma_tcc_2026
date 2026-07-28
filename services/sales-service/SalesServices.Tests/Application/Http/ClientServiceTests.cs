using System.Net;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;
using SalesService.Application.Services;
using SalesServices.Tests.Application.TestHelpers;

namespace SalesServices.Tests.Application.Services;
public class ClientServiceClientTests
{
    [Fact]
    public async Task ClientExists_Should_Return_True()
    {
        var handler = new FakeHttpMessageHandler(
            new HttpResponseMessage(HttpStatusCode.OK));

        var http = new HttpClient(handler)
        {
            BaseAddress = new Uri("http://localhost")
        };

        var logger =
            new Mock<ILogger<ClientServiceClient>>();

        var service =
            new ClientServiceClient(http, logger.Object);

        var exists =
            await service.ClientExists("client-001");

        Assert.True(exists);
    }

    [Fact]
    public async Task ClientExists_Should_Return_False()
    {
        var handler = new FakeHttpMessageHandler(
            new HttpResponseMessage(HttpStatusCode.NotFound));

        var http = new HttpClient(handler)
        {
            BaseAddress = new Uri("http://localhost")
        };

        var logger =
            new Mock<ILogger<ClientServiceClient>>();

        var service =
            new ClientServiceClient(http, logger.Object);

        var exists =
            await service.ClientExists("client-001");

        Assert.False(exists);
    }
}