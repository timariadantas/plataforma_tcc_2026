using Microsoft.AspNetCore.Mvc;
using CurrencyService.Application.Services;

namespace CurrencyService.API.Controller;

[ApiController]
[Route("currency")]

public class CurrencyController : ControllerBase
{
    private readonly ICurrencyService _currencyService;

    public CurrencyController(ICurrencyService currencyService)
    {
        _currencyService = currencyService;
    }

    [HttpGet]
    public async Task <IActionResult> GetAll()
    {
        var rates = await _currencyService.GetAllAsync();

        return Ok(new
        {
            message = "Currencies found",
            timestamp = DateTime.UtcNow,
            elapsed = 0,
            data = rates
        });
    }
    [HttpGet("{code}")]
    public async Task <IActionResult> GetByCode(string code)
        {
            var rate = await _currencyService.GetByCodeAsync(code);

            if (rate == null)
        {
            return NotFound(new
            {
                 message = "Currency not found",
                timestamp = DateTime.UtcNow,
                elapsed = 0,
                error = "Invalid currency code"
            });
        }
        return Ok(new
        {
            message = "Currency found",
            timestamp = DateTime.UtcNow,
            elapsed = 0,
            data = rate
        });

    }
}
    
