using System.Text.Json;
using SalesService.Application.Repositories;
using SalesService.Application.DTO.Response;
using System.Net.Http.Json;
using SalesService.Domain.Exceptions;

namespace SalesService.Application.Services;

public class ProductServiceClient : IProductService
{
   private readonly HttpClient _http;
   private readonly ILogger <ProductServiceClient>_logger;

   public ProductServiceClient (HttpClient http , ILogger<ProductServiceClient>logger)
   {
      _http = http;
      _logger = logger;
   }

   private async Task<ProductServiceResponse> GetProduct(string productId)
    {
        var response = await _http.GetAsync($"/internal/products/{productId}");

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogWarning("Product not found: {ProductId}", productId);
            throw new NotFoundException("Product not found");
        }

        var json = await response.Content.ReadAsStringAsync();

        _logger.LogInformation("Product JSON: {Json}", json);

        var product = JsonSerializer.Deserialize<ProductServiceResponse>(
            json,
            new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

        if (product == null)
            throw new ValidationException ("Invalid product response");

        return product;
    }


    public async Task<int> GetStock(string productId)
    {
        var product = await GetProduct(productId);
        return product.Quantity;
    }

 
    public async Task<decimal> GetPrice(string productId)
    {
        var product = await GetProduct(productId);
        return product.Price;
    }

    public async Task DecreaseStock(string productId, int quantity)
    {
        var body = new
        {
            quantity
        };

        var response = await _http.PatchAsJsonAsync(
            $"/internal/products/{productId}/decrease-stock",
            body
        );

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogError(
                "Error decreasing stock for product {ProductId}",
                productId
            );

            throw new ValidationException ("Error decreasing stock");
        }
    }

  
}