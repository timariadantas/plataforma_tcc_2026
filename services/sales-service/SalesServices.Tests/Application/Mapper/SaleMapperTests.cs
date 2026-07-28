using Xunit;
using SalesService.Application.Mapper;
using SalesService.Domain.Entities;
using SalesService.Domain.Enums;

namespace SalesServices.Tests.Application.Mapper;

public class SaleMapperTests
{
    [Fact]
public void ToResponse_Should_Map_Basic_Properties()
{
    // Arrange

    var sale = new Sale("client-001");

    // Act

    var response = SaleMapper.ToResponse(sale);

    // Assert

    Assert.Equal(
        sale.Id,
        response.Id);

    Assert.Equal(
        sale.ClientId,
        response.clientId);

    Assert.Equal(
        SaleStatus.Started.ToString(),
        response.Status);
}
[Fact]
public void ToResponse_Should_Map_Items()
{
    // Arrange

    var sale = new Sale("client-001");

    sale.AddItem(
        "product-001",
        3,
        100);

    sale.AddItem(
        "product-002",
        2,
        50);

    // Act

    var response = SaleMapper.ToResponse(sale);

    // Assert

    Assert.Equal(
        2,
        response.Items.Count);

    Assert.Equal(
        "product-001",
        response.Items[0].ProductId);

    Assert.Equal(
        3,
        response.Items[0].Quantity);

    Assert.Equal(
        "product-002",
        response.Items[1].ProductId);

    Assert.Equal(
        2,
        response.Items[1].Quantity);
}

[Fact]
public void ToResponse_Should_Return_Empty_List_When_Sale_Has_No_Items()
{
    // Arrange

    var sale = new Sale("client-001");

    // Act

    var response = SaleMapper.ToResponse(sale);

    // Assert

    Assert.NotNull(response.Items);

    Assert.Empty(response.Items);
}
}
