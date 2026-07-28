using System.Security.Claims;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

using SalesService.Api.Controllers;
using SalesService.Application.DTO.Request;
using SalesService.Application.DTO.Response;
using SalesService.Application.Repositories;
using SalesService.Domain.Entities;
using SalesService.Domain.Enums;

namespace SalesServices.Tests.Api.Controllers;

public class SalesControllerTests
{
    private readonly Mock<ISaleService> _serviceMock;
    private readonly Mock<ILogger<SalesController>> _loggerMock;

    private readonly SalesController _controller;

    public SalesControllerTests()
    {
        _serviceMock = new Mock<ISaleService>();
        _loggerMock = new Mock<ILogger<SalesController>>();

        _controller = new SalesController(
            _serviceMock.Object,
            _loggerMock.Object);
    }

    private void SetAuthenticatedUser(string clientId)
    {
        var user = new ClaimsPrincipal(
            new ClaimsIdentity(
            new[]
            {
                new Claim("client_id", clientId)
            },
            "TestAuth"));

        _controller.ControllerContext =
            new ControllerContext
            {
                HttpContext = new DefaultHttpContext
                {
                    User = user
                }
            };
    }

    [Fact]
    public async Task Create_Should_Return_Created()
    {
        // Arrange

        SetAuthenticatedUser("client-001");

        var sale = new Sale("client-001");

        _serviceMock
            .Setup(x => x.CreateSale("client-001"))
            .ReturnsAsync(sale);

        // Act

        var result = await _controller.Create();

        // Assert

        var created =
            Assert.IsType<CreatedResult>(result);

        var response =
            Assert.IsType<ApiResponse<SaleResponse>>(created.Value);

        Assert.Equal(
            "Sale created successfully",
            response.Message);

        Assert.NotNull(response.Data);

        _serviceMock.Verify(
            x => x.CreateSale("client-001"),
            Times.Once);
    }

    [Fact]
    public async Task Create_Should_Return_Unauthorized_When_Client_Not_In_Token()
    {
        // Arrange

        _controller.ControllerContext =
            new ControllerContext
            {
                HttpContext = new DefaultHttpContext()
            };

        // Act

        var result = await _controller.Create();

        // Assert

        Assert.IsType<UnauthorizedResult>(result);

        _serviceMock.Verify(
            x => x.CreateSale(It.IsAny<string>()),
            Times.Never);
    }

    [Fact]
    public void GetById_Should_Return_Ok()
    {
        // Arrange

        var sale = new Sale("client-001");

        _serviceMock
            .Setup(x => x.GetById(sale.Id))
            .Returns(sale);

        // Act

        var result = _controller.GetById(sale.Id);

        // Assert

        var ok =
            Assert.IsType<OkObjectResult>(result);

        var response =
            Assert.IsType<ApiResponse<SaleResponse>>(ok.Value);

        Assert.Equal(
            "Sale found",
            response.Message);

        Assert.NotNull(response.Data);

        Assert.Equal(
            sale.Id,
            response.Data!.Id);

        _serviceMock.Verify(
            x => x.GetById(sale.Id),
            Times.Once);
    }

