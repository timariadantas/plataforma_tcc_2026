using System.Collections.Generic;

namespace SalesService.Application.DTO.Response;

public class SaleResponse
{
    public string Id {get; set;}
    public string ClientId {get; set;}
    public string Status {get; set;}

    public List<SaleItemResponse> Items {get;set;}
}
