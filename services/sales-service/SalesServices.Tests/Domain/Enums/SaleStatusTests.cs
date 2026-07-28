using SalesService.Domain.Enums;

namespace SalesServices.Tests.Domain.Enums;

public class SaleStatusTests
{
    [Fact]
    public void Should_Have_Correct_Values()
    {
        Assert.Equal(0, (int)SaleStatus.Started);
        Assert.Equal(1, (int)SaleStatus.Progress);
        Assert.Equal(2, (int)SaleStatus.Done);
        Assert.Equal(3, (int)SaleStatus.Canceled);
    }

    [Fact]
    public void Should_Convert_To_String()
    {
        Assert.Equal("Started", SaleStatus.Started.ToString());
        Assert.Equal("Progress", SaleStatus.Progress.ToString());
        Assert.Equal("Done", SaleStatus.Done.ToString());
        Assert.Equal("Canceled", SaleStatus.Canceled.ToString());
    }
}