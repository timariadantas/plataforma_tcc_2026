using System.Text.Json;
using SalesService.Application.Repositories;
using SalesService.Application.DTO.Response;
using System.Net.Http.Json;

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

   public async Task<bool> ProductsExists(string productId)
   {
      var response = await _http.GetAsync($"/products/{productId}");
      return response.IsSuccessStatusCode;
   }
   public async Task<int> GetStock(string productId)
{
    var response = await _http.GetAsync($"/products/{productId}");

    if (!response.IsSuccessStatusCode)
        throw new Exception("Product not found");

    var json = await response.Content.ReadAsStringAsync();

    _logger.LogInformation("Product JSON: {Json}", json);

    var product = JsonSerializer.Deserialize<ProductServiceResponse>(
        json,
        new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        });

    if (product == null)
        throw new Exception("Invalid product response");

    return product.Quantity;
}
   public async Task<decimal> GetPrice(string productId)
   {
      var response = await _http.GetAsync($"/products/{productId}");

      if (!response.IsSuccessStatusCode)
         throw new Exception("Product not found");

      var json = await response.Content.ReadAsStringAsync();

      _logger.LogInformation("Product JSON: {Json}", json);
      var product = JsonSerializer.Deserialize<ProductServiceResponse>(
         json,
      new JsonSerializerOptions
         {
            PropertyNameCaseInsensitive = true
         });

      if (product == null)
         throw new Exception("Invalid product response");
      
      return product.Price;
   }

   public async Task DecreaseStock(string productId, int quantity)
   {
      var body = new
      {
         quantity = quantity
      };

      var response = await _http.PatchAsJsonAsync($"/products/{productId}/decrease-stock", body);

      if (!response.IsSuccessStatusCode)
         throw new Exception("Error decreasing stock");
   }
}


