using SalesService.Domain.Entities;

namespace SalesService.Application.Repositories;
public interface ISaleService
{
    Sale CreateSale(string clientId);
    Sale GetById(string saleId);
    void AddItem(string saleId, string productId, int quantity);
    void FinishSale(string saleId);
    void CancelSale(string saleId);
}