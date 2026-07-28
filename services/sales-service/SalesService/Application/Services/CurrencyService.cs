using SalesService.Application.Repositories;
namespace SalesService.Application.Services
{
    public class CurrencyService : ICurrencyService
    {
        public Task<Dictionary<string, decimal>> GetAllRates()
        {
            var rates = new Dictionary<string, decimal>
            {
                {"USD" , 5.10m},
                {"EUR" , 5.50m},
                {"BRL" , 1m}

            };

            return Task.FromResult(rates);
        }
    }
}
