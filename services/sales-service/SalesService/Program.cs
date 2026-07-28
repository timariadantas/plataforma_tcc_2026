using SalesService.API.Middlewares;
using SalesService.Application.Repositories;
using SalesService.Application.Services;
using SalesService.Domain.Repositories;
using SalesService.Infrastructute.Repositories;
using SalesService.Infrastructute.DataBase;
using SalesService.Infrastructute.Executor;
using DotNetEnv;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

Env.Load();

var builder = WebApplication.CreateBuilder(args);


// controllers
builder.Services.AddControllers();


// swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();


builder.Services.AddScoped<ISaleRepository, SaleRepository>();
builder.Services.AddScoped<IDbConnectionFactory, DbConnection>();
builder.Services.AddScoped<IDatabaseExecutor, NpgsqlDatabaseExecutor>();

builder.Services.AddScoped<ISaleService, SaleService>();


builder.Services.AddHttpClient<IClientService, ClientServiceClient>(client =>
{
    client.BaseAddress = new Uri("http://client_service:5000");
});

// Product Service (porta 5001) container
builder.Services.AddHttpClient<IProductService, ProductServiceClient>(client =>
{
    client.BaseAddress = new Uri("http://product_service:5000");
});

builder.Services.AddScoped<ICurrencyService, CurrencyService>();

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = false,
            ValidateAudience = false,
            ValidateLifetime = false,
            ValidateIssuerSigningKey = true,

            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(Environment.GetEnvironmentVariable("JWT_SECRET")!)
            )
        };
        options.Events = new JwtBearerEvents
        {
            OnAuthenticationFailed = context =>
            {
                Console.WriteLine("===== JWT ERROR =====");
                Console.WriteLine(context.Exception.ToString());
                return Task.CompletedTask;
            },

            OnTokenValidated = context =>
            {
                Console.WriteLine("===== TOKEN VALIDADO =====");
                return Task.CompletedTask;
            }
        };
    });
    

builder.Services.AddAuthorization();

// logs
builder.Logging.ClearProviders();
builder.Logging.AddConsole();

var app = builder.Build();


// swagger
app.UseSwagger();
app.UseSwaggerUI();


// middleware global
app.UseMiddleware<ExceptionMiddleware>();

app.UseAuthentication();   
app.UseAuthorization(); 
app.MapControllers();

app.Run();