using Moq;
using Xunit;
using Microsoft.Extensions.Logging;
using System.Data;
using SalesService.Domain.Entities;
using SalesService.Domain.Enums;
using SalesService.Domain.Repositories;
using SalesService.Infrastructute.Repositories;
using SalesService.Infrastructute.Executor;
using SalesService.Infrastructute.DataBase;

namespace SalesService.Tests.Infrastructure;


public class SaleRepositoryTests
{
    private readonly Mock<ILogger<SaleRepository>> _loggerMock;
    private readonly Mock<IDbConnectionFactory> _connectionFactoryMock;
    private readonly Mock<IDatabaseExecutor> _executorMock;
    
    private readonly Mock<IDbConnection> _connectionMock;
    private readonly Mock<IDbTransaction> _transactionMock;
 


    private readonly SaleRepository _repository;


    public SaleRepositoryTests()
    {
        _loggerMock = new();
        _connectionFactoryMock = new();
        _executorMock = new();

        _connectionMock = new();
        _transactionMock = new();
        


        _connectionFactoryMock
            .Setup(x => x.CreateConnection())
            .Returns(_connectionMock.Object);


        _connectionMock
            .Setup(x => x.BeginTransaction())
            .Returns(_transactionMock.Object);


        _repository = new SaleRepository(
            _loggerMock.Object,
            _connectionFactoryMock.Object,
            _executorMock.Object);
    }



    [Fact]
    public void Save_Should_Insert_Sale_And_Items_Successfully()
    {
        // Arrange

        var sale = new Sale(
            "client-001"
        );


        sale.LoadItem(
            "product-001",
            2,
            50,
            DateTime.UtcNow,
            DateTime.UtcNow
        );


        // Act

        _repository.Save(sale);



        // Assert

        _executorMock.Verify(
            x => x.Execute(
                It.IsAny<string>(),
                _connectionMock.Object,
                _transactionMock.Object,
                It.IsAny<Dictionary<string,object>>()),
            Times.Exactly(2)
        );


        _transactionMock.Verify(
            x => x.Commit(),
            Times.Once
        );
    }

