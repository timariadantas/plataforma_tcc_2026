using SalesService.Application.DTO.Response;
using SalesService.Application.Repositories;

namespace SalesService.Application.Services;

public class CurrencyServiceClient : ICurrencyService
{
    private readonly HttpClient _http;
    public CurrencyServiceClient(HttpClient http)
    {
        _http = http;
    }

    public async Task <Dictionary<string, decimal>> GetAllRates()
    {
        var response = await _http.GetFromJsonAsync<CurrencyApiResponse>("/currency");

        if (response == null)
            throw new Exception("Currency service unavailable");

        return response.Data.ToDictionary(
            x => x.Code,
            x => x.Value
        );

    }

}

