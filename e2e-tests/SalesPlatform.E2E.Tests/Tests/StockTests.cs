using Newtonsoft.Json.Linq;
using Xunit;
using SalesPlatform.E2E.Tests.Helpers;

namespace SalesPlatform.E2E.Tests.Tests;

public class StockTests
{
    private readonly ApiClient _api = new();

    [Fact]
    public async Task Should_Decrease_Product_Stock_After_Finish_Sale()
    {
        // cria cliente
        var email = await _api.CreateClient();

        // login
        var token = await _api.Login(email);
        _api.SetToken(token);

        // cria produto (estoque = 10)
        var productId = await _api.CreateProduct();

        // cria venda
        var saleId = await _api.CreateSale();

        // adiciona 2 unidades
        await _api.AddItem(
            saleId,
            productId);

        // finaliza venda
        await _api.FinishSale(saleId);

        // consulta produto
        JObject product =
            await _api.GetProduct(productId);

        Assert.NotNull(product);

        var quantity =
            product["quantity"]?.Value<int>()
            ?? product["data"]?["quantity"]?.Value<int>();

        Assert.Equal(8, quantity);
    }
}