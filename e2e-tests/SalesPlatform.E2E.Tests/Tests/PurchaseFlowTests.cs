using Newtonsoft.Json.Linq;
using Xunit;
using SalesPlatform.E2E.Tests.Helpers;

namespace SalesPlatform.E2E.Tests.Tests;

public class PurchaseFlowTests
{
    private readonly ApiClient _api = new();

    [Fact]
    public async Task Should_Create_Complete_Sale_Flow()
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

        // finaliza venda
        await _api.FinishSale(saleId);

        // consulta venda
        JObject sale =
            await _api.GetSale(saleId);

        Assert.NotNull(sale);
        Assert.Equal(
            saleId,
            sale["data"]?["id"]?.ToString() ??
                sale["id"]?.ToString());

        Assert.NotNull(
            sale["data"]?["items"] ??
            sale["items"]);
    }
}