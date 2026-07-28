using Microsoft.AspNetCore.Mvc;
using SalesService.Application.DTO.Request;
using SalesService.Application.DTO.Response;
using SalesService.Application.Mapper;
using SalesService.Application.Repositories;
using System;
using Microsoft.AspNetCore.Authorization;


namespace SalesService.Api.Controllers;
[Authorize]
[ApiController]
[Route("sales")]
public class SalesController : ControllerBase
{
    private readonly ISaleService _service;
    private readonly ILogger<SalesController> _logger;

    public SalesController(ISaleService service, ILogger<SalesController>logger)
    {
        _service = service;
        _logger = logger;

    }

    [HttpPost]
    public async Task <IActionResult> Create()
   {

        var clientId = User.FindFirst("client_id")?.Value;
        if (clientId == null)
            return Unauthorized();

        _logger.LogInformation(
        "Creating sale for client {ClientId}",clientId);

        var sale = await _service.CreateSale(clientId);
    
        var response = SaleMapper.ToResponse(sale);

       var result = new ApiResponse<SaleResponse>
        {
            Message = "Sale created successfully",
            Elapsed = 0,
            Data = response
        };

        return Created("", result);
    }

    [HttpGet("{id}")]
    public IActionResult GetById(string id)
    {
        _logger.LogInformation(
            "Fetching sale {SaleId}", id);

        var sale =  _service.GetById(id);
        var response = SaleMapper.ToResponse(sale);
        
        var result = new ApiResponse<SaleResponse>
        {
            Message = "Sale found",
            Elapsed = 0,
            Data = response
        };

        return Ok(result);
    }

    [HttpPost("{id}/items")]
    public async Task<IActionResult> AddItem(string id, 
    [FromBody] AddItemRequest request)
    {
        _logger.LogInformation(
            "Adding product {ProductId} to sale {SaleId}", request.ProductId, id);

        await _service.AddItem(
            id, 
            request.ProductId,
            request.Quantity);

       var result = new ApiResponse<object>
    {
        Message = "Item added successfully",
        Elapsed = 0,
        Data = null
    };

    return Ok(result);
    }

    [HttpPut("{saleId}/items/{productId}")]
    public async Task<IActionResult> UpdateItem(
        string saleId,
        string productId,

        [FromBody] UpdateItemRequest request
         )
    {
        _logger.LogInformation(
            "Updating product {ProductId} in sale {SaleId}",
                productId,
                saleId);

        await _service.UpdateItem(
            saleId,
            productId,
            request.Quantity);

        return Ok(new
        {
            success = true,
            message = "Item updated"
        });
    }

    [HttpPost("{id}/finish")]
    public async Task <IActionResult> Finish(string id)
    {
        _logger.LogInformation(
            "Finishing sale {SaleId}", id);

        var totals = await _service.FinishSale(id);

        var result = new ApiResponse<object>
    {
        Message = "Sale finished successfully",
        Elapsed = 0,
        Data = totals,
    };

    return Ok(result);
    }            
        

    [HttpPost("{id}/cancel")]
    public IActionResult Cancel(string id)
    {
        _logger.LogInformation(
            "Canceling sale {SaleId}", id);

        _service.CancelSale(id);
        
        var result = new ApiResponse<object>
    {
        Message = "Sale canceled successfully",
        Elapsed = 0,
        Data = null
    };

    return Ok(result);
    }

    [HttpGet("product/{productId}")]
    public async Task<IActionResult>GetByProduct(string productId)
    {
         _logger.LogInformation(
            "Fetching sales by product {ProductId}", productId);

        var sales = await _service.GetByProductId(productId);

        var response = sales
            .Select(SaleMapper.ToResponse)
            .ToList();

        var result = new ApiResponse<List<SaleResponse>>
    {
        Message = "Sales found",
        Elapsed = 0,
        Data = response
    };

    return Ok(result);
    }

    [HttpGet("status/{status}")]
    public async Task<IActionResult> GetByStatus(string status)
    {
        _logger.LogInformation(
            "Fetching sales by status {Status}", status);

        var sales = await _service.GetByStatus(status);

        var response = sales
        .Select(SaleMapper.ToResponse)
        .ToList();

        var result = new ApiResponse<List<SaleResponse>>
    {
        Message = "Sales found",
        Elapsed = 0,
        Data = response
    };

    return Ok(result);
    }

    [HttpGet("product/{productId}/totals")]
    public async Task<IActionResult> GetTotals(string productId)
        {
             _logger.LogInformation(
            "Fetching totals for product {ProductId}",productId);

            var totals = 
                await _service.GetTotalSalesByProductAndStatus(productId);

            var result =
                new ApiResponse<Dictionary<Domain.Enums.SaleStatus, int>>
            {
                Message = "Totals found",
                Elapsed = 0,
                Data = totals
            };

        return Ok(result); 
        
        }



}

