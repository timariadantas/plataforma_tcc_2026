using System.Net;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

using SalesService.Application.Services;
using SalesService.Domain.Exceptions;

using SalesServices.Tests.Application.TestHelpers;

namespace SalesServices.Tests.Application.Services;

public class ProductServiceClientTests{


 
[Fact]
public async Task GetStock_Should_Return_Quantity()
{
    var json =
        """
        {
            "id":"product-001",
            "price":10.5,
            "quantity":20
        }
        """;

    var handler = new FakeHttpMessageHandler(
        new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent(json)
        });

    var http = new HttpClient(handler)
    {
        BaseAddress = new Uri("http://localhost")
    };

    var logger =
        new Mock<ILogger<ProductServiceClient>>();

    var service =
        new ProductServiceClient(http, logger.Object);

    var stock = await service.GetStock("product-001");

    Assert.Equal(20, stock);
}

[Fact]
public async Task GetPrice_Should_Return_Price()
{
    var json =
        """
        {
            "id":"product-001",
            "price":15.75,
            "quantity":8
        }
        """;

    var handler = new FakeHttpMessageHandler(
        new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent(json)
        });

    var http = new HttpClient(handler)
    {
        BaseAddress = new Uri("http://localhost")
    };

    var logger =
        new Mock<ILogger<ProductServiceClient>>();

    var service =
        new ProductServiceClient(http, logger.Object);

    var price = await service.GetPrice("product-001");

    Assert.Equal(15.75m, price);
}

[Fact]
public async Task GetStock_Should_Throw_NotFoundException()
{
    var handler = new FakeHttpMessageHandler(
        new HttpResponseMessage(HttpStatusCode.NotFound));

    var http = new HttpClient(handler)
    {
        BaseAddress = new Uri("http://localhost")
    };

    var logger =
        new Mock<ILogger<ProductServiceClient>>();

    var service =
        new ProductServiceClient(http, logger.Object);

    await Assert.ThrowsAsync<NotFoundException>(() =>
        service.GetStock("product-001"));
}

[Fact]
public async Task GetPrice_Should_Throw_NotFoundException()
{
    var handler = new FakeHttpMessageHandler(
        new HttpResponseMessage(HttpStatusCode.NotFound));

    var http = new HttpClient(handler)
    {
        BaseAddress = new Uri("http://localhost")
    };

    var logger =
        new Mock<ILogger<ProductServiceClient>>();

    var service =
        new ProductServiceClient(http, logger.Object);

    await Assert.ThrowsAsync<NotFoundException>(() =>
        service.GetPrice("product-001"));
}

[Fact]
public async Task GetStock_Should_Throw_ValidationException_When_Response_Is_Invalid()
{
    var handler = new FakeHttpMessageHandler(
        new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent("null")
        });

    var http = new HttpClient(handler)
    {
        BaseAddress = new Uri("http://localhost")
    };

    var logger =
        new Mock<ILogger<ProductServiceClient>>();

    var service =
        new ProductServiceClient(http, logger.Object);

    await Assert.ThrowsAsync<ValidationException>(() =>
        service.GetStock("product-001"));
}
[Fact]
public async Task DecreaseStock_Should_Not_Throw()
{
    var handler = new FakeHttpMessageHandler(
        new HttpResponseMessage(HttpStatusCode.OK));

    var http = new HttpClient(handler)
    {
        BaseAddress = new Uri("http://localhost")
    };

    var logger =
        new Mock<ILogger<ProductServiceClient>>();

    var service =
        new ProductServiceClient(http, logger.Object);

    await service.DecreaseStock("product-001", 3);
}

[Fact]
public async Task DecreaseStock_Should_Throw_ValidationException()
{
    var handler = new FakeHttpMessageHandler(
        new HttpResponseMessage(HttpStatusCode.BadRequest));

    var http = new HttpClient(handler)
    {
        BaseAddress = new Uri("http://localhost")
    };

    var logger =
        new Mock<ILogger<ProductServiceClient>>();

    var service =
        new ProductServiceClient(http, logger.Object);

    await Assert.ThrowsAsync<ValidationException>(() =>
        service.DecreaseStock("product-001", 5));
}

}