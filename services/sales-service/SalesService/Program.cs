using SalesService.API.Middlewares;
using SalesService.Application.Repositories;
using SalesService.Application.Services;
using SalesService.Domain.Repositories;
using SalesService.Infrastructute.Repositories;
using SalesService.Infrastructute.DataBase;
using DotNetEnv;

Env.Load();

var builder = WebApplication.CreateBuilder(args);


// controllers
builder.Services.AddControllers();


// swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();


// repository
builder.Services.AddScoped<ISaleRepository, SaleRepository>();

builder.Services.AddScoped<IDbConnectionFactory, DbConnection>();

// service principal
builder.Services.AddScoped<ISaleService, SaleService>();


// Product Service (porta 5001)
builder.Services.AddHttpClient<IProductService, ProductServiceClient>(client =>
{
    client.BaseAddress = new Uri("http://localhost:5001");
});


// Currency Service (porta 5001)
builder.Services.AddHttpClient<ICurrencyService, CurrencyServiceClient>(client =>
{
    client.BaseAddress = new Uri("http://localhost:5001");
});
// logs
builder.Logging.ClearProviders();
builder.Logging.AddConsole();

var app = builder.Build();


// swagger
app.UseSwagger();
app.UseSwaggerUI();


// middleware global
app.UseMiddleware<ExceptionMiddleware>();


app.MapControllers();

app.Run();