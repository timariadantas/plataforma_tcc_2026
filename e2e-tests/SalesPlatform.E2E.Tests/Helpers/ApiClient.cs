using System.Net.Http.Headers;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;


namespace SalesPlatform.E2E.Tests.Helpers;

public class ApiClient
{
    private readonly HttpClient _http = new();
    private const string ClientApi = "http://localhost:5000";
    private const string ProductApi = "http://localhost:5001";
    private const string SalesApi = "http://localhost:5008";


    public ApiClient()
    {
        _http = new HttpClient();
    }

    public void SetToken(string token)
    {
        _http.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", token);
    }

    public async Task<string> CreateClient()
    {
        var email = $"maria{Guid.NewGuid()}@test.com";
        var response =
            await _http.PostAsync(
                $"{ClientApi}/clients",
                new StringContent(
                    JsonConvert.SerializeObject(
                        new
                        {
                            name = "Maria",
                            surname = "Dantas",
                            email,
                            password = "123456",
                            birthdate = "1993-05-01"
                        }),
                        Encoding.UTF8,
                        "application/json"));

        response.EnsureSuccessStatusCode();
        return email;
    }


    public async Task<string> Login(string email)
    {
        var response =
            await _http.PostAsync(
                $"{ClientApi}/auth/login",
                new StringContent(
                    JsonConvert.SerializeObject(new
                    {
                        email,
                        password = "123456"
                    }),
                    Encoding.UTF8,
                    "application/json"));
        response.EnsureSuccessStatusCode();

        var json = JObject.Parse(await response.Content.ReadAsStringAsync());
        return json["token"]!.ToString();
    }

    public async Task<string> CreateProduct()
    {
        var response =
            await _http.PostAsync(
                $"{ProductApi}/products",
                new StringContent(
                    JsonConvert.SerializeObject(new
                    {
                        name = "Notebook",
                        description = "RTX",
                        price = 5000,
                        quantity = 10
                    }),
                    Encoding.UTF8,
                    "application/json"));

        response.EnsureSuccessStatusCode();
        var json =
        JObject.Parse(await response.Content.ReadAsStringAsync());
        return json["id"]!.ToString();
    }

    public async Task<string> CreateSale()
    {
        var response =
            await _http.PostAsync(
                $"{SalesApi}/sales",
                null);

        response.EnsureSuccessStatusCode();

        var json =
            JObject.Parse(await response.Content.ReadAsStringAsync());

        return json["id"]!.ToString();
    }
    public async Task AddItem(
        string saleId,
        string productId)
    {
        var response =
            await _http.PostAsync(
                $"{SalesApi}/sales/{saleId}/items",
                new StringContent(
                    JsonConvert.SerializeObject(new
                    {
                        productId,
                        quantity = 2
                    }),
                    Encoding.UTF8,
                    "application/json"));

        response.EnsureSuccessStatusCode();
    }

    public async Task FinishSale(string saleId)
    {
        var response =
            await _http.PostAsync(
                $"{SalesApi}/sales/{saleId}/finish",
                null);

        response.EnsureSuccessStatusCode();
    }

    public async Task CancelSale(string saleId)
    {
        var response =
            await _http.PostAsync(
                $"{SalesApi}/sales/{saleId}/cancel",
                null);

        response.EnsureSuccessStatusCode();
    }

    public async Task<JObject> GetSale(string saleId)
    {
        var response =
            await _http.GetAsync(
                $"{SalesApi}/sales/{saleId}");

        response.EnsureSuccessStatusCode();

        return JObject.Parse(
            await response.Content.ReadAsStringAsync());
    }

    public async Task<JObject> GetProduct(string productId)
{
    var response =
        await _http.GetAsync(
            $"{ProductApi}/products/{productId}");

    response.EnsureSuccessStatusCode();

    return JObject.Parse(
        await response.Content.ReadAsStringAsync());
}
}



