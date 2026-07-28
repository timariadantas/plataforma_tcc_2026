using SalesService.Domain.Entities;
using SalesService.Domain.Enums;
using SalesService.Domain.Exceptions;

namespace SalesServices.Tests.Domain.Entities;

public class SaleTests
{
    [Fact]
    public void Should_Create_Sale()
    {
        var sale = new Sale("client-1");

        Assert.Equal("client-1", sale.ClientId);
        Assert.Equal(SaleStatus.Started, sale.Status);
        Assert.Empty(sale.Items);
    }

    [Fact]
    public void Should_Add_Item()
    {
        var sale = new Sale("client");

        sale.AddItem(
            "product",
            2,
            20m
        );

        Assert.Single(sale.Items);
        Assert.Equal(SaleStatus.Progress, sale.Status);
    }

    [Fact]
    public void Should_Calculate_Total()
    {
        var sale = new Sale("client");

        sale.AddItem("p1", 2, 10m);
        sale.AddItem("p2", 3, 20m);

        Assert.Equal(80m, sale.Total);
    }

    [Fact]
    public void Should_Update_Item()
    {
        var sale = new Sale("client");

        sale.AddItem("p1", 2, 10m);

        sale.UpdateItem("p1", 5);

        Assert.Equal(50m, sale.Total);
    }

    [Fact]
    public void Should_Finish_Sale()
    {
        var sale = new Sale("client");

        sale.AddItem("p1", 1, 10m);

        sale.Finish();

        Assert.Equal(SaleStatus.Done, sale.Status);
    }

    [Fact]
    public void Should_Cancel_Sale()
    {
        var sale = new Sale("client");

        sale.Cancel();

        Assert.Equal(SaleStatus.Canceled, sale.Status);
    }

    [Fact]
    public void Should_Rehydrate_Sale()
    {
        var now = DateTime.UtcNow;

        var sale = Sale.Rehydrate(
            "sale-id",
            "client-id",
            SaleStatus.Done,
            now,
            now
        );

        Assert.Equal("sale-id", sale.Id);
        Assert.Equal("client-id", sale.ClientId);
        Assert.Equal(SaleStatus.Done, sale.Status);
    }

    [Fact]
    public void Should_Load_Item()
    {
        var sale = new Sale("client");

        var now = DateTime.UtcNow;

        sale.LoadItem(
            "product",
            2,
            20m,
            now,
            now
        );

        Assert.Single(sale.Items);
    }

    [Fact]
    public void Should_Throw_When_Client_Is_Empty()
    {
        Assert.Throws<ValidationException>(() =>
        {
            new Sale("");
        });
    }

    [Fact]
    public void Should_Throw_When_Quantity_Is_Invalid()
    {
        var sale = new Sale("client");

        Assert.Throws<ValidationException>(() =>
        {
            sale.AddItem(
                "product",
                0,
                10m
            );
        });
    }

    [Fact]
    public void Should_Throw_When_Finish_Without_Items()
    {
        var sale = new Sale("client");

        Assert.Throws<BusinessException>(() =>
        {
            sale.Finish();
        });
    }

    [Fact]
    public void Should_Throw_When_Cancel_After_Finish()
    {
        var sale = new Sale("client");

        sale.AddItem("p1", 1, 10m);

        sale.Finish();

        Assert.Throws<BusinessException>(() =>
        {
            sale.Cancel();
        });
    }

    [Fact]
    public void Should_Throw_When_Update_Item_Not_Found()
    {
        var sale = new Sale("client");

        Assert.Throws<BusinessException>(() =>
        {
            sale.UpdateItem("product", 5);
        });
    }

    [Fact]
    public void Should_Not_Allow_Add_Item_After_Finish()
    {
        var sale = new Sale("client");

        sale.AddItem("p1", 1, 10m);

        sale.Finish();

        Assert.Throws<BusinessException>(() =>
        {
            sale.AddItem("p2", 1, 20m);
        });
    }

    [Fact]
    public void Should_Not_Allow_Update_Item_After_Cancel()
    {
        var sale = new Sale("client");

        sale.AddItem("p1", 1, 10m);

        sale.Cancel();

        Assert.Throws<BusinessException>(() =>
        {
            sale.UpdateItem("p1", 3);
        });
    }
}
