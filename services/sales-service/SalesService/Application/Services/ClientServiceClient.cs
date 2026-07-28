using System.Net.Http.Json;
using SalesService.Application.Repositories;

namespace SalesService.Application.Services;
public class ClientServiceClient : IClientService
{
    private readonly HttpClient _http;
    private readonly ILogger<ClientServiceClient> _logger;

    public ClientServiceClient(HttpClient http, ILogger<ClientServiceClient> logger)
    {
        _http = http;
        _logger = logger;
    }

    public async Task<bool> ClientExists(string clientId)
    {
        var response = await _http.GetAsync($"/internal/clients/{clientId}");

        _logger.LogInformation("Client check status: {Status}", response.StatusCode);
        
        return response.IsSuccessStatusCode;
    }
}
