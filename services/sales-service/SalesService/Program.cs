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
using Microsoft.Extensions.Http.Resilience;
using Polly;
using System.Text.Json;
using System.Text.Json.Serialization;
using SalesService.Application.DTO.Response;

Env.Load();

var builder = WebApplication.CreateBuilder(args);


// controllers
builder.Services
    .AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.DefaultIgnoreCondition =
            JsonIgnoreCondition.WhenWritingNull;

        options.JsonSerializerOptions.PropertyNamingPolicy =
            JsonNamingPolicy.CamelCase;
    });


// swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();


builder.Services.AddScoped<ISaleRepository, SaleRepository>();
builder.Services.AddScoped<IDbConnectionFactory, DbConnection>();
builder.Services.AddScoped<IDatabaseExecutor, NpgsqlDatabaseExecutor>();

builder.Services.AddScoped<ISaleService, SaleService>();


builder.Services
.AddHttpClient<IClientService, ClientServiceClient>(client =>
{
    client.BaseAddress = new Uri("http://client_service:5000");
    client.Timeout = TimeSpan.FromSeconds(5);
})
.AddResilienceHandler("client-service-resilience", pipeline =>
    {
        pipeline.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 2,
            Delay = TimeSpan.FromSeconds(1),
            BackoffType = DelayBackoffType.Exponential,
            UseJitter = true,

            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
            .Handle<HttpRequestException>()
            .HandleResult(response =>
                response.RequestMessage?.Method == HttpMethod.Get &&
                ((int)response.StatusCode >= 500 ||
                 response.StatusCode == System.Net.HttpStatusCode.RequestTimeout)),

            OnRetry = args =>
        {
            Console.WriteLine(
                $"===== RETRY CLIENT SERVICE ===== " +
                $"Tentativa: {args.AttemptNumber + 1} " +
                $"Delay: {args.RetryDelay.TotalSeconds:F2}s");

            return default;
        }

                
        });
    });

// Product Service (porta 5001) container
builder.Services
.AddHttpClient<IProductService, ProductServiceClient>(client =>
{
    client.BaseAddress = new Uri("http://product_service:5000");
    client.Timeout = TimeSpan.FromSeconds(5);
})
.AddResilienceHandler("product-service-resilience", pipeline =>
    {
        pipeline.AddRetry(new HttpRetryStrategyOptions
        {
            MaxRetryAttempts = 2,
            Delay = TimeSpan.FromSeconds(1),
            BackoffType = DelayBackoffType.Exponential,
            UseJitter = true,

            //retry para get
            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                .Handle<HttpRequestException>()
                .HandleResult(response =>
                    response.RequestMessage?.Method == HttpMethod.Get &&
                    ((int)response.StatusCode >= 500 ||
                     response.StatusCode == System.Net.HttpStatusCode.RequestTimeout))
        });
    });

builder.Services
    .AddHttpClient<ICurrencyService, CurrencyServiceClient>(client =>
    {
        client.BaseAddress =
            new Uri("http://currency_service:8080");

        client.Timeout =
            TimeSpan.FromSeconds(5);
    });

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = false,
            ValidateAudience = false,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,

            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(Environment.GetEnvironmentVariable("JWT_SECRET")!)
            
        ),
            // Pequena tolerância para diferença de relógio entre serviços/containers
            ClockSkew = TimeSpan.FromSeconds(30)
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
            },

             OnChallenge = async context =>
    {
        context.HandleResponse();

        var response = new ApiResponse<object>
        {
            Message = "Request failed",
            Timestamp = DateTime.UtcNow,
            Elapsed = 0,
            Error = "Authentication required"
        };

        context.Response.StatusCode =
            StatusCodes.Status401Unauthorized;

        context.Response.ContentType =
            "application/json";

        await context.Response.WriteAsJsonAsync(
            response,
            new JsonSerializerOptions
            {
                PropertyNamingPolicy =
                    JsonNamingPolicy.CamelCase,

                DefaultIgnoreCondition =
                    JsonIgnoreCondition.WhenWritingNull
            });
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