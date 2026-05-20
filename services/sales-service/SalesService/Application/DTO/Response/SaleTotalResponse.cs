namespace SalesService.Application.DTO.Response;

public class SaleTotalResponse
{
    public decimal TotalBRL {get;set;}
    public Dictionary<string, decimal> Coins {get;set;} = new();
}
