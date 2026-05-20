namespace SalesService.Application.Repositories;
public interface IProductService

{
    Task <bool> ProductsExists(string productId);
    Task <int> GetStock(string productId);
    Task<decimal> GetPrice(string productId);
    Task DecreaseStock(string productId, int quantity);
}