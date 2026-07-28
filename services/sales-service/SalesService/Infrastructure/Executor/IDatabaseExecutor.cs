using System.Data;

namespace SalesService.Infrastructute.Executor;

public interface IDatabaseExecutor
{
    int Execute(
        string sql,
        IDbConnection connection,
        IDbTransaction? transaction,
        IReadOnlyDictionary<string, object> parameters);

    IDataReader Query(
        string sql,
        IDbConnection connection,
        IReadOnlyDictionary<string, object> parameters);

    IDataReader Query(
        string sql,
        IDbConnection connection,
        IDbTransaction transaction,
        IReadOnlyDictionary<string, object> parameters);
}