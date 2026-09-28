using System.Globalization;
using System.Text.Json;
using CurrencyService.Domain;
using CurrencyService.Domain.Exceptions;

namespace CurrencyService.Application.Services;

public class CurrencyService : ICurrencyService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<CurrencyService> _logger;
    private static List<CurrencyRate>? _cache;
    private static DateTime _lastUpdate;

    public CurrencyService (HttpClient httpClient, ILogger<CurrencyService> logger) // DI
    {
        _httpClient = httpClient;
        _logger = logger;

    }

    public async Task <List<CurrencyRate>> GetAllAsync()
    {
        _logger.LogInformation(
            "Getting all currency rates.");

        if (_cache != null && _lastUpdate.Date == DateTime.UtcNow.Date)
        {
            _logger.LogInformation(
                "Currency rates retrieved from cache. Last update: {LastUpdate}",
            _lastUpdate);

            return _cache;
        }

        var url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,GBP-BRL,CNY-BRL";

        _logger.LogInformation( "Requesting currency rates from external provider.");

        HttpResponseMessage response;

        try
        {
            response = await _httpClient.GetAsync(url);
        }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(
            ex,
                "Currency provider request timed out.");

            throw new CurrencyServiceUnavailableException(
                "Currency provider timeout.",
                ex);
        }
        catch (HttpRequestException ex)
        {
             _logger.LogError(
            ex,
                "Currency provider request failed.");

            throw new CurrencyServiceUnavailableException(
                "Currency provider is unavailable.",
                ex);
        }

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogError(
                "Currency provider returned HTTP status code {StatusCode}.",
            response.StatusCode); 

            throw new CurrencyServiceUnavailableException(
                "Currency provider is unavailable.");
        }

        var json = await response.Content.ReadAsStringAsync();

        using var document = JsonDocument.Parse(json);

        var root = document.RootElement;

        var rates = new List<CurrencyRate>
        {
            CreateRate(root, "USDBRL", "USD"),
            CreateRate(root, "EURBRL", "EUR"),
            CreateRate(root, "GBPBRL", "GBP"),
            CreateRate(root, "CNYBRL", "CNY"),

        };

        _cache = rates;
        _lastUpdate = DateTime.UtcNow;

        _logger.LogInformation(
            "Currency rates successfully updated in cache at {LastUpdate}.",
        _lastUpdate);

        return rates;
    }

    public async Task<CurrencyRate?> GetByCodeAsync(string code)
    {
        _logger.LogInformation(
            "Getting currency rate for code {CurrencyCode}.", code);

        var rates = await GetAllAsync();
        
        var rate = rates.FirstOrDefault(x => 
        x.Code.Equals(code, StringComparison.OrdinalIgnoreCase));

        if (rate == null) 
        { 
            _logger.LogWarning( "Currency rate not found for code {CurrencyCode}.", code); 
        }

        else 
        { 
            _logger.LogInformation( "Currency rate found for code {CurrencyCode}.", code); 
        } 
        
        return rate;
        
        
    }
        

    

    private CurrencyRate CreateRate(
        JsonElement root, 
        string propertyName,
        string code
    )
    {
        var currency = root.GetProperty(propertyName);

        var value = decimal.Parse(
            currency.GetProperty("bid").GetString()!,
            CultureInfo.InvariantCulture);

        return new CurrencyRate
        {
            Code = code,
            Value = value,
            CreatedAt = DateTime.UtcNow
        };
    }

}