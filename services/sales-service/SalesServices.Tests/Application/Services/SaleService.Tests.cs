using Moq;
using Xunit;
using Microsoft.Extensions.Logging;
using SalesService.Application.Services;
using SalesService.Application.Repositories;
using SalesService.Domain.Repositories;
using SalesService.Domain.Exceptions;
using SalesService.Domain.Entities;
using SalesService.Domain.Enums;

namespace SalesService.Tests.Application.Services;


public class SaleServiceTests
{
    private readonly Mock<ISaleRepository> _repositoryMock;
    private readonly Mock<IClientService> _clientMock;
    private readonly Mock<IProductService> _productMock;
    private readonly Mock<ICurrencyService> _currencyMock;
    private readonly Mock<ILogger<SaleService>> _loggerMock;


    private readonly SaleService _service;


    public SaleServiceTests()
    {
        _repositoryMock = new();
        _clientMock = new();
        _productMock = new();
        _currencyMock = new();
        _loggerMock = new();


        _service = new SaleService(
            _repositoryMock.Object,
            _clientMock.Object,
            _productMock.Object,
            _currencyMock.Object,
            _loggerMock.Object
        );
    }

[Fact]
public async Task CreateSale_Should_Create_When_Client_Exists()
{
    // Arrange

    var clientId = "client-001";


    _clientMock
        .Setup(x => x.ClientExists(clientId))
        .ReturnsAsync(true);



    // Act

    var result = await _service.CreateSale(clientId);

    // Assert
    Assert.NotNull(result);

    Assert.Equal(
        clientId,
        result.ClientId
    );


    _repositoryMock.Verify(
        x => x.Save(
            It.IsAny<Sale>()
        ),
        Times.Once
    );
}

[Fact]
public async Task CreateSale_Should_Throw_When_Client_Not_Found()
{
    // Arrange

    var clientId = "client-invalid";


    _clientMock
        .Setup(x => x.ClientExists(clientId))
        .ReturnsAsync(false);



    // Act + Assert


    await Assert.ThrowsAsync<NotFoundException>(
        () => _service.CreateSale(clientId)
    );


    _repositoryMock.Verify(
        x => x.Save(
            It.IsAny<Sale>()
        ),
        Times.Never
    );
}

[Fact]
public void GetById_Should_Return_Sale()
{
    // Arrange

    var sale = new Sale("client-001");

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    // Act

    var result = _service.GetById(sale.Id);

    // Assert

    Assert.NotNull(result);

    Assert.Equal(sale.Id, result.Id);
}

[Fact]
public void GetById_Should_Throw_When_NotFound()
{
    // Arrange

    _repositoryMock
        .Setup(x => x.GetById(It.IsAny<string>()))
        .Returns((Sale?)null);

    // Act + Assert

    Assert.Throws<NotFoundException>(
        () => _service.GetById("sale-001"));
}

[Fact]
public async Task AddItem_Should_Add_Item()
{
    // Arrange

    var sale = new Sale("client-001");

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    _productMock
        .Setup(x => x.GetPrice("product-001"))
        .ReturnsAsync(100);

    // Act

    await _service.AddItem(
        sale.Id,
        "product-001",
        2);

    // Assert

    Assert.Single(sale.Items);

    _repositoryMock.Verify(
        x => x.Update(sale),
        Times.Once);
}
[Fact]
public async Task AddItem_Should_Increase_Quantity_When_Product_Already_Exists()
{
    // Arrange

    var sale = new Sale("client-001");

    sale.AddItem(
        "product-001",
        2,
        100);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    _productMock
        .Setup(x => x.GetPrice("product-001"))
        .ReturnsAsync(100);

    // Act

    await _service.AddItem(
        sale.Id,
        "product-001",
        3);

    // Assert

    Assert.Single(sale.Items);

    Assert.Equal(
        5,
        sale.Items.First().Quantity);

    Assert.Equal(
        100,
        sale.Items.First().UnitPrice);

    _repositoryMock.Verify(
        x => x.Update(sale),
        Times.Once);
}

[Fact]
public async Task AddItem_Should_Throw_When_Total_Quantity_Exceeds_Stock()
{
    // Arrange

    var sale = new Sale("client-001");

    sale.AddItem(
        "product-001",
        8,
        100);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    // Act + Assert

    await Assert.ThrowsAsync<BusinessException>(
        () => _service.AddItem(
            sale.Id,
            "product-001",
            3));

    // A quantidade original não deve ter sido alterada
    Assert.Equal(
        8,
        sale.Items.First().Quantity);

    // Não deve persistir a venda
    _repositoryMock.Verify(
        x => x.Update(sale),
        Times.Never);
}
[Fact]
public async Task AddItem_Should_Throw_When_Stock_Is_Insufficient()
{
    var sale = new Sale("client-001");

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(1);

    await Assert.ThrowsAsync<BusinessException>(
        () => _service.AddItem(
            sale.Id,
            "product-001",
            5));
}

[Fact]
public async Task AddItem_Should_Throw_When_Quantity_Is_Invalid()
{
    var sale = new Sale("client-001");

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    await Assert.ThrowsAsync<ValidationException>(
        () => _service.AddItem(
            sale.Id,
            "product-001",
            0));
}

[Fact]
public void CancelSale_Should_Cancel_Sale()
{
    var sale = new Sale("client-001");

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _service.CancelSale(sale.Id);

    Assert.Equal(
        SaleStatus.Canceled,
        sale.Status);

    _repositoryMock.Verify(
        x => x.Update(sale),
        Times.Once);
}

[Fact]
public async Task UpdateItem_Should_Update_Quantity()
{
    var sale = new Sale("client-001");

    sale.AddItem(
        "product-001",
        1,
        100);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    await _service.UpdateItem(
        sale.Id,
        "product-001",
        5);

    Assert.Equal(
        5,
        sale.Items.First().Quantity);

    _repositoryMock.Verify(
        x => x.Update(sale),
        Times.Once);
}

[Fact]
public async Task GetByStatus_Should_Return_List()
{
    var sales = new List<Sale>
    {
        new Sale("client-001")
    };

    _repositoryMock
        .Setup(x => x.GetByStatus(SaleStatus.Started))
        .Returns(sales);

    var result =
        await _service.GetByStatus("Started");

    Assert.Single(result);
}

[Fact]
public async Task GetByProductId_Should_Return_List()
{
    var sales = new List<Sale>
    {
        new Sale("client-001")
    };

    _repositoryMock
        .Setup(x => x.GetByProductId("product-001"))
        .Returns(sales);

    var result =
        await _service.GetByProductId("product-001");

    Assert.Single(result);
}

[Fact]
public async Task GetTotalSalesByProductAndStatus_Should_Return_Result()
{
    var expected = new Dictionary<SaleStatus, int>
    {
        { SaleStatus.Started, 2 },
        { SaleStatus.Done, 5 }
    };

    _repositoryMock
        .Setup(x => x.GetTotalSalesByProductAndStatus("product-001"))
        .Returns(expected);

    var result =
        await _service.GetTotalSalesByProductAndStatus("product-001");

    Assert.Equal(2, result.Count);

    Assert.Equal(5, result[SaleStatus.Done]);
}

// FinishSale
[Fact]
public async Task FinishSale_Should_Finish_Sale()
{
    // Arrange

    var sale = new Sale("client-001");

    sale.AddItem("product-001", 2, 100);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    _productMock
        .Setup(x => x.DecreaseStock("product-001", 2))
        .Returns(Task.CompletedTask);

    _currencyMock
        .Setup(x => x.GetAllRates())
        .ReturnsAsync(new Dictionary<string, decimal>
        {
            { "BRL", 1 },
            { "USD", 5 }
        });

    // Act

    var result = await _service.FinishSale(sale.Id);

    // Assert

    Assert.Equal(
        SaleStatus.Done,
        sale.Status);

    Assert.Equal(
        200,
        result.TotalBRL);
}
[Fact]
public async Task FinishSale_Should_Throw_When_Sale_NotFound()
{
    _repositoryMock
        .Setup(x => x.GetById(It.IsAny<string>()))
        .Returns((Sale?)null);

    await Assert.ThrowsAsync<NotFoundException>(
        () => _service.FinishSale("sale-001"));
}
[Fact]
public async Task FinishSale_Should_Throw_When_Stock_Is_Insufficient()
{
    var sale = new Sale("client-001");

    sale.AddItem("product-001", 10, 100);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(2);

    await Assert.ThrowsAsync<BusinessException>(
        () => _service.FinishSale(sale.Id));
}
[Fact]
public async Task FinishSale_Should_Decrease_Stock()
{
    var sale = new Sale("client-001");

    sale.AddItem("product-001", 3, 50);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    _productMock
        .Setup(x => x.DecreaseStock("product-001", 3))
        .Returns(Task.CompletedTask);

    _currencyMock
        .Setup(x => x.GetAllRates())
        .ReturnsAsync(new Dictionary<string, decimal>
        {
            { "BRL", 1 }
        });

    await _service.FinishSale(sale.Id);

    _productMock.Verify(
        x => x.DecreaseStock("product-001", 3),
        Times.Once);
}
[Fact]
public async Task FinishSale_Should_Update_Repository()
{
    var sale = new Sale("client-001");

    sale.AddItem("product-001", 1, 100);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    _productMock
        .Setup(x => x.DecreaseStock("product-001", 1))
        .Returns(Task.CompletedTask);

    _currencyMock
        .Setup(x => x.GetAllRates())
        .ReturnsAsync(new Dictionary<string, decimal>
        {
            { "BRL", 1 }
        });

    await _service.FinishSale(sale.Id);

    _repositoryMock.Verify(
        x => x.Update(sale),
        Times.Once);
}
[Fact]
public async Task FinishSale_Should_Return_All_Currencies()
{
    var sale = new Sale("client-001");

    sale.AddItem("product-001", 2, 100);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    _productMock
        .Setup(x => x.DecreaseStock("product-001", 2))
        .Returns(Task.CompletedTask);

    _currencyMock
        .Setup(x => x.GetAllRates())
        .ReturnsAsync(new Dictionary<string, decimal>
        {
            { "BRL", 1m },
            { "USD", 5m },
            { "EUR", 6m }
        });

    var result = await _service.FinishSale(sale.Id);

    Assert.Equal(3, result.Coins.Count);

    Assert.Equal(200, result.TotalBRL);

    Assert.Equal(40, result.Coins["USD"]);

    Assert.Equal(33.33m, result.Coins["EUR"]);
}
[Fact]
public async Task FinishSale_Should_Throw_When_Sale_Has_No_Items()
{
    var sale = new Sale("client-001");

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    await Assert.ThrowsAsync<BusinessException>(
        () => _service.FinishSale(sale.Id));
}

[Fact]
public async Task FinishSale_Should_Compensate_Stock_When_Second_Product_Fails()
{
    // Arrange

    var sale = new Sale("client-001");

    sale.AddItem("product-001", 2, 100);
    sale.AddItem("product-002", 2, 50);

    _repositoryMock
        .Setup(x => x.GetById(sale.Id))
        .Returns(sale);

    // Ambos possuem estoque suficiente no pré-check
    _productMock
        .Setup(x => x.GetStock("product-001"))
        .ReturnsAsync(10);

    _productMock
        .Setup(x => x.GetStock("product-002"))
        .ReturnsAsync(10);

    // Primeiro produto consegue reduzir o estoque
    _productMock
        .Setup(x => x.DecreaseStock("product-001", 2))
        .Returns(Task.CompletedTask);

    // Segundo produto falha
    _productMock
        .Setup(x => x.DecreaseStock("product-002", 2))
        .ThrowsAsync(
            new DependencyUnavailableException(
                "Product Service is unavailable."));

    // Act + Assert

    await Assert.ThrowsAsync<DependencyUnavailableException>(
        () => _service.FinishSale(sale.Id));

    // O primeiro produto foi realmente reduzido
    _productMock.Verify(
        x => x.DecreaseStock("product-001", 2),
        Times.Once);

    // O segundo produto tentou reduzir e falhou
    _productMock.Verify(
        x => x.DecreaseStock("product-002", 2),
        Times.Once);

    // O primeiro produto precisa ser compensado
    _productMock.Verify(
        x => x.IncreaseStock("product-001", 2),
        Times.Once);

    // A venda NÃO deve ser finalizada
    Assert.NotEqual(
        SaleStatus.Done,
        sale.Status);

    // O repository NÃO deve salvar a venda como finalizada
    _repositoryMock.Verify(
        x => x.Update(sale),
        Times.Never);
}

}