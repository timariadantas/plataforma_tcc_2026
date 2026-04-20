namespace SalesService.Application.Services;

public class ProductServiceFake : IProductServiceFake
{
    public bool ProductsExists (string productId)
    {
        return !string.IsNullOrEmpty(productId);
    }

    public int GetStock(string productId)
    {
        return 10;
    }
}

