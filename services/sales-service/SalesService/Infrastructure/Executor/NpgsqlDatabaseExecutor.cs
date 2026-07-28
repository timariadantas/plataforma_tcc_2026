using System.Data;
using Npgsql;


namespace SalesService.Infrastructute.Executor;

public class NpgsqlDatabaseExecutor : IDatabaseExecutor
{
    public int Execute(
        string sql,
        IDbConnection connection,
        IDbTransaction? transaction,
        IReadOnlyDictionary<string, object> parameters)
    {
        using var command = new NpgsqlCommand(
            sql,
            (NpgsqlConnection)connection,
            (NpgsqlTransaction?)transaction);

        foreach (var p in parameters)
            command.Parameters.AddWithValue(p.Key, p.Value);

        return command.ExecuteNonQuery();
    }

    public IDataReader Query(
        string sql,
        IDbConnection connection,
        IReadOnlyDictionary<string, object> parameters)
    {
        var command = new NpgsqlCommand(
            sql,
            (NpgsqlConnection)connection);

        foreach (var p in parameters)
            command.Parameters.AddWithValue(p.Key, p.Value);

        return command.ExecuteReader();
    }

    public IDataReader Query(
        string sql,
        IDbConnection connection,
        IDbTransaction transaction,
        IReadOnlyDictionary<string, object> parameters)
    {
        var command = new NpgsqlCommand(
            sql,
            (NpgsqlConnection)connection,
            (NpgsqlTransaction)transaction);

        foreach (var p in parameters)
            command.Parameters.AddWithValue(p.Key, p.Value);

        return command.ExecuteReader();
    }
}
