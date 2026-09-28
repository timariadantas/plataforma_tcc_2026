using SalesService.Domain.Entities;
using SalesService.Domain.Exceptions;
using SalesService.Domain.Repositories;
using SalesService.Application.Repositories;
using SalesService.Application.DTO.Response;
using SalesService.Domain.Enums;
using Microsoft.Extensions.Logging;

namespace SalesService.Application.Services;

public class SaleService : ISaleService   
{
   private readonly ISaleRepository _repository;
   private readonly IClientService _clientservice;
   private readonly IProductService _productservice;
   private readonly ICurrencyService _currencyService; 
   private readonly ILogger<SaleService> _logger;

   public SaleService(
       ISaleRepository repository,
       IClientService clientservice,
       IProductService productservice,
       ICurrencyService currencyService,
       ILogger<SaleService> logger
   )
    {
        _repository = repository;
        _clientservice = clientservice;
        _productservice = productservice;
        _currencyService = currencyService;
        _logger = logger;
    }

    public async Task<Sale> CreateSale(string clientId)
    {
        _logger.LogInformation(
        "Creating sale for client {ClientId}", clientId);

        if (!await _clientservice.ClientExists(clientId))
            throw new NotFoundException("Client not found");

        var sale = new Sale(clientId);
        _repository.Save(sale);
        return sale;
    }

    public Sale GetById (string saleId)
    {
        var sale = _repository.GetById(saleId);
        if (sale == null)
            throw new NotFoundException ("Sale not Found");
        
        return sale;

    }

    public async Task AddItem(string saleId, string productId, int quantity)
{
    _logger.LogInformation(
        "Adding item {ProductId} to sale {SaleId}",
        productId,
        saleId);

    // busca a venda
    var sale = _repository.GetById(saleId);

    if (sale == null)
        throw new NotFoundException("Sale not found");

    if (quantity <= 0)
        throw new ValidationException("Invalid quantity");

    // consulta estoque no product-service
    var stock = await _productservice.GetStock(productId);

    _logger.LogInformation(
        "Stock returned from product service: {Stock}",
        stock);

    if (quantity > stock)
    {
        _logger.LogWarning(
            "Insufficient stock for product {ProductId}",
            productId);

        throw new BusinessException("Insufficient stock");
    }

    // consulta preço no product-service
    var price = await _productservice.GetPrice(productId);

    // adiciona item na entidade
    sale.AddItem(productId, quantity, price);


    // atualiza venda
    _repository.Update(sale);

    _logger.LogInformation(
        "Item {ProductId} added successfully to sale {SaleId}",
        productId,
        saleId);
}

    public async Task<SaleTotalResponse> FinishSale(string saleId)
{
    _logger.LogInformation(
        "Finishing sale {SaleId}",
        saleId);

    var sale = _repository.GetById(saleId);

    if (sale == null)
        throw new NotFoundException("Sale not found");

    // 1. Validação do estoque
    foreach (var item in sale.Items)
    {
        var stock = await _productservice.GetStock(item.ProductId);

        if (item.Quantity > stock)
        {
            _logger.LogWarning(
                "Insufficient stock for product {ProductId}",
                item.ProductId);

            throw new BusinessException(
                $"Insufficient stock for product {item.ProductId}");
        }
    }

    // 2. Baixa do estoque + compensação
    var decreasedItems = new List<SaleItem>();

    try
    {
        foreach (var item in sale.Items)
        {
            _logger.LogInformation(
                "Decreasing stock for product {ProductId}",
                item.ProductId);

            await _productservice.DecreaseStock(
                item.ProductId,
                item.Quantity);

            decreasedItems.Add(item);
        }
    }
    catch (Exception ex)
    {
        _logger.LogError(
            ex,
            "Error while decreasing stock for sale {SaleId}. Starting compensation.",
            saleId);

        // 3. Compensação
        foreach (var item in decreasedItems)
        {
            try
            {
                _logger.LogWarning(
                    "Compensating stock for product {ProductId}",
                    item.ProductId);

                await _productservice.IncreaseStock(
                    item.ProductId,
                    item.Quantity);

                _logger.LogInformation(
                    "Stock compensation completed for product {ProductId}",
                    item.ProductId);
            }
            catch (Exception compensationException)
            {
                _logger.LogCritical(
                    compensationException,
                    "CRITICAL: Stock compensation failed for product {ProductId} in sale {SaleId}. Manual intervention may be required.",
                    item.ProductId,
                    saleId);
            }
        }

        throw;
    }

    // 4. Finaliza a venda
    sale.Finish();
    _repository.Update(sale);

    // 5. Busca as cotações
    var rates = await _currencyService.GetAllRates();

    var totals = new Dictionary<string, decimal>();

    foreach (var rate in rates)
    {
        totals[rate.Key] =
            Math.Round(sale.Total / rate.Value, 2);
    }

    return new SaleTotalResponse
    {
        TotalBRL = sale.Total,
        Coins = totals
    };
}

    public void CancelSale(string saleId)
    {
        var sale = _repository.GetById(saleId);

        if (sale == null)
            throw new NotFoundException ("Sale not found");
        
        sale.Cancel();

        _repository.Update(sale);
    }

    public async Task UpdateItem(
        string saleId,
        string productId,
        int quantity
    )
    {
        var sale  = _repository.GetById(saleId);

        if(sale == null)
            throw new NotFoundException("Sale not found");
        if (quantity <= 0)
        throw new ValidationException("Invalid quantity");

        var stock = await _productservice.GetStock(productId);
        
        if (quantity > stock)
            throw new BusinessException("Insufficient stock");
            
        sale.UpdateItem(productId, quantity);
        _repository.Update(sale);

    }

    public Task<List<Sale>> GetByProductId(string productId)
    {
        var sales = _repository.GetByProductId(productId);
        return Task.FromResult(sales);  // O repository é síncrono
    }

    public Task<List<Sale>> GetByStatus(string status)
    {
        if (Enum.TryParse<SaleStatus>(status, true, out var parsedStatus))
        {
            var sales = _repository.GetByStatus(parsedStatus);

            return Task.FromResult(sales);
        }

        throw new ValidationException("Invalid status");
    }

    public Task<Dictionary<SaleStatus, int>>
         GetTotalSalesByProductAndStatus(string productId)
    {
        var result = _repository.GetTotalSalesByProductAndStatus(productId);

        return Task.FromResult(result);
    }

    
}
