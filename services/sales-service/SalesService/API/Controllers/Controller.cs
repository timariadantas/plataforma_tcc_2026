using Microsoft.AspNetCore.Mvc;
using SalesService.Application.DTO.Request;
using SalesService.Application.Mapper;
using SalesService.Application.Repositories;
using System;

namespace SalesService.Api.Controllers;

[ApiController]
[Route("sales")]
public class SalesController : ControllerBase
{
    private readonly ISaleService _service;

    public SalesController(ISaleService service)
    {
        _service = service;

    }

    [HttpPost]
    public IActionResult Create([FromBody] CreateSaleRequest request)
    {
        var sale = _service.CreateSale(request.ClientId);
        var response = SaleMapper.ToResponse(sale);
        return Created ("", new { success = true, data = response });
    }

    [HttpGet("{id}")]
    public IActionResult GetById(string id)
    {
        var sale = _service.GetById(id);
        var response = SaleMapper.ToResponse(sale);
        return Ok (new { success = true, data = response });
    }

    [HttpPost("{id}/items")]
    public IActionResult AddItem(string id, [FromBody] AddItemRequest request)
    {
        _service.AddItem(id, request.ProductId,request.Quantity);
        return Ok(new { success = true });
    }

    [HttpPost("{id}/finish")]
    public IActionResult Finish(string id)
    {
        _service.FinishSale(id);
         return Ok(new { success = true });
    }            
        

    [HttpPost("{id}/cancel")]
    public IActionResult Cancel(string id)
    {
        _service.CancelSale(id);
        return Ok(new { success = true });
    }
}
