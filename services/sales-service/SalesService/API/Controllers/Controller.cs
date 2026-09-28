using Microsoft.AspNetCore.Mvc;
using SalesService.Domain.Exceptions;
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
        var startTime = DateTime.UtcNow;

        var clientId = User.FindFirst("client_id")?.Value;
        if (clientId == null)
            throw new UnauthorizedException("Authentication required");

        _logger.LogInformation(
        "Creating sale for client {ClientId}",clientId);

        var sale = await _service.CreateSale(clientId);
    
        var response = SaleMapper.ToResponse(sale);

        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds; 
        var result = new ApiResponse<SaleResponse> 
        {   
            Message = "Sale created successfully",
            Timestamp = DateTime.UtcNow,
            Elapsed = elapsed, Data = response 
        }; 
         
         return Created("", result);
   }
    [HttpGet("{id}")]
    public IActionResult GetById(string id)
    {
        var startTime = DateTime.UtcNow;
        _logger.LogInformation(
            "Fetching sale {SaleId}", id);

        var sale =  _service.GetById(id);
        var response = SaleMapper.ToResponse(sale);
        
        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds;

        var result = new ApiResponse<SaleResponse> 
        {   
            Message = "Sale found", 
            Timestamp = DateTime.UtcNow, 
            Elapsed = elapsed, 
            Data = response 
        }; 
        
        return Ok(result); 
    }
    [HttpPost("{id}/items")]
    public async Task<IActionResult> AddItem(string id, 
    [FromBody] AddItemRequest request)
    {
        var startTime = DateTime.UtcNow;

        _logger.LogInformation(
            "Adding product {ProductId} to sale {SaleId}", request.ProductId, id);

        await _service.AddItem(
            id, 
            request.ProductId,
            request.Quantity);

        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds;
        var result = new ApiResponse<object> 
        {
            Message = "Item added successfully", 
            Timestamp = DateTime.UtcNow, 
            Elapsed = elapsed, 
            Data = null
         };

         return Ok(result); 
    }
    [HttpPut("{saleId}/items/{productId}")]
    public async Task<IActionResult> UpdateItem(
        string saleId,
        string productId,[FromBody] UpdateItemRequest request)
    {
        var startTime = DateTime.UtcNow;

        _logger.LogInformation(
            "Updating product {ProductId} in sale {SaleId}",
                productId,
                saleId);

        await _service.UpdateItem(
            saleId,
            productId,
            request.Quantity);

        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds; 

        var result = new ApiResponse<object> 
        {  
            Message = "Item updated successfully", 
            Timestamp = DateTime.UtcNow, 
            Elapsed = elapsed, 
            Data = null 
        }; 
        return Ok(result); 
    }
    [HttpPost("{id}/finish")]
    public async Task <IActionResult> Finish(string id)
    {
        var startTime = DateTime.UtcNow;

        _logger.LogInformation(
            "Finishing sale {SaleId}", id);

        var totals = await _service.FinishSale(id);

        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds;
        var result = new ApiResponse<SaleTotalResponse> 
        { 
            Message = "Sale finished successfully", 
            Timestamp = DateTime.UtcNow, 
            Elapsed = elapsed, 
            Data = totals 
        }; 
        return Ok(result); 
        
    }
    [HttpPost("{id}/cancel")]
    public IActionResult Cancel(string id)
    {
        var startTime = DateTime.UtcNow;
        _logger.LogInformation(
            "Canceling sale {SaleId}", id);

        _service.CancelSale(id);

        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds; 
        var result = new ApiResponse<object> 
        { 
            Message = "Sale canceled successfully", 
            Timestamp = DateTime.UtcNow,
            Elapsed = elapsed, 
            Data = null 
        }; 
        return Ok(result); 
    }
    [HttpGet("product/{productId}")]
    public async Task<IActionResult>GetByProduct(string productId)
    {
        var startTime = DateTime.UtcNow;
         _logger.LogInformation(
            "Fetching sales by product {ProductId}", productId);

        var sales = await _service.GetByProductId(productId);

        var response = sales
            .Select(SaleMapper.ToResponse)
            .ToList();

        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds;
        var result = new ApiResponse<List<SaleResponse>> 
        { 
            Message = "Sales found", 
            Timestamp = DateTime.UtcNow, 
            Elapsed = elapsed, 
            Data = response 
            }; 
            return Ok(result); 
        }

    [HttpGet("status/{status}")]
    public async Task<IActionResult> GetByStatus(string status)
    {
        var startTime = DateTime.UtcNow;
        _logger.LogInformation(
            "Fetching sales by status {Status}", status);

        var sales = await _service.GetByStatus(status);

        var response = sales
        .Select(SaleMapper.ToResponse)
        .ToList();

        var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds; 
        var result = new ApiResponse<List<SaleResponse>> 
        { 
            Message = "Sales found", 
            Timestamp = DateTime.UtcNow, 
            Elapsed = elapsed, 
            Data = response 
            }; 

            return Ok(result); 
        }

    [HttpGet("product/{productId}/totals")]
    public async Task<IActionResult> GetTotals(string productId)
        {
            var startTime = DateTime.UtcNow;
            _logger.LogInformation(
            "Fetching totals for product {ProductId}",productId);

            var totals = 
                await _service.GetTotalSalesByProductAndStatus(productId);

            var elapsed = (long)( DateTime.UtcNow - startTime ).TotalMilliseconds; 
            var result = new ApiResponse<Dictionary<Domain.Enums.SaleStatus, int>> 
            { 
                Message = "Totals found", 
                Timestamp = DateTime.UtcNow, 
                Elapsed = elapsed, 
                Data = totals 
                }; 
                return Ok(result); 
                }
        }




