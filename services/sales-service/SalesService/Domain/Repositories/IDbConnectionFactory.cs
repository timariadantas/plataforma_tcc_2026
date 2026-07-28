using System.Data;

namespace SalesService.Domain.Repositories;

public interface IDbConnectionFactory
{
    IDbConnection CreateConnection();
}