    [Fact]
    public async Task AddItem_Should_Return_Ok()
    {
        // Arrange

        var request = new AddItemRequest
        {
            ProductId = "product-001",
            Quantity = 2
        };

        // Act

        var result =
            await _controller.AddItem(
                "sale-001",
                request);

        // Assert

        var ok =
            Assert.IsType<OkObjectResult>(result);

        var response =
            Assert.IsType<ApiResponse<object>>(ok.Value);

        Assert.Equal(
            "Item added successfully",
            response.Message);

        _serviceMock.Verify(
            x => x.AddItem(
                "sale-001",
                "product-001",
                2),
            Times.Once);
    }
   
[Fact]
public async Task UpdateItem_Should_Return_Ok()
{
    // Arrange

    var request = new UpdateItemRequest
    {
        Quantity = 5
    };

    // Act

    var result = await _controller.UpdateItem(
        "sale-001",
        "product-001",
        request);

    // Assert

    var ok = Assert.IsType<OkObjectResult>(result);

    Assert.NotNull(ok.Value);

    var value = ok.Value;

    var successProperty = value!.GetType().GetProperty("success");
    var messageProperty = value.GetType().GetProperty("message");

    Assert.NotNull(successProperty);
    Assert.NotNull(messageProperty);

    Assert.Equal(
        true,
        successProperty!.GetValue(value));

    Assert.Equal(
        "Item updated",
        messageProperty!.GetValue(value));

    _serviceMock.Verify(x =>
        x.UpdateItem(
            "sale-001",
            "product-001",
            5),
        Times.Once);
}
[Fact]
public async Task Finish_Should_Return_Ok()
{
    // Arrange

    var response = new SaleTotalResponse
    {
        TotalBRL = 200,
        Coins = new Dictionary<string, decimal>
        {
            { "BRL", 200 },
            { "USD", 40 }
        }
    };

    _serviceMock
        .Setup(x => x.FinishSale("sale-001"))
        .ReturnsAsync(response);

    // Act

    var result = await _controller.Finish("sale-001");

    // Assert

    var ok = Assert.IsType<OkObjectResult>(result);

    var api =
        Assert.IsType<ApiResponse<object>>(ok.Value);

    Assert.Equal(
        "Sale finished successfully",
        api.Message);

    Assert.NotNull(api.Data);

    _serviceMock.Verify(
        x => x.FinishSale("sale-001"),
        Times.Once);
}

[Fact]
public void Cancel_Should_Return_Ok()
{
    // Act

    var result = _controller.Cancel("sale-001");

    // Assert

    var ok =
        Assert.IsType<OkObjectResult>(result);

    var api =
        Assert.IsType<ApiResponse<object>>(ok.Value);

    Assert.Equal(
        "Sale canceled successfully",
        api.Message);

    _serviceMock.Verify(
        x => x.CancelSale("sale-001"),
        Times.Once);
}
[Fact]
public async Task GetByProduct_Should_Return_Ok()
{
    // Arrange

    var sales = new List<Sale>
    {
        new Sale("client-001"),
        new Sale("client-002")
    };

    _serviceMock
        .Setup(x => x.GetByProductId("product-001"))
        .ReturnsAsync(sales);

    // Act

    var result = await _controller.GetByProduct("product-001");

    // Assert

    var ok = Assert.IsType<OkObjectResult>(result);

    var response =
        Assert.IsType<ApiResponse<List<SaleResponse>>>(ok.Value);

    Assert.Equal("Sales found", response.Message);

    Assert.Equal(2, response.Data!.Count);

    _serviceMock.Verify(
        x => x.GetByProductId("product-001"),
        Times.Once);
}

[Fact]
public async Task GetByStatus_Should_Return_Ok()
{
    // Arrange

    var sales = new List<Sale>
    {
        new Sale("client-001"),
        new Sale("client-002")
    };

    _serviceMock
        .Setup(x => x.GetByStatus("Progress"))
        .ReturnsAsync(sales);

    // Act

    var result = await _controller.GetByStatus("Progress");

    // Assert

    var ok = Assert.IsType<OkObjectResult>(result);

    var response =
        Assert.IsType<ApiResponse<List<SaleResponse>>>(ok.Value);

    Assert.Equal("Sales found", response.Message);

    Assert.Equal(2, response.Data!.Count);

    _serviceMock.Verify(
        x => x.GetByStatus("Progress"),
        Times.Once);
}

[Fact]
public async Task GetTotals_Should_Return_Ok()
{
    // Arrange

    var totals = new Dictionary<SaleStatus, int>
    {
        { SaleStatus.Started, 5 },
        { SaleStatus.Done, 2 }
    };

    _serviceMock
        .Setup(x => x.GetTotalSalesByProductAndStatus("product-001"))
        .ReturnsAsync(totals);

    // Act

    var result = await _controller.GetTotals("product-001");

    // Assert

    var ok = Assert.IsType<OkObjectResult>(result);

    var response =
        Assert.IsType<ApiResponse<Dictionary<SaleStatus, int>>>(ok.Value);

    Assert.Equal("Totals found", response.Message);

    Assert.Equal(2, response.Data!.Count);

    Assert.Equal(5, response.Data[SaleStatus.Started]);

    Assert.Equal(2, response.Data[SaleStatus.Done]);

    _serviceMock.Verify(
        x => x.GetTotalSalesByProductAndStatus("product-001"),
        Times.Once);
}
}