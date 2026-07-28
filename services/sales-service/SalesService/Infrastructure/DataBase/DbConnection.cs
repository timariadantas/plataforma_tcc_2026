using System.Data;
using Npgsql;
using SalesService.Domain.Repositories;
namespace SalesService.Infrastructute.DataBase;

public class DbConnection : IDbConnectionFactory
{
    public  IDbConnection CreateConnection()
    {
        var host = Environment.GetEnvironmentVariable("POSTGRES_HOST") ;
        var port = Environment.GetEnvironmentVariable("POSTGRES_PORT") ;
        var database = Environment.GetEnvironmentVariable("POSTGRES_DB") ;
        var username = Environment.GetEnvironmentVariable("POSTGRES_USER") ;
        var password = Environment.GetEnvironmentVariable("POSTGRES_PASSWORD") ;

        if (string.IsNullOrWhiteSpace(host) ||
            string.IsNullOrWhiteSpace(port) ||
            string.IsNullOrWhiteSpace(database) ||
            string.IsNullOrWhiteSpace(username) ||
            string.IsNullOrWhiteSpace(password))
        {
            throw new Exception("Variáveis de ambiente do PostgreSQL não configuradas.");
        }

        var connectionString =
            $"Host={host};Port={port};Username={username};Password={password};Database={database}";

        return new NpgsqlConnection(connectionString);
    }

}