using System.Linq;
using SalesService.Application.DTO.Response;
using SalesService.Domain.Entities;

namespace SalesService.Application.Mapper;

public static class SaleMapper
{
public static SaleResponse ToResponse (Sale sale)
{
    return new SaleResponse
    {
        Id = sale.Id,
        clientId = sale.ClientId,
        Status = sale.Status.ToString(),
        Items = sale.Items.Select(item => new SaleItemResponse
        {
            ProductId = item.ProductId,
            Quantity = item.Quantity

        }).ToList()
    };
}}