using System.Text.Json;
using CurrencyService.Domain;

namespace CurrencyService.Application.Services;

public class CurrencyService : ICurrencyService
{
    private readonly HttpClient _httpClient;
    private static List<CurrencyRate>? _cache;
    private static DateTime _lastUpdate;

    public CurrencyService (HttpClient httpClient) // DI
    {
        _httpClient = httpClient;

    }

    public async Task <List<CurrencyRate>> GetAllAsync()
    {
        if (_cache != null && _lastUpdate.Date == DateTime.UtcNow.Date)
        {
            return _cache;
        }

        var url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,GBP-BRL,CNY-BRL";

        var response = await _httpClient.GetAsync(url);
        if (!response.IsSuccessStatusCode)
{
    return new List<CurrencyRate>
    {
        new CurrencyRate
        {
            Code = "USD",
            Value = 5.40m,
            CreatedAt = DateTime.UtcNow
        },

        new CurrencyRate
        {
            Code = "EUR",
            Value = 6.20m,
            CreatedAt = DateTime.UtcNow
        },

        new CurrencyRate
        {
            Code = "GBP",
            Value = 7.10m,
            CreatedAt = DateTime.UtcNow
        },

        new CurrencyRate
        {
            Code = "CNY",
            Value = 0.76m,
            CreatedAt = DateTime.UtcNow
        }
    };
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

        return rates;
    }

    public async Task<CurrencyRate?> GetByCodeAsync(string code)
    {
        var rates = await GetAllAsync();
        return rates.FirstOrDefault(x => 
        x.Code.Equals(code, StringComparison.OrdinalIgnoreCase));
    }

    private CurrencyRate CreateRate(
        JsonElement root, 
        string propertyName,
        string code
    )
    {
        var currency = root.GetProperty(propertyName);

        var value = decimal.Parse(
            currency.GetProperty("bid").GetString()!);

        return new CurrencyRate
        {
            Code = code,
            Value = value,
            CreatedAt = DateTime.UtcNow
        };
    }

}