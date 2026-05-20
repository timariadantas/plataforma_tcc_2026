namespace SalesService.Application.DTO.Response;

public class ApiResponse<T>
{
    public string Message{get;set;} = string.Empty;
    public DateTime Timestamp { get; set; }
        = DateTime.UtcNow;

    public long Elapsed { get; set; }

    public T? Data { get; set; }

    public string? Error { get; set; }
}
