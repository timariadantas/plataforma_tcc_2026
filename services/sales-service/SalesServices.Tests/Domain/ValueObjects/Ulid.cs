using SalesService.Domain.ValueObjects;

namespace SalesServices.Tests.Domain.ValueObjects;

public class UlidTests
{
    [Fact]
    public void Should_Generate_Id()
    {
        var id = Ulid.New();

        Assert.False(string.IsNullOrWhiteSpace(id));
    }

    [Fact]
    public void Should_Generate_Unique_Ids()
    {
        var id1 = Ulid.New();
        var id2 = Ulid.New();

        Assert.NotEqual(id1, id2);
    }

    [Fact]
    public void Should_Have_Length_26()
    {
        var id = Ulid.New();

        Assert.Equal(26, id.Length);
    }
}