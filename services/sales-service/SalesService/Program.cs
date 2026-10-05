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
        pipeline.AddCircuitBreaker(
        new HttpCircuitBreakerStrategyOptions
        {
            FailureRatio = 0.5,
            SamplingDuration = TimeSpan.FromSeconds(10),
            MinimumThroughput = 4,
            BreakDuration = TimeSpan.FromSeconds(10),

            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                .Handle<HttpRequestException>()
                .HandleResult(response =>
                    response.RequestMessage?.Method == HttpMethod.Get &&
                    ((int)response.StatusCode >= 500 ||
                     response.StatusCode == System.Net.HttpStatusCode.RequestTimeout)),

            OnOpened = args =>
            {
                Console.WriteLine(
                    "===== CIRCUIT BREAKER CLIENT ABERTO =====");

                return default;
            },

            OnClosed = args =>
            {
                Console.WriteLine(
                    "===== CIRCUIT BREAKER CLIENT FECHADO =====");

                return default;
            },

            OnHalfOpened = args =>
            {
                Console.WriteLine(
                    "===== CIRCUIT BREAKER CLIENT HALF-OPEN =====");

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
        // Retry: somente GET
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
                     response.StatusCode == System.Net.HttpStatusCode.RequestTimeout))
        });
    
    // Circuit Breaker : GET E PATCH
    pipeline.AddCircuitBreaker(
        new HttpCircuitBreakerStrategyOptions
        {
            FailureRatio = 0.5,
            SamplingDuration = TimeSpan.FromSeconds(10),
            MinimumThroughput = 4,
            BreakDuration = TimeSpan.FromSeconds(10),

            ShouldHandle = new PredicateBuilder<HttpResponseMessage>()
                .Handle<HttpRequestException>()
                .HandleResult(response =>
                    response.RequestMessage?.Method == HttpMethod.Get &&
                    ((int)response.StatusCode >= 500 ||
                     response.StatusCode == System.Net.HttpStatusCode.RequestTimeout)),

            OnOpened = args =>
            {
                Console.WriteLine(
                    "===== CIRCUIT BREAKER PRODUCT ABERTO =====");

                return default;
            },

            OnClosed = args =>
            {
                Console.WriteLine(
                    "===== CIRCUIT BREAKER PRODUCT FECHADO =====");

                return default;
            },

            OnHalfOpened = args =>
            {
                Console.WriteLine(
                    "===== CIRCUIT BREAKER PRODUCT HALF-OPEN =====");

                return default;
            }
        });
    });

builder.Services
    .AddHttpClient<ICurrencyService, CurrencyServiceClient>(client =>
    {
        client.BaseAddress =
            new Uri("http://currency_service:8080");

        client.Timeout =
            TimeSpan.FromSeconds(5);
    })
    .AddResilienceHandler("currency-service-resilience", pipeline =>
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
                     response.StatusCode ==
                        System.Net.HttpStatusCode.RequestTimeout))
        });

        pipeline.AddCircuitBreaker(
            new HttpCircuitBreakerStrategyOptions
            {
                FailureRatio = 0.5,
                SamplingDuration = TimeSpan.FromSeconds(10),
                MinimumThroughput = 4,
                BreakDuration = TimeSpan.FromSeconds(10),

                ShouldHandle =
                    new PredicateBuilder<HttpResponseMessage>()
                        .Handle<HttpRequestException>()
                        .HandleResult(response =>
                            response.RequestMessage?.Method ==
                                HttpMethod.Get &&
                            ((int)response.StatusCode >= 500 ||
                             response.StatusCode ==
                                System.Net.HttpStatusCode.RequestTimeout)),

                OnOpened = args =>
                {
                    Console.WriteLine(
                        "===== CIRCUIT BREAKER CURRENCY ABERTO =====");

                    return default;
                },

                OnClosed = args =>
                {
                    Console.WriteLine(
                        "===== CIRCUIT BREAKER CURRENCY FECHADO =====");

                    return default;
                },

                OnHalfOpened = args =>
                {
                    Console.WriteLine(
                        "===== CIRCUIT BREAKER CURRENCY HALF-OPEN =====");

                    return default;
                }
            });
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