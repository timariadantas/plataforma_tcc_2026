using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using CurrencyService.Domain;
using CurrencyService.Application.Services;
using CurrencyService.Application.DTO.Response;



namespace CurrencyService.API.Controller;

[ApiController]
[Route("currency")]

public class CurrencyController : ControllerBase
{
    private readonly ICurrencyService _currencyService;
    private readonly ILogger<CurrencyController> _logger;

    public CurrencyController(ICurrencyService currencyService, ILogger<CurrencyController> logger)
    {
        _currencyService = currencyService;
        _logger = logger;
    }

    [HttpGet]
    public async Task <IActionResult> GetAll()

    {
        var start = Stopwatch.GetTimestamp();
         _logger.LogInformation(
            "GET /currency started.");

        var rates = await _currencyService.GetAllAsync();
        var elapsed = (long)Stopwatch.GetElapsedTime(start).TotalMilliseconds;

        _logger.LogInformation( "GET /currency completed in {Elapsed} ms.", elapsed);

        return Ok(new ApiResponse<List<CurrencyRate>>
        {
            Message = "Currencies found",
            Timestamp = DateTime.UtcNow,
            Elapsed = elapsed,
            Data = rates
        });
    }
    [HttpGet("{code}")]
    public async Task <IActionResult> GetByCode(string code)
        {
            var start = Stopwatch.GetTimestamp();
            
            _logger.LogInformation(
                "GET /currency/{CurrencyCode} started.", code);

            var rate = await _currencyService.GetByCodeAsync(code);

            var elapsed = (long)Stopwatch.GetElapsedTime(start).TotalMilliseconds;

            if (rate == null)
            {
                _logger.LogWarning( "GET /currency/{CurrencyCode} returned not found.", code);
                return NotFound(new ApiResponse<CurrencyRate>
                {
                    Message = "Currency not found",
                    Timestamp = DateTime.UtcNow,
                    Elapsed = elapsed,
                    Error = "Invalid currency code"
                });
        }
        _logger.LogInformation( "GET /currency/{CurrencyCode} completed in {Elapsed} ms.", code, elapsed);
        
        return Ok(new ApiResponse<CurrencyRate>
        {
            Message = "Currency found",
            Timestamp = DateTime.UtcNow,
            Elapsed = elapsed,
            Data = rate
        });

    }
}
    
