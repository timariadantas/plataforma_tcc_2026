using SalesService.Domain.Entities;
using SalesService.Domain.Enums;
using SalesService.Application.DTO.Response;

namespace SalesService.Application.Repositories;
public interface ISaleService
{
    Sale CreateSale(string clientId);
    Sale GetById(string saleId);
    Task AddItem(string saleId, string productId, int quantity);
    Task<SaleTotalResponse> FinishSale(string saleId);
    void CancelSale(string saleId);
    Task UpdateItem(string saleId, string productId, int quantity);
    Task<List<Sale>> GetByProductId(string productId);

    Task<List<Sale>> GetByStatus(string status);

    Task<Dictionary<SaleStatus, int>> GetTotalSalesByProductAndStatus(string productId);
}