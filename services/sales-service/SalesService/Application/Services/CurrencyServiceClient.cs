using System.Net.Http.Json;
using SalesService.Application.DTO.Response;
using SalesService.Application.Repositories;

namespace SalesService.Application.Services;

public class CurrencyServiceClient : ICurrencyService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<CurrencyServiceClient> _logger;

    public CurrencyServiceClient(
        HttpClient httpClient,
        ILogger<CurrencyServiceClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<Dictionary<string, decimal>> GetAllRates()
    {
        _logger.LogInformation(
            "Requesting currency rates from Currency Service.");

        HttpResponseMessage response;

        try
        {
            response = await _httpClient.GetAsync("/currency");
        }
        catch (TaskCanceledException ex)
        {
            _logger.LogWarning(
                ex,
                "Currency Service request timed out. " +
                "Sale will continue without currency conversion.");

            return new Dictionary<string, decimal>();
        }
        catch (HttpRequestException ex)
        {
            _logger.LogWarning(
                ex,
                "Currency Service is unavailable. " +
                "Sale will continue without currency conversion.");

            return new Dictionary<string, decimal>();
        }

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogWarning(
                "Currency Service returned HTTP {StatusCode}. " +
                "Sale will continue without currency conversion.",
                response.StatusCode);

            return new Dictionary<string, decimal>();
        }

        var result =
            await response.Content
                .ReadFromJsonAsync<CurrencyServiceResponse>();

        if (result?.Data == null)
        {
            _logger.LogWarning(
                "Currency Service returned an invalid response. " +
                "Sale will continue without currency conversion.");

            return new Dictionary<string, decimal>();
        }

        var rates = result.Data.ToDictionary(
            currency => currency.Code,
            currency => currency.Value);

        _logger.LogInformation(
            "Currency rates received successfully. Count: {Count}.",
            rates.Count);

        return rates;
    }
}