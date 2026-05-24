namespace SalesService.Domain.Entities;
using SalesService.Domain.Exceptions;

public class SaleItem
{
    public string SaleId{get; private set;}
    public string ProductId{get; private set;}
    public int Quantity {get; private set;}
    public decimal UnitPrice {get; private set;}
    public decimal Total => Quantity * UnitPrice;

    public DateTime CreatedAt{get; private set;}
    public DateTime UpdatedAt{get; private set;}

    private SaleItem(){}

    public SaleItem (string saleId, string productId, int quantity, decimal unitPrice)
    {
         if (string.IsNullOrEmpty(productId))
            throw new ValidationException("ProductId is required");

        if (quantity <= 0)
            throw new ValidationException("Quantity invalid");
            
        SaleId = saleId;
        ProductId = productId;
        Quantity = quantity;
        UnitPrice = unitPrice;
        CreatedAt = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;

    }

    public static SaleItem Rehydrate(
        string saleId,
        string productId,
        int quantity,
        decimal unitPrice,
        DateTime createdAt,
        DateTime updatedAt)
    {
        return new SaleItem
        {
            SaleId = saleId,
            ProductId = productId,
            Quantity = quantity,
            UnitPrice = unitPrice,
            CreatedAt = createdAt,
            UpdatedAt = updatedAt
        };
    }
    

    // regra do negócio 

    public void UpdateQuantity( int quantity)
    {
        if (quantity <= 0)
            throw new ValidationException("Quantity invalid.");
        
        Quantity = quantity;
        UpdatedAt = DateTime.UtcNow;
    }
}
