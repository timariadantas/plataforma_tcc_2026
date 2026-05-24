using SalesService.Domain.Entities;
using SalesService.Domain.Enums;

namespace SalesService.Domain.Repositories;
public interface ISaleRepository
{
    void Save(Sale sale);
    Sale? GetById(string id);
    void Update(Sale sale);
    List<Sale> GetByProductId(string productId);
    List<Sale> GetByStatus(SaleStatus status);
    Dictionary<SaleStatus, int> GetTotalSalesByProductAndStatus(string productId);

   
}

