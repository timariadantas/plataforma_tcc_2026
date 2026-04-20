using SalesService.Domain.Enums;
using SalesService.Domain.ValueObjects;

namespace SalesService.Domain.Entities;

public class Sale
{
    public string Id {get; private set;}
    public string ClientId{get; private set;}
    public SaleStatus Status {get; private set;}

    public DateTime CreatedAt{get; private set;}
    public DateTime UpdatedAt{get; private set;}

    private readonly List<SaleItem> _items = new();
    public IReadOnlyCollection<SaleItem> Items => _items;

    private Sale()
    {
        Id = string.Empty;
        ClientId = string.Empty;
    }

    public Sale(string clientId){
        if (string.IsNullOrEmpty(clientId))
            throw new Exception("Client is required.");

        Id = Ulid.New();
        ClientId = clientId;
        Status = SaleStatus.Started;
        CreatedAt = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;
    }

    public static Sale Rehydrate (
        string id, 
        string clientId,
        SaleStatus status,
        DateTime createdAt,
        DateTime updatedAt)
    {
        return new Sale
        {
            Id = id,
            ClientId = clientId,
            Status = status,
            CreatedAt = createdAt,
            UpdatedAt = updatedAt
        };
    }

    public void LoadItem(
        string productId,
        int quantity,
        DateTime createdAt,
        DateTime updatedAt)
    {
        var item = SaleItem.Rehydrate(
            Id,
            productId,
            quantity,
            createdAt,
            updatedAt
        );

        _items.Add(item);
    }


        // regra de negócio (Venda)
    public void AddItem(string productId, int quantity)
    {
        if (Status == SaleStatus.Done || Status == SaleStatus.Canceled)
            throw new Exception ("Sale cannot be changed.");
        if (quantity <= 0)
            throw new Exception("Quantity invalid.");

        var item = new SaleItem(Id, productId, quantity);
        _items.Add(item);

        Status = SaleStatus.Progress;
        UpdatedAt = DateTime.UtcNow;

    }

    public void Finish()
    {
        if (!_items.Any())
            throw new Exception("Sale has no items");
        
        if(Status == SaleStatus.Canceled)
            throw new Exception("Sale Canceled");

        Status = SaleStatus.Done;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Cancel()
    {
        if (Status == SaleStatus.Done)
            throw new Exception("Sale completed.");
        Status = SaleStatus.Canceled;
        UpdatedAt = DateTime.UtcNow;
    }

    


}
