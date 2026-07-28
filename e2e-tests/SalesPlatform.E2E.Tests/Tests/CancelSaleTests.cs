using Newtonsoft.Json.Linq;
using Xunit;
using SalesPlatform.E2E.Tests.Helpers;

namespace SalesPlatform.E2E.Tests.Tests;

public class CancelSaleTests
{
    private readonly ApiClient _api = new();

    [Fact]
    public async Task Should_Cancel_Sale()
    {
        // cria cliente
        var email = await _api.CreateClient();

        // login
        var token = await _api.Login(email);
        _api.SetToken(token);

        // cria produto
        var productId = await _api.CreateProduct();

        // cria venda
        var saleId = await _api.CreateSale();

        // adiciona item
        await _api.AddItem(
            saleId,
            productId);

        // cancela venda
        await _api.CancelSale(saleId);

        // consulta venda
        JObject sale = await _api.GetSale(saleId);

        Assert.NotNull(sale);

        var status =
            sale["data"]?["status"]?.ToString()
            ?? sale["status"]?.ToString();

        Assert.Equal("Canceled", status);
    }
}