namespace SalesService.Application.Repositories;

public interface IClientService
{
    Task<bool> ClientExists(string clientId);
}
