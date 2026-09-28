using System.Text.Json.Serialization;

namespace CurrencyService.Application.DTO.Response;

public class ApiResponse<T>
{
    public string Message { get; set; } = string.Empty;

    public DateTime Timestamp { get; set; }

    public long Elapsed { get; set; }

    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public T? Data { get; set; }

    [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
    public string? Error { get; set; }
}