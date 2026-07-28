using SalesService.Domain.Entities;
using SalesService.Domain.Exceptions;

namespace SalesServices.Tests.Domain.Entities;

public class SaleItemTests
{
    [Fact]
    public void Should_Create_SaleItem()
    {
        var item = new SaleItem(
            "sale-1",
            "product-1",
            2,
            50m
        );

        Assert.Equal("sale-1", item.SaleId);
        Assert.Equal("product-1", item.ProductId);
        Assert.Equal(2, item.Quantity);
        Assert.Equal(50m, item.UnitPrice);
        Assert.Equal(100m, item.Total);
    }

    [Fact]
    public void Should_Update_Quantity()
    {
        var item = new SaleItem(
            "sale-1",
            "product-1",
            2,
            50m
        );

        item.UpdateQuantity(5);

        Assert.Equal(5, item.Quantity);
        Assert.Equal(250m, item.Total);
    }

    [Fact]
    public void Should_Rehydrate_Item()
    {
        var now = DateTime.UtcNow;

        var item = SaleItem.Rehydrate(
            "sale",
            "product",
            3,
            10m,
            now,
            now
        );

        Assert.Equal("sale", item.SaleId);
        Assert.Equal("product", item.ProductId);
        Assert.Equal(3, item.Quantity);
        Assert.Equal(10m, item.UnitPrice);
        Assert.Equal(now, item.CreatedAt);
    }

    [Fact]
    public void Should_Throw_When_Product_Is_Empty()
    {
        Assert.Throws<ValidationException>(() =>
        {
            new SaleItem(
                "sale",
                "",
                1,
                10m
            );
        });
    }

    [Fact]
    public void Should_Throw_When_Quantity_Is_Invalid()
    {
        Assert.Throws<ValidationException>(() =>
        {
            new SaleItem(
                "sale",
                "product",
                0,
                10m
            );
        });
    }

    [Fact]
    public void Should_Throw_When_Updating_With_Invalid_Quantity()
    {
        var item = new SaleItem(
            "sale",
            "product",
            2,
            10m
        );

        Assert.Throws<ValidationException>(() =>
        {
            item.UpdateQuantity(0);
        });
    }
}