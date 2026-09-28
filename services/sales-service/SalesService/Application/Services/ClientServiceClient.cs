using SalesService.Application.Repositories;
using SalesService.Domain.Exceptions;

namespace SalesService.Application.Services;

public class ClientServiceClient : IClientService
{
    private readonly HttpClient _http;
    private readonly ILogger<ClientServiceClient> _logger;

    public ClientServiceClient(
        HttpClient http,
        ILogger<ClientServiceClient> logger)
    {
        _http = http;
        _logger = logger;
    }

    public async Task<bool> ClientExists(string clientId)
    {
        try
        {
            var response = await _http.GetAsync(
                $"/internal/clients/{clientId}");

            _logger.LogInformation(
                "Client check status: {StatusCode} for {ClientId}",
                response.StatusCode,
                clientId);

            // Cliente existe
            if (response.IsSuccessStatusCode)
                return true;

            // Cliente realmente não existe
            if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
                return false;

            // Qualquer outro erro não significa "cliente não existe".
            // Deixamos a exceção chegar ao middleware global.
            response.EnsureSuccessStatusCode();

            return false;
    }
        catch (TaskCanceledException ex)
        {
            _logger.LogError(
            ex,
            "Timeout calling Client Service for client {ClientId}",
            clientId);

        throw new DependencyTimeoutException(
            "Client Service did not respond within the timeout.");
        }
}

}