public interface IProductServiceFake
{
    bool ProductsExists(string productId);
    int GetStock(string productId);
}