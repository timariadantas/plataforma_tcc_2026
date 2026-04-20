using NUlid;
namespace SalesService.Domain.ValueObjects;

public static class Ulid
{
    public static string New()
    {
        return NUlid.Ulid.NewUlid().ToString();
    }
}

// Centraliza geração
// se quiser trocar , muda aqui

