using Npgsql;
using SalesService.Domain.Entities;
using SalesService.Domain.Enums;
using SalesService.Domain.Repositories;
using SalesService.Infrastructute.Executor;
using Microsoft.Extensions.Logging;

namespace SalesService.Infrastructute.Repositories;

public class SaleRepository : ISaleRepository

{
    private readonly ILogger<SaleRepository> _logger;
    private readonly IDbConnectionFactory _connectionFactory;
    private readonly IDatabaseExecutor _databaseExecutor;
    public SaleRepository(ILogger<SaleRepository> logger,
                            IDbConnectionFactory connectionFactory,
                            IDatabaseExecutor databaseExecutor)
    {
        _logger = logger;
         _connectionFactory = connectionFactory;
         _databaseExecutor = databaseExecutor;
    }
    public void Save(Sale sale)
    {
        _logger.LogInformation(
            "Saving sale {SaleId} in database", sale.Id);

        using var connection = _connectionFactory.CreateConnection();
        connection.Open();

        using var transaction = connection.BeginTransaction();
        try
        {
          _databaseExecutor.Execute(
            @"
            INSERT INTO sales
            (
                id,
                client_id,
                status,
                created_at,
                updated_at
            )
            VALUES
            (
                @id,
                @client_id,
                @status,
                @created_at,
                @updated_at
            )",
            connection,
            transaction,
            new Dictionary<string, object>
            {
                ["id"] = sale.Id,
                ["client_id"] = sale.ClientId,
                ["status"] = sale.Status.ToString(),
                ["created_at"] = sale.CreatedAt,
                ["updated_at"] = sale.UpdatedAt
            });

        foreach (var item in sale.Items)
        {
            _databaseExecutor.Execute(
                @"
                INSERT INTO sale_items
                (
                    sale_id,
                    product_id,
                    quantity,
                    unit_price,
                    created_at,
                    updated_at
                )
                VALUES
                (
                    @sale_id,
                    @product_id,
                    @quantity,
                    @unit_price,
                    @created_at,
                    @updated_at
                )",
                connection,
                transaction,
                new Dictionary<string, object>
                {
                    ["sale_id"] = item.SaleId,
                    ["product_id"] = item.ProductId,
                    ["quantity"] = item.Quantity,
                    ["unit_price"] = item.UnitPrice,
                    ["created_at"] = item.CreatedAt,
                    ["updated_at"] = item.UpdatedAt
                });
        }

        transaction.Commit();
    }
    catch
    {
        transaction.Rollback();
        throw;
    }
}

 public Sale? GetById(string id)
{
    _logger.LogInformation(
        "Fetching sale {SaleId} from database", id);

    using var connection = _connectionFactory.CreateConnection();
    connection.Open();

    Sale? sale = null;

    using (var reader = _databaseExecutor.Query(
        @"
        SELECT
            id,
            client_id,
            status,
            created_at,
            updated_at
        FROM sales
        WHERE id = @id",
        connection,
        new Dictionary<string, object>
        {
            ["id"] = id
        }))
    {
        if (!reader.Read())
        {
            _logger.LogWarning(
                "Sale {SaleId} not found in database", id);

            return null;
        }

        sale = Sale.Rehydrate(
            reader.GetString(0),
            reader.GetString(1),
            Enum.Parse<SaleStatus>(reader.GetString(2)),
            reader.GetDateTime(3),
            reader.GetDateTime(4)
        );
    }

    using (var reader = _databaseExecutor.Query(
        @"
        SELECT
            product_id,
            quantity,
            unit_price,
            created_at,
            updated_at
        FROM sale_items
        WHERE sale_id = @sale_id",
        connection,
        new Dictionary<string, object>
        {
            ["sale_id"] = id
        }))
    {
        while (reader.Read())
        {
            sale!.LoadItem(
                reader.GetString(0),
                reader.GetInt32(1),
                reader.GetDecimal(2),
                reader.GetDateTime(3),
                reader.GetDateTime(4)
            );
        }
    }

    return sale;
}           
   
