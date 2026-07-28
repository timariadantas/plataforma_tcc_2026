using Xunit;
using SalesService.Application.Services;

namespace SalesServices.Tests.Application.Services;

public class CurrencyServiceTests
{
    [Fact]
    public async Task GetAllRates_Should_Return_All_Currencies()
    {
        // Arrange
        var service = new CurrencyService();

        // Act
        var result = await service.GetAllRates();

        // Assert
        Assert.NotNull(result);

        Assert.Equal(3, result.Count);

        Assert.Equal(5.10m, result["USD"]);
        Assert.Equal(5.50m, result["EUR"]);
        Assert.Equal(1m, result["BRL"]);
    }
}