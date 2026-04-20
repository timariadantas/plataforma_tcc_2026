using SalesService.Domain.Entities;
using SalesService.Domain.Exceptions;
using SalesService.Domain.Repositories;


namespace SalesService.Application.Services;

public class SaleService : ISaleService   
{
   private readonly ISaleRepository _repository;
   private readonly IProductServiceFake _productServiceFake; 

   public SaleService(
       ISaleRepository repository,
       IProductServiceFake productServiceFake
   )
    {
        _repository = repository;
        _productServiceFake = productServiceFake;
    }

    public Sale CreateSale(string clientId)
    {
        if (string.IsNullOrEmpty(clientId))
            throw new ValidationException("ClientId is required");

        var sale = new Sale(clientId);
        _repository.Save(sale);
        return sale;
    }

    public Sale GetById (string saleId)
    {
        var sale = _repository.GetById(saleId);
        if (sale == null)
            throw new NotFoundException ("Sale not Found");
        return sale ;

    }

    public void AddItem(string saleId, string productId, int quantity)
    {
        var sale = _repository.GetById(saleId);

        if (sale == null)
            throw new ValidationException("Sale not found");
        
        if (!_productServiceFake.ProductsExists(productId))
            throw new NotFoundException("product not found");

        if (quantity <= 0)
            throw new ValidationException ("Invalid quantity");

        var stock = _productServiceFake.GetStock(productId);
        if (quantity > stock)
            throw new BusinessException("Insufficient stock");
        
        sale.AddItem(productId, quantity);
        _repository.Update(sale);

    }

    public void FinishSale(string saleId)
    {
        var sale = _repository.GetById(saleId);
        if(sale ==null)
            throw new NotFoundException("Sale not found");

        // percorre estoque 
        foreach (var item in sale.Items)
        {
            var stock = _productServiceFake.GetStock(item.ProductId);

            if (item.Quantity > stock)
                throw new BusinessException($"Insufficient stock for product {item.ProductId}");
            
        }

        sale.Finish();
        _repository.Update(sale);

    }

    public void CancelSale(string saleId)
    {
        var sale = _repository.GetById(saleId);

        if (sale == null)
            throw new NotFoundException ("Sale not found");
        
        sale.Cancel();

        _repository.Update(sale);
    }


}
