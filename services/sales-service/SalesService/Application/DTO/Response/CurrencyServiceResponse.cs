namespace SalesService.Application.DTO.Response;

public class CurrencyServiceResponse
{
    public string Message { get; set; } = string.Empty;

    public DateTime Timestamp { get; set; }

    public long Elapsed { get; set; }

    public List<CurrencyRateResponse>? Data { get; set; }

    public string? Error { get; set; }
}

public class CurrencyRateResponse
{
    public string Code { get; set; } = string.Empty;

    public decimal Value { get; set; }

    public DateTime CreatedAt { get; set; }
}