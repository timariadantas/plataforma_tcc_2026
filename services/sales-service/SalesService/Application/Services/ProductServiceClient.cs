using System.Text.Json;
using SalesService.Application.Repositories;
using SalesService.Application.DTO.Response;
using System.Net.Http.Json;
using SalesService.Domain.Exceptions;

namespace SalesService.Application.Services;

public class ProductServiceClient : IProductService
{
    private readonly HttpClient _http;
    private readonly ILogger<ProductServiceClient> _logger;

    public ProductServiceClient(HttpClient http, ILogger<ProductServiceClient> logger)
    {
        _http = http;
        _logger = logger;
    }

    private async Task<ProductServiceResponse> GetProduct(string productId)
    {
        try
        {


            var response = await _http.GetAsync(
                $"/internal/products/{productId}");

            _logger.LogInformation(
                "Product request status: {StatusCode} for {ProductId}",
                response.StatusCode,
                productId);

            // Produto encontrado
            if (response.IsSuccessStatusCode)
            {
                var product = await response.Content
                    .ReadFromJsonAsync<ApiResponse<ProductServiceResponse>>();

                if (product?.Data== null)
                    throw new ValidationException(
                        "Invalid product response");

                return product.Data;
            }

            // Produto realmente não encontrado
            if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
            {
                throw new NotFoundException(
                    "Product not found");
            }

            // Outros erros HTTP não significam que o produto não existe.
            response.EnsureSuccessStatusCode();

            throw new ValidationException(
                "Invalid product response");
        }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(
                ex,
                "Timeout calling Product Service for product {ProductId}",
                productId);

            throw new DependencyTimeoutException(
                "Product Service did not respond within the timeout.");
        }catch (HttpRequestException ex)
        {
        _logger.LogError(
            ex,
            "Product Service unavailable for product {ProductId}",
            productId);

        throw new DependencyUnavailableException(
            "Product Service is unavailable.");
        }   
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

        try
        {
            var response = await _http.PatchAsJsonAsync(
            $"/internal/products/{productId}/decrease-stock",
            body
        );

            _logger.LogInformation(
                "Decrease stock status: {StatusCode} for product {ProductId}",
                response.StatusCode,
                productId
            );

            // Estoque reduzido com sucesso
            if (response.IsSuccessStatusCode)
                return;

            // Produto não existe
            if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
            {
                throw new NotFoundException(
                    "Product not found"
                );
            }

            // Conflito, por exemplo estoque insuficiente
            if (response.StatusCode == System.Net.HttpStatusCode.Conflict)
            {
                throw new ConflictException(
                    "Insufficient stock"
                );
            }

            // Qualquer outro erro não deve ser convertido
            // em ValidationException.
            response.EnsureSuccessStatusCode();

        }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(
            ex,
            "Timeout calling Product Service to decrease stock for product {ProductId}",
            productId
        );

            throw new DependencyTimeoutException(
                "Product Service did not respond within the timeout."
            );
        }catch (HttpRequestException ex)
        {
            _logger.LogError(
                ex,
                "Product Service unavailable for product {ProductId}",
                productId);

            throw new DependencyUnavailableException(
                "Product Service is unavailable.");
    }
}
    public async Task IncreaseStock(string productId, int quantity)
    {
        var body = new
        {
            quantity
        };

        try
        {
            var response = await _http.PatchAsJsonAsync(
                $"/internal/products/{productId}/increase-stock",
                body
            );

            _logger.LogInformation(
                "Increase stock status: {StatusCode} for product {ProductId}",
                response.StatusCode,
                productId
            );

            // Estoque aumentado com sucesso
            if (response.IsSuccessStatusCode)
                return;

            // Produto não existe
            if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
            {
                throw new NotFoundException(
                    "Product not found"
                );
            }

            // Qualquer outro erro HTTP não deve ser
            // convertido em ProductNotFoundException.
            response.EnsureSuccessStatusCode();
        }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(
                ex,
                "Timeout calling Product Service to increase stock for product {ProductId}",
                productId
            );

            throw new DependencyTimeoutException(
                "Product Service did not respond within the timeout."
            );
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError(
                ex,
                "Product Service unavailable while increasing stock for product {ProductId}",
                productId
            );

            throw new DependencyUnavailableException(
                "Product Service is unavailable."
            );
        }
    }
}
