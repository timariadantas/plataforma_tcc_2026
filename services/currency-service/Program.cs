using CurrencyService.Application.Services;
using CurrencyService.Infrastructure.Middleware;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddHttpClient
<ICurrencyService,
CurrencyService.Application.Services.CurrencyService>(client=>
{
    client.Timeout = TimeSpan.FromSeconds(5);
});

var app = builder.Build();
var logger = app.Services
    .GetRequiredService<ILogger<Program>>();

    logger.LogInformation(
        "Currency Service started.");
        
app.Lifetime.ApplicationStopping.Register(() =>
{
    logger.LogInformation(
        "Currency Service stopping.");
});



if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseMiddleware<ExceptionMiddleware>();
app.MapControllers();


app.Run();
public partial class Program
{
}