using Newtonsoft.Json.Linq;

namespace SalesPlatform.E2E.Tests.Helpers;

public static class JwtHelper
{
    public static string GetToken(string json)
    {
        return JObject.Parse(json)["token"]!.ToString();
    }
}