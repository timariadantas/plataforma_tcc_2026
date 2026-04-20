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
        try
        {
            var sale = _service.CreateSale(request.ClientId);
            var response = SaleMapper.ToResponse(sale);
            return Ok (new { success = true, data = response });
        }
        catch(Exception ex)
        {
            return BadRequest(new { success = false, error = ex.Message });
        }

    }

    [HttpGet("{id}")]
    public IActionResult GetById(string id)
    {
        try
        {
            var sale = _service.GetById(id);
            var response = SaleMapper.ToResponse(sale);
            return Ok (new { success = true, data = response });
        }
        catch(Exception ex)
        {
            return NotFound(new { success = false, error = ex.Message });
        }
    }

    [HttpPost("{id}/items")]
    public IActionResult AddItem(string id, [FromBody] AddItemRequest request)
    {
        try
        {
            _service.AddItem(id, request.ProductId,request.Quantity);
             return Ok(new { success = true });
        }
        catch(Exception ex)
        {
            return BadRequest(new { success = false, error = ex.Message });
        }
    }

    [HttpPost("{id}/finish")]
    public IActionResult Finish(string id)
    {
        try{
            _service.FinishSale(id);
            return Ok(new { success = true });

        }catch(Exception ex)
        {
            return BadRequest(new { success = false, error = ex.Message });
        }
    }

    [HttpPost("{id}/ cancel")]
    public IActionResult Cancel(string id)
    {
        try
        {
            _service.CancelSale(id);
            return Ok(new { success = true });
        }catch(Exception ex)
        {
            return BadRequest(new { success = false, error = ex.Message });
        }
    }

}