     [Fact]
    public void Save_Should_Insert_Sale_And_Items_And_Commit()
    {
        // Arrange

        var sale = new Sale("client-001");


        sale.AddItem(
            "product-001",
            2,
            50
        );


        // Act

        _repository.Save(sale);



        // Assert


        _executorMock.Verify(
            x => x.Execute(
                It.IsAny<string>(),
                _connectionMock.Object,
                _transactionMock.Object,
                It.IsAny<Dictionary<string,object>>()
            ),
            Times.Exactly(2)
        );


        _transactionMock.Verify(
            x => x.Commit(),
            Times.Once
        );


        _transactionMock.Verify(
            x => x.Rollback(),
            Times.Never
        );
    }
    [Fact]
public void Save_Should_Rollback_When_Insert_Fails()
{
    // Arrange

    var sale = new Sale("client-001");

    sale.AddItem(
        "product-001",
        2,
        50
    );


    _executorMock
        .SetupSequence(x => x.Execute(
            It.IsAny<string>(),
            _connectionMock.Object,
            _transactionMock.Object,
            It.IsAny<Dictionary<string, object>>()))
        .Returns(1)
        .Throws(new Exception("Database error"));



    // Act + Assert

    Assert.Throws<Exception>(
        () => _repository.Save(sale)
    );



    // Assert

    _transactionMock.Verify(
        x => x.Rollback(),
        Times.Once
    );


    _transactionMock.Verify(
        x => x.Commit(),
        Times.Never
    );
}
[Fact]
public void GetById_Should_Return_Sale_With_Items()
{
    // Arrange

    var saleId = "01HSALE001";


    var readerSale = new Mock<IDataReader>();

    readerSale.SetupSequence(x => x.Read())
        .Returns(true)
        .Returns(false);


    readerSale.Setup(x => x.GetString(0))
        .Returns(saleId);

    readerSale.Setup(x => x.GetString(1))
        .Returns("client-001");

    readerSale.Setup(x => x.GetString(2))
        .Returns(SaleStatus.Started.ToString());

    readerSale.Setup(x => x.GetDateTime(3))
        .Returns(DateTime.UtcNow);

    readerSale.Setup(x => x.GetDateTime(4))
        .Returns(DateTime.UtcNow);



    var readerItems = new Mock<IDataReader>();

    readerItems.SetupSequence(x => x.Read())
        .Returns(true)
        .Returns(false);


    readerItems.Setup(x => x.GetString(0))
        .Returns("product-001");

    readerItems.Setup(x => x.GetInt32(1))
        .Returns(2);

    readerItems.Setup(x => x.GetDecimal(2))
        .Returns(50);

    readerItems.Setup(x => x.GetDateTime(3))
        .Returns(DateTime.UtcNow);

    readerItems.Setup(x => x.GetDateTime(4))
        .Returns(DateTime.UtcNow);



    _executorMock
        .SetupSequence(x => x.Query(
            It.IsAny<string>(),
            _connectionMock.Object,
            It.IsAny<Dictionary<string,object>>()))
        .Returns(readerSale.Object)
        .Returns(readerItems.Object);



    // Act

    var result = _repository.GetById(saleId);



    // Assert


    Assert.NotNull(result);

    Assert.Equal(
        saleId,
        result!.Id
    );


    Assert.Equal(
        "client-001",
        result.ClientId
    );


    Assert.Single(result.Items);


    var item = result.Items.First();


    Assert.Equal(
        "product-001",
        item.ProductId
    );


    Assert.Equal(
        2,
        item.Quantity
    );


    Assert.Equal(
        50,
        item.UnitPrice
    );
}
[Fact]
public void GetById_Should_Return_Null_When_Sale_Not_Found()
{
    // Arrange

    var saleId = "01HSALE999";


    var readerMock = new Mock<IDataReader>();


    readerMock
        .Setup(x => x.Read())
        .Returns(false);



    _executorMock
        .Setup(x => x.Query(
            It.IsAny<string>(),
            _connectionMock.Object,
            It.IsAny<Dictionary<string, object>>()))
        .Returns(readerMock.Object);



    // Act

    var result = _repository.GetById(saleId);



    // Assert


    Assert.Null(result);



    _executorMock.Verify(
        x => x.Query(
            It.IsAny<string>(),
            _connectionMock.Object,
            It.IsAny<Dictionary<string, object>>()),
        Times.Once
    );
}
[Fact]
public void Update_Should_Update_Sale_And_Items_And_Commit()
{
    // Arrange

    var sale = new Sale("client-001");


    sale.AddItem(
        "product-001",
        2,
        50
    );


    // Act

    _repository.Update(sale);



    // Assert


    _executorMock.Verify(
        x => x.Execute(
            It.IsAny<string>(),
            _connectionMock.Object,
            _transactionMock.Object,
            It.IsAny<Dictionary<string, object>>()
        ),
        Times.Exactly(3)
    );


    _transactionMock.Verify(
        x => x.Commit(),
        Times.Once
    );


    _transactionMock.Verify(
        x => x.Rollback(),
        Times.Never
    );
}
[Fact]
public void GetByProductId_Should_Return_Sales()
{
    // Arrange

    var readerMock = new Mock<IDataReader>();


    readerMock.SetupSequence(x => x.Read())
        .Returns(true)
        .Returns(false);


    readerMock.Setup(x => x.GetString(0))
        .Returns("sale-001");

    readerMock.Setup(x => x.GetString(1))
        .Returns("client-001");

    readerMock.Setup(x => x.GetString(2))
        .Returns(SaleStatus.Started.ToString());

    readerMock.Setup(x => x.GetDateTime(3))
        .Returns(DateTime.UtcNow);

    readerMock.Setup(x => x.GetDateTime(4))
        .Returns(DateTime.UtcNow);



    _executorMock
        .Setup(x => x.Query(
            It.IsAny<string>(),
            _connectionMock.Object,
            It.IsAny<Dictionary<string, object>>()))
        .Returns(readerMock.Object);



    // Act

    var result = _repository.GetByProductId(
        "product-001"
    );


    // Assert


    Assert.Single(result);

    Assert.Equal(
        "sale-001",
        result[0].Id
    );


    Assert.Equal(
        "client-001",
        result[0].ClientId
    );
}
[Fact]
public void GetByStatus_Should_Return_Sales()
{
    // Arrange

    var readerMock = new Mock<IDataReader>();


    readerMock.SetupSequence(x => x.Read())
        .Returns(true)
        .Returns(false);


    readerMock.Setup(x => x.GetString(0))
        .Returns("sale-002");

    readerMock.Setup(x => x.GetString(1))
        .Returns("client-002");

    readerMock.Setup(x => x.GetString(2))
        .Returns(SaleStatus.Progress.ToString());

    readerMock.Setup(x => x.GetDateTime(3))
        .Returns(DateTime.UtcNow);

    readerMock.Setup(x => x.GetDateTime(4))
        .Returns(DateTime.UtcNow);



    _executorMock
        .Setup(x => x.Query(
            It.IsAny<string>(),
            _connectionMock.Object,
            It.IsAny<Dictionary<string, object>>()))
        .Returns(readerMock.Object);



    // Act

    var result = _repository.GetByStatus(
        SaleStatus.Progress
    );



    // Assert


    Assert.Single(result);


    Assert.Equal(
        "sale-002",
        result[0].Id
    );


    Assert.Equal(
        SaleStatus.Progress,
        result[0].Status
    );
}
[Fact]
public void GetTotalSalesByProductAndStatus_Should_Return_Counts()
{
    // Arrange


    var readerMock = new Mock<IDataReader>();


    readerMock.SetupSequence(x => x.Read())
        .Returns(true)
        .Returns(true)
        .Returns(false);



    readerMock.SetupSequence(x => x.GetString(0))
        .Returns(SaleStatus.Started.ToString())
        .Returns(SaleStatus.Done.ToString());



    readerMock.SetupSequence(x => x.GetInt32(1))
        .Returns(3)
        .Returns(5);



    _executorMock
        .Setup(x => x.Query(
            It.IsAny<string>(),
            _connectionMock.Object,
            It.IsAny<Dictionary<string, object>>()))
        .Returns(readerMock.Object);



    // Act


    var result =
        _repository.GetTotalSalesByProductAndStatus(
            "product-001"
        );



    // Assert


    Assert.Equal(
        3,
        result[SaleStatus.Started]
    );


    Assert.Equal(
        5,
        result[SaleStatus.Done]
    );


    Assert.Equal(
        2,
        result.Count
    );
}
}