    public void Update(Sale sale)
{
    _logger.LogInformation(
        "Updating sale {SaleId} in database", sale.Id);

    using var connection = _connectionFactory.CreateConnection();
    connection.Open();

    using var transaction = connection.BeginTransaction();

    try
    {
        _databaseExecutor.Execute(
            @"
            UPDATE sales
            SET
                status = @status,
                updated_at = @updated_at
            WHERE id = @id",
            connection,
            transaction,
            new Dictionary<string, object>
            {
                ["id"] = sale.Id,
                ["status"] = sale.Status.ToString(),
                ["updated_at"] = sale.UpdatedAt
            });

        _databaseExecutor.Execute(
            @"
            DELETE FROM sale_items
            WHERE sale_id = @sale_id",
            connection,
            transaction,
            new Dictionary<string, object>
            {
                ["sale_id"] = sale.Id
            });

        foreach (var item in sale.Items)
        {
            _databaseExecutor.Execute(
                @"
                INSERT INTO sale_items
                (
                    sale_id,
                    product_id,
                    quantity,
                    unit_price,
                    created_at,
                    updated_at
                )
                VALUES
                (
                    @sale_id,
                    @product_id,
                    @quantity,
                    @unit_price,
                    @created_at,
                    @updated_at
                )",
                connection,
                transaction,
                new Dictionary<string, object>
                {
                    ["sale_id"] = item.SaleId,
                    ["product_id"] = item.ProductId,
                    ["quantity"] = item.Quantity,
                    ["unit_price"] = item.UnitPrice,
                    ["created_at"] = item.CreatedAt,
                    ["updated_at"] = item.UpdatedAt
                });
        }

        transaction.Commit();
    }
    catch
    {
        transaction.Rollback();
        throw;
    }
}
   
   public List<Sale> GetByProductId(string productId)
{
    using var connection = _connectionFactory.CreateConnection();
    connection.Open();

    var sales = new List<Sale>();

    using var reader = _databaseExecutor.Query(
        @"
        SELECT DISTINCT
            s.id,
            s.client_id,
            s.status,
            s.created_at,
            s.updated_at
        FROM sales s
        INNER JOIN sale_items si
            ON s.id = si.sale_id
        WHERE si.product_id = @product_id",
        connection,
        new Dictionary<string, object>
        {
            ["product_id"] = productId
        });

    while (reader.Read())
    {
        var sale = Sale.Rehydrate(
            reader.GetString(0),
            reader.GetString(1),
            Enum.Parse<SaleStatus>(reader.GetString(2)),
            reader.GetDateTime(3),
            reader.GetDateTime(4)
        );

        sales.Add(sale);
    }

    return sales;
}
    public List<Sale> GetByStatus(SaleStatus status)
{
    using var connection = _connectionFactory.CreateConnection();
    connection.Open();

    var sales = new List<Sale>();

    using var reader = _databaseExecutor.Query(
        @"
        SELECT
            id,
            client_id,
            status,
            created_at,
            updated_at
        FROM sales
        WHERE status = @status",
        connection,
        new Dictionary<string, object>
        {
            ["status"] = status.ToString()
        });

    while (reader.Read())
    {
        var sale = Sale.Rehydrate(
            reader.GetString(0),
            reader.GetString(1),
            Enum.Parse<SaleStatus>(reader.GetString(2)),
            reader.GetDateTime(3),
            reader.GetDateTime(4)
        );

        sales.Add(sale);
    }

    return sales;
}
   public Dictionary<SaleStatus, int> GetTotalSalesByProductAndStatus(string productId)
{
    using var connection = _connectionFactory.CreateConnection();
    connection.Open();

    var result = new Dictionary<SaleStatus, int>();

    using var reader = _databaseExecutor.Query(
        @"
        SELECT
            s.status,
            COUNT(*)
        FROM sales s
        INNER JOIN sale_items si
            ON s.id = si.sale_id
        WHERE si.product_id = @product_id
        GROUP BY s.status",
        connection,
        new Dictionary<string, object>
        {
            ["product_id"] = productId
        });

    while (reader.Read())
    {
        var status = Enum.Parse<SaleStatus>(reader.GetString(0));
        var count = reader.GetInt32(1);

        result[status] = count;
    }
    return result;
}
}
    

