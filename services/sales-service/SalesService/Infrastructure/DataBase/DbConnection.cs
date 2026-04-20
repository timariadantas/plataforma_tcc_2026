using Npgsql;
namespace SalesService.Infrastructute.DataBase;

public static class DbConnection
{
    public static NpgsqlConnection GetConnection()
    {
        var host = Environment.GetEnvironmentVariable("DB_HOST") ??"localhost";
        var port = Environment.GetEnvironmentVariable("DB_PORT") ??"5432";
        var database = Environment.GetEnvironmentVariable("DB_NAME") ??"sales_db";
        var username = Environment.GetEnvironmentVariable("DB_USER") ??"postgres";
        var password = Environment.GetEnvironmentVariable("DB_PASSWORD") ??"postgres";

        var connectionString = 
            $"Host={host}; Port={port}; Username={username}; Passaword={password}; Database={database}";

        return new NpgsqlConnection(connectionString);


    }
}
