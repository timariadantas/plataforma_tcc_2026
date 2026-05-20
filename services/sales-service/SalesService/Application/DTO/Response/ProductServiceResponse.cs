namespace SalesService.Application.DTO.Response;

public class ProductServiceResponse
{
    public string Id {get; set;} = string.Empty;
    public decimal Price {get; set;}
    public int Quantity{ get; set;}
}
