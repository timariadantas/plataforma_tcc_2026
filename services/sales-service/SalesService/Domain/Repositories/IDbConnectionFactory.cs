using Npgsql;

namespace SalesService.Domain.Repositories;

public interface IDbConnectionFactory
{
    NpgsqlConnection CreateConnection();
}
