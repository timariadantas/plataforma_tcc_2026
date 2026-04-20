using Npgsql;
using SalesService.Domain.Entities;
using SalesService.Domain.Enums;
using SalesService.Domain.Repositories;
using SalesService.Infrastructute.DataBase;

namespace SalesService.Infrastructute.Repositories;

public class SaleRepository : ISaleRepository
{
    public void Save(Sale sale)
    {
        using var connection = DbConnection.GetConnection();
        connection.Open();

        using var transaction = connection.BeginTransaction();
        try
        {
            using (var command = new NpgsqlCommand(@"
                INSERT INTO sales (id, client_id, status, created_at, updated_at)
                VALUES (@id, @client_id, @status, @created_at, @updated_at)", connection, transaction))
            {
                command.Parameters.AddWithValue("id",sale.Id );
                command.Parameters.AddWithValue("client_id",sale.ClientId );
                command.Parameters.AddWithValue("status",sale.Status);
                command.Parameters.AddWithValue("created_at",sale.CreatedAt);
                command.Parameters.AddWithValue("updated_at",sale.UpdatedAt);

                command.ExecuteNonQuery();
            }

            foreach (var item in sale.Items)
            {
                using var command = new NpgsqlCommand(@"
                INSERT INTO sale_items
                (sale_id, product_id, quantity, created_at, updated_at)
                VALUES(@sale_id, @product_id, @quantity, @created_at, @updated_at)", connection, transaction);

                command.Parameters.AddWithValue("sale_id",item.SaleId);
                command.Parameters.AddWithValue("product_id",item.ProductId);
                command.Parameters.AddWithValue("quantity",item.Quantity);
                command.Parameters.AddWithValue("created_at",item.CreatedAt);
                command.Parameters.AddWithValue("updated_at",item.UpdatedAt);

                command.ExecuteNonQuery();
            }
            transaction.Commit();
        }
                catch
        {
            transaction.Rollback();
            throw;
        }
            }

        public Sale GetById(string id)
    {
        using var connection = DbConnection.GetConnection();
        connection.Open();

        Sale sale = null;
        // buscar a venda
        using (var command = new NpgsqlCommand(@"
            SELECT id, client_id, status, created_at, updated_at
            FROM sales
            WHERE id = @id", connection))
        {
            command.Parameters.AddWithValue("id", id);

            using var reader = command.ExecuteReader();
            if(!reader.Read())
                return null;
            
            sale = Sale.Rehydrate ( 
                reader.GetString(0),
                reader.GetString(1),
                (SaleStatus)reader.GetInt32(2),
                reader.GetDateTime(3),
                reader.GetDateTime(4)
            );
        }
        // buscar itens 
        using (var command = new NpgsqlCommand(@"
            SELECT product_id, quantity, created_at, updated_at
            FROM sale_items
            WHERE sale_id = @sale_id", connection))
        {
            command.Parameters.AddWithValue("sale_id", id);
            using var reader = command.ExecuteReader();

            while (reader.Read())
            {
                sale.LoadItem(
                    reader.GetString(0),
                    reader.GetInt32(1),
                    reader.GetDateTime(2),
                    reader.GetDateTime(3)
                );
            }
        }
        return sale;
    }

    public void Update(Sale sale)
    {
        using var connection = DbConnection.GetConnection();
        connection.Open();

        using var command = new NpgsqlCommand(@"
            UPDATE sales
            SET status = @status,
                updated_at = @updated_at
            WHERE id = @id", connection);
               
            command.Parameters.AddWithValue("id", sale.Id);
            command.Parameters.AddWithValue("status",(int)sale.Status);
            command.Parameters.AddWithValue("updated_at", sale.UpdatedAt);

            command.ExecuteNonQuery();

    }

    public List<Sale> GetByProductId(string productId)
    {
         using var connection = DbConnection.GetConnection();
         connection.Open();

         var sales = new List<Sale>();

         using var command = new NpgsqlCommand(@"
            SELECT DISTINT s.id, s.client_id, s.status, s.created_at, s.updated_at
            FROM sales s
            INNER JOIN sale_items si ON s.id = si.sale_id
            WHERE si.product_id = @product_id", connection);

            command.Parameters.AddWithValue("product_id", productId);

            using var reader = command.ExecuteReader();

            while (reader.Read())
        {
            var sale = Sale.Rehydrate(
                reader.GetString(0),
                reader.GetString(1),
                (SaleStatus)reader.GetInt32(2),
                reader.GetDateTime(3),
                reader.GetDateTime(4)
            );
            sales.Add(sale);
        }
        return sales;

    }

    public List<Sale> GetByStatus(SaleStatus status)
    {
        using var connection = DbConnection.GetConnection();
        connection.Open();

        var sales = new List<Sale>();

        using var command = new NpgsqlCommand(@"
            SELECT id , client_id, status, created_at, updated_at
            FROM sales
            WHERE status = @status", connection);

        command.Parameters.AddWithValue("status", (int)status);

        using var reader = command.ExecuteReader();

        while (reader.Read())
        {
            var sale = Sale.Rehydrate(
                reader.GetString(0),
                reader.GetString(1),
                (SaleStatus)reader.GetInt32(2),
                reader.GetDateTime(3),
                reader.GetDateTime(4)
            );
            sales.Add(sale);
        }
        return sales;

    }

    public Dictionary <SaleStatus, int> GetTotalSalesByProductAndStatus(string productId)
    {
        using var connection= DbConnection.GetConnection();
        connection.Open();

        var result = new Dictionary<SaleStatus,int>();
        using var command = new NpgsqlCommand (@"
            SELECT s.status, COUNT(*)
            FROM sales s
            INNER JOIN sale_items si ON s.id = si.sale_id
            WHERE si.product = @product_id
            GROUP BY s.status
            ", connection);

            command.Parameters.AddWithValue("product_id, productId");

            using var reader = command.ExecuteReader();

        while (reader.Read())
        {
            var status = (SaleStatus)reader.GetInt32(0);
            var count = reader.GetInt32(1);

            result[status] = count;
        }
        return result ;
    }
    




}
    

