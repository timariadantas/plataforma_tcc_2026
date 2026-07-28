using System.Collections.Generic;

namespace SalesService.Application.DTO.Response;

public class SaleResponse
{
    public string Id {get; set;} = string.Empty;
    public string clientId {get; set;} = string.Empty;
    public string Status {get; set;} = string.Empty;

    public List<SaleItemResponse> Items {get;set;} = new();
}
