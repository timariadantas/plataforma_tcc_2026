namespace SalesService.Domain.Entities;

public class SaleItem
{
    public string SaleId{get; private set;}
    public string ProductId{get; private set;}
    public int Quantity {get; private set;}

    public DateTime CreatedAt{get; private set;}
    public DateTime UpdatedAt{get; private set;}

    private SaleItem(){}

    public SaleItem (string saleId, string productId, int quantity)
    {
        SaleId = saleId;
        ProductId = productId;
        Quantity = quantity;
        CreatedAt = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;

    }

    public static SaleItem Rehydrate(
        string saleId,
        string productId,
        int quantity,
        DateTime createdAt,
        DateTime updatedAt)
    {
        return new SaleItem
        {
            SaleId = saleId,
            ProductId = productId,
            Quantity = quantity,
            CreatedAt = createdAt,
            UpdatedAt = updatedAt
        };
    }
    

    // regra do negócio 

    public void UpdateQuantity( int quantity)
    {
        if (quantity <= 0)
            throw new Exception("Quantity invalid.");
        
        Quantity = quantity;
        UpdatedAt = DateTime.UtcNow;
    }
}
