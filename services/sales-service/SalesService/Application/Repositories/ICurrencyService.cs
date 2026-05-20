namespace SalesService.Application.Repositories;

public interface ICurrencyService
{
    Task <Dictionary<string, decimal>> GetAllRates();
}
