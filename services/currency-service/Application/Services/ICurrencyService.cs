using CurrencyService.Domain;

namespace CurrencyService.Application.Services;

public interface ICurrencyService
{
    Task <List<CurrencyRate>> GetAllAsync ();
    Task <CurrencyRate?> GetByCodeAsync(string code);
}