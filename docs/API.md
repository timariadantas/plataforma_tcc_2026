# Documentação da API

# Plataforma TCC 2026

---

# Índice

- Introdução
- Arquitetura da Plataforma
- Autenticação
- Convenções da API
- Client Service
- Product Service
- Sales Service
- Currency Service
- Fluxo Completo
- Códigos HTTP
- Observações

---

# Introdução

Esta documentação descreve todos os endpoints disponíveis na Plataforma de Microserviços para Gerenciamento de Vendas.

A aplicação foi desenvolvida utilizando arquitetura de microserviços, onde cada serviço possui responsabilidade única, banco de dados próprio e comunicação através de APIs REST utilizando HTTP.

Toda a plataforma encontra-se containerizada utilizando Docker e Docker Compose.

Os serviços disponíveis são:

- Client Service
- Product Service
- Sales Service
- Currency Service

---

# Arquitetura da Plataforma

```
                   Cliente
                      │
                      │
              Client Service
              Python + Flask
                      │
                     JWT
                      │
     ---------------------------------------
     │                 │                  │
     │                 │                  │

Product Service   Sales Service    Currency Service
Python            C# ASP.NET Core
MongoDB           PostgreSQL
```

O Sales Service atua como orquestrador do fluxo de vendas, realizando chamadas aos demais serviços sempre que necessário.

---

# Autenticação

A autenticação da plataforma é baseada em JWT (JSON Web Token).

O token é gerado pelo Client Service durante o processo de login.

Após autenticado, o cliente deverá enviar o token no cabeçalho Authorization.

## Header

```http
Authorization: Bearer {TOKEN}
```

Exemplo:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Todos os endpoints protegidos exigem este cabeçalho.

---

# Convenções da API

## Content-Type

```http
Content-Type: application/json
```

---

## Datas

Formato ISO-8601.

Exemplo

```text
1999-05-20
```

---

## Identificadores

A plataforma utiliza identificadores únicos para clientes, produtos e vendas.

Clientes:
UUID

Produtos:
UUID

Vendas:
ULID

---

# CLIENT SERVICE

Base URL

```
http://localhost:5000
```

O Client Service é responsável pelo gerenciamento dos clientes da plataforma e pelo processo de autenticação dos usuários.

Principais responsabilidades:

- Cadastro de clientes
- Consulta de clientes
- Atualização
- Exclusão
- Alteração de senha
- Login
- Geração do JWT

---

# POST /clients

## Descrição

Realiza o cadastro de um novo cliente.

## Autenticação

Não requerida.

## URL

```
POST /clients
```

## Request

```json
{
    "name":"Maria",
    "surname":"Dantas",
    "email":"maria@test.com",
    "password":"123456",
    "birthdate":"1999-05-20"
}
```

## Curl

```bash
curl -X POST http://localhost:5000/clients \
-H "Content-Type: application/json" \
-d '{
"name":"Maria",
"surname":"Dantas",
"email":"maria@test.com",
"password":"123456",
"birthdate":"1999-05-20"
}'
```

## Response (201)

```json
{
    "id":"e175ced7-a086-4eb6-8c9a-814245533f46",
    "name":"Maria",
    "surname":"Dantas",
    "email":"maria@test.com",
    "birthdate":"1999-05-20",
    "active":true
}
```

## Possíveis respostas

| Código    | Descrição 

|201        | Cliente criado
|400        | Dados inválidos
|503        | Serviço indisponível

---

# POST /auth/login

## Descrição

Realiza a autenticação do usuário.

## Autenticação

Não requerida.

## URL

```
POST /auth/login
```

## Request

```json
{
    "email":"maria@test.com",
    "password":"123456"
}
```

## Curl

```bash
curl -X POST http://localhost:5000/auth/login \
-H "Content-Type: application/json" \
-d '{
"email":"maria@test.com",
"password":"123456"
}'
```

## Response (200)

```json
{
    "token":"eyJhbGciOiJIUzI1NiIs..."
}
```

## Possíveis respostas

| Código       |  Descrição 

|200           |  Login realizado
|401           |  Credenciais inválidas
|500           |  Erro interno

---

# GET /clients

## Descrição

Lista todos os clientes cadastrados.

## Autenticação

Obrigatória.

## URL

```
GET /clients
```

## Curl

```bash
curl http://localhost:5000/clients \
-H "Authorization: Bearer TOKEN"
```

## Response (200)

```json
[
    {
        "id":"...",
        "name":"Maria",
        "surname":"Dantas",
        "email":"maria@test.com",
        "birthdate":"1999-05-20",
        "active":true
    }
]
```

## Possíveis respostas

| Código    |   Descrição 

|200        |   Lista retornada
|401        |   Não autenticado
|503        |   Serviço indisponível

---

# GET /clients/{clientId}

## Descrição

Consulta um cliente pelo identificador.

## Autenticação

Obrigatória.

## URL

```
GET /clients/{clientId}
```

## Curl

```bash
curl http://localhost:5000/clients/CLIENT_ID \
-H "Authorization: Bearer TOKEN"
```

## Response (200)

```json
{
    "id":"...",
    "name":"Maria",
    "surname":"Dantas",
    "email":"maria@test.com",
    "birthdate":"1999-05-20",
    "active":true
}
```

## Possíveis respostas

| Código    |   Descrição 

|200        |   Cliente encontrado
|401        |   Não autenticado
|404        |   Cliente não encontrado
|503        |   Serviço indisponível

---

# GET /clients/active

## Descrição

Retorna apenas clientes ativos.

## Autenticação

Obrigatória.

## Curl

```bash
curl http://localhost:5000/clients/active \
-H "Authorization: Bearer TOKEN"
```

## Response (200)

```json
[
    {
        "id":"...",
        "name":"Maria",
        "active":true
    }
]
```

---

# GET /clients/inactive

## Descrição

Retorna apenas clientes inativos.

## Autenticação

Obrigatória.

## Curl

```bash
curl http://localhost:5000/clients/inactive \
-H "Authorization: Bearer TOKEN"
```

## Response (200)

```json
[
    {
        "id":"...",
        "name":"Maria",
        "active":false
    }
]
```

---

# PUT /clients/{clientId}

## Descrição

Atualiza os dados cadastrais de um cliente.

## Autenticação

Obrigatória.

## Request

```json
{
    "name":"Maria",
    "surname":"Dantas",
    "email":"novo@email.com",
    "password":"123456",
    "birthdate":"1999-05-20"
}
```

## Curl

```bash
curl -X PUT http://localhost:5000/clients/CLIENT_ID \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"name":"Maria",
"surname":"Dantas",
"email":"novo@email.com",
"password":"123456",
"birthdate":"1999-05-20"
}'
```

## Response (200)

```json
{
    "message":"updated"
}
```

---

# PATCH /clients/{clientId}/password

## Descrição

Atualiza a senha do cliente.

## Autenticação

Obrigatória.

## Request

```json
{
    "new_password":"novaSenha123"
}
```

## Curl

```bash
curl -X PATCH http://localhost:5000/clients/CLIENT_ID/password \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"new_password":"novaSenha123"
}'
```

## Response

```json
{
    "message":"Password updated successfully"
}
```

---

# DELETE /clients/{clientId}

## Descrição

Remove um cliente.

## Autenticação

Obrigatória.

## Curl

```bash
curl -X DELETE http://localhost:5000/clients/CLIENT_ID \
-H "Authorization: Bearer TOKEN"
```

## Response

```json
{
    "message":"deleted"
}
```

---

# GET /internal/clients/{clientId}

## Descrição

Endpoint interno utilizado pelo Sales Service para validar a existência de um cliente durante o fluxo de vendas.
Este endpoint não deve ser consumido diretamente por clientes externos.

## Autenticação

Não requerida (uso interno).

## Curl

```bash
curl http://localhost:5000/internal/clients/CLIENT_ID
```

## Response

```json
{
    "id":"...",
    "name":"Maria",
    "surname":"Dantas",
    "email":"maria@test.com",
    "birthdate":"1999-05-20",
    "active":true
}
```

---

# PRODUCT SERVICE

Base URL

```
http://localhost:5001
```

O Product Service é responsável pelo gerenciamento dos produtos da plataforma e pelo controle de estoque.

Além dos endpoints públicos utilizados pelos usuários autenticados, este serviço disponibiliza endpoints internos consumidos exclusivamente pelo Sales Service durante o processamento das vendas.

Principais responsabilidades:

- Cadastro de produtos
- Consulta de produtos
- Atualização de produtos
- Exclusão de produtos
- Controle de estoque
- Fornecimento de informações internas (preço e quantidade)

Tecnologias:

- Python
- Flask
- MongoDB

---

# POST /products

## Descrição

Realiza o cadastro de um novo produto.

## Autenticação

Obrigatória.

## URL

```
POST /products
```

## Request

```json
{
    "name":"Notebook Gamer",
    "description":"RTX 4070",
    "price":5000,
    "quantity":10
}
```

## Curl

```bash
curl -X POST http://localhost:5001/products \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"name":"Notebook Gamer",
"description":"RTX 4070",
"price":5000,
"quantity":10
}'
```

## Response (201)

```json
{
    "id":"e7eccd74-0fd1-4ac6-991a-7fc93d8f9a7c",
    "name":"Notebook Gamer",
    "description":"RTX 4070",
    "price":5000,
    "quantity":10,
    "created_by":"CLIENT_ID"
}
```

## Possíveis respostas

| Código    | Descrição 

|201        |Produto criado
|400        |Dados inválidos
|401        |Não autenticado
|500        |Erro interno

---

# GET /products

## Descrição

Lista todos os produtos cadastrados utilizando paginação.

## Autenticação

Obrigatória.

## Query Parameters

| Nome  | Tipo      | Obrigatório 

|page   |integer    |Não
|limit  |integer    |Não

## Exemplo

```
GET /products?page=1&limit=10
```

## Curl

```bash
curl "http://localhost:5001/products?page=1&limit=10" \
-H "Authorization: Bearer TOKEN"
```

## Response (200)

```json
{
    "success":true,
    "page":1,
    "limit":10,
    "data":[
        {
            "id":"...",
            "name":"Notebook Gamer",
            "description":"RTX 4070",
            "price":5000,
            "quantity":10
        }
    ]
}
```

---

# GET /products/{productId}

## Descrição

Consulta um produto pelo identificador.

## Autenticação

Obrigatória.

## Curl

```bash
curl http://localhost:5001/products/PRODUCT_ID \
-H "Authorization: Bearer TOKEN"
```

## Response (200)

```json
{
    "id":"...",
    "name":"Notebook Gamer",
    "description":"RTX 4070",
    "price":5000,
    "quantity":10
}
```

## Possíveis respostas

| Código    |   Descrição 
|200        |   Produto encontrado
|401        |   Não autenticado|
|404        |   Produto não encontrado
|500        |   Erro interno

---

# PUT /products/{productId}

## Descrição

Atualiza as informações de um produto.

## Autenticação

Obrigatória.

## Request

```json
{
    "name":"Notebook RTX",
    "description":"RTX 4080",
    "price":6200,
    "quantity":15
}
```

## Curl

```bash
curl -X PUT http://localhost:5001/products/PRODUCT_ID \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"name":"Notebook RTX",
"description":"RTX 4080",
"price":6200,
"quantity":15
}'
```

## Response (200)

```json
{
    "message":"Product updated"
}
```

---

# DELETE /products/{productId}

## Descrição

Remove um produto.

## Autenticação

Obrigatória.

## Curl

```bash
curl -X DELETE http://localhost:5001/products/PRODUCT_ID \
-H "Authorization: Bearer TOKEN"
```

## Response

```json
{
    "message":"Product deleted"
}
```

---

# PATCH /products/{productId}/decrease-stock

## Descrição

Reduz a quantidade disponível em estoque.
Este endpoint pode ser utilizado para ajustes manuais de estoque.

## Autenticação

Obrigatória.

## Request

```json
{
    "quantity":2
}
```

## Curl

```bash
curl -X PATCH http://localhost:5001/products/PRODUCT_ID/decrease-stock \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"quantity":2
}'
```

## Response

```json
{
    "message":"Stock updated"
}
```

---

# ENDPOINTS INTERNOS

Os endpoints abaixo são utilizados exclusivamente pelo Sales Service durante o fluxo de processamento da venda.
Eles não fazem parte da API pública da plataforma.

---

# GET /internal/products/{productId}

## Descrição

Obtém todas as informações de um produto.

## Curl

```bash
curl http://localhost:5001/internal/products/PRODUCT_ID
```

## Response

```json
{
    "id":"...",
    "name":"Notebook",
    "description":"RTX",
    "price":5000,
    "quantity":10
}
```

---

# PATCH /internal/products/{productId}/decrease-stock

## Descrição

Atualiza o estoque após a finalização de uma venda.
Consumido pelo Sales Service.

## Request

```json
{
    "quantity":2
}
```

## Curl

```bash
curl -X PATCH http://localhost:5001/internal/products/PRODUCT_ID/decrease-stock \
-H "Content-Type: application/json" \
-d '{
"quantity":2
}'
```

## Response

```json
{
    "message":"Stock updated"
}
```

---

# GET /internal/products/{productId}/stock

## Descrição

Retorna apenas a quantidade disponível em estoque.
Utilizado pelo Sales Service antes da confirmação da venda.

## Curl

```bash
curl http://localhost:5001/internal/products/PRODUCT_ID/stock
```

## Response

```json
{
    "quantity":10
}
```

---

# GET /internal/products/{productId}/price

## Descrição

Retorna apenas o preço do produto.
Consumido pelo Sales Service durante o cálculo do valor da venda.

## Curl

```bash
curl http://localhost:5001/internal/products/PRODUCT_ID/price
```

## Response

```json
{
    "price":5000
}
```

---



---
# SALES SERVICE

Base URL

```
http://localhost:5008
```

O Sales Service é responsável pelo processamento completo das vendas da plataforma.

Este serviço atua como **orquestrador do fluxo de vendas**, comunicando-se com os demais microserviços para validar clientes, consultar produtos, atualizar estoque e obter cotações de moedas.

Principais responsabilidades:

- Criar vendas
- Adicionar produtos à venda
- Atualizar itens
- Finalizar vendas
- Cancelar vendas
- Consultar vendas
- Buscar vendas por produto
- Buscar vendas por status
- Calcular totais por produto

Tecnologias utilizadas:

- ASP.NET Core 8
- C#
- PostgreSQL

---

# POST /sales

## Descrição

Cria uma nova venda para o cliente autenticado.

O identificador do cliente é obtido automaticamente através do JWT.

## Autenticação

Obrigatória.

## URL

```
POST /sales
```

## Request

Não possui corpo (Body).

## Curl

```bash
curl -X POST http://localhost:5008/sales \
-H "Authorization: Bearer TOKEN"
```

## Response (201)

```json
{
  "message":"Sale created successfully",
  "timestamp":"2026-07-26T22:51:05Z",
  "elapsed":0,
  "data":{
      "id":"01KYG9ZWY44RYKBEVDYDN5D34Q",
      "clientId":"28e62ed7-9954-4d94-9694-275714c0660c",
      "status":"Started",
      "items":[]
  },
  "error":null
}
```

## Possíveis respostas

| Código | Descrição |
|---------|-----------|
|201|Venda criada|
|401|Usuário não autenticado|
|500|Erro interno|

---

# GET /sales/{saleId}

## Descrição

Consulta uma venda pelo identificador.

## Autenticação

Obrigatória.

## Curl

```bash
curl http://localhost:5008/sales/SALE_ID \
-H "Authorization: Bearer TOKEN"
```

## Response (200)

```json
{
  "message":"Sale found",
  "timestamp":"2026-07-26T22:51:05Z",
  "elapsed":0,
  "data":{
      "id":"01KYG9ZWY44RYKBEVDYDN5D34Q",
      "clientId":"28e62ed7-9954-4d94-9694-275714c0660c",
      "status":"Done",
      "items":[
          {
              "productId":"PRODUCT_ID",
              "quantity":2
          }
      ]
  },
  "error":null
}
```

---

# POST /sales/{saleId}/items

## Descrição

Adiciona um produto à venda.

Antes da inclusão, o Sales Service:

- verifica se o produto existe;
- consulta o estoque;
- valida a quantidade disponível.

## Request

```json
{
    "productId":"PRODUCT_ID",
    "quantity":2
}
```

## Curl

```bash
curl -X POST http://localhost:5008/sales/SALE_ID/items \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"productId":"PRODUCT_ID",
"quantity":2
}'
```

## Response

```json
{
    "message":"Item added successfully",
    "timestamp":"2026-07-26T22:51:05Z",
    "elapsed":0,
    "data":null,
    "error":null
}
```

---

# PUT /sales/{saleId}/items/{productId}

## Descrição

Atualiza a quantidade de um item existente na venda.

## Request

```json
{
    "quantity":5
}
```

## Curl

```bash
curl -X PUT http://localhost:5008/sales/SALE_ID/items/PRODUCT_ID \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"quantity":5
}'
```

## Response

```json
{
    "success":true,
    "message":"Item updated"
}
```

---

# POST /sales/{saleId}/finish

## Descrição

Finaliza a venda.

Durante este processo o Sales Service:

1. Consulta o preço dos produtos.
2. Consulta o estoque.
3. Atualiza o estoque no Product Service.
4. Consulta as cotações no Currency Service.
5. Calcula o valor final.
6. Marca a venda como concluída.

## Curl

```bash
curl -X POST http://localhost:5008/sales/SALE_ID/finish \
-H "Authorization: Bearer TOKEN"
```

## Response

```json
{
    "message":"Sale finished successfully",
    "timestamp":"2026-07-26T22:51:05Z",
    "elapsed":0,
    "data":{
        "BRL":10000,
        "USD":1830,
        "EUR":1685
    },
    "error":null
}
```

---

# POST /sales/{saleId}/cancel

## Descrição

Cancela uma venda.

## Curl

```bash
curl -X POST http://localhost:5008/sales/SALE_ID/cancel \
-H "Authorization: Bearer TOKEN"
```

## Response

```json
{
    "message":"Sale canceled successfully",
    "timestamp":"2026-07-26T22:51:05Z",
    "elapsed":0,
    "data":null,
    "error":null
}
```

---

# GET /sales/product/{productId}

## Descrição

Retorna todas as vendas que contêm determinado produto.

## Curl

```bash
curl http://localhost:5008/sales/product/PRODUCT_ID \
-H "Authorization: Bearer TOKEN"
```

## Response

```json
{
    "message":"Sales found",
    "timestamp":"2026-07-26T22:51:05Z",
    "elapsed":0,
    "data":[
        {
            "id":"SALE_ID",
            "status":"Done",
            "items":[]
        }
    ],
    "error":null
}
```

---

# GET /sales/status/{status}

## Descrição

Lista todas as vendas com determinado status.

Status aceitos:

- Started
- Done
- Cancelled

## Curl

```bash
curl http://localhost:5008/sales/status/Done \
-H "Authorization: Bearer TOKEN"
```

## Response

```json
{
    "message":"Sales found",
    "timestamp":"2026-07-26T22:51:05Z",
    "elapsed":0,
    "data":[
        {
            "id":"SALE_ID",
            "status":"Done"
        }
    ],
    "error":null
}
```

---

# GET /sales/product/{productId}/totals

## Descrição

Retorna a quantidade de vendas agrupadas por status para um determinado produto.

Este endpoint é utilizado para consultas estatísticas.

## Curl

```bash
curl http://localhost:5008/sales/product/PRODUCT_ID/totals \
-H "Authorization: Bearer TOKEN"
```

## Response

```json
{
    "message":"Totals found",
    "timestamp":"2026-07-26T22:51:05Z",
    "elapsed":0,
    "data":{
        "Started":3,
        "Done":12,
        "Cancelled":2
    },
    "error":null
}
```

---

# Fluxo interno do Sales Service

```
Cliente autenticado
        │
        ▼
Criação da venda
        │
        ▼
Adicionar itens
        │
        ▼
Consultar Product Service
        │
        ├── Verificar preço
        │
        ├── Verificar estoque
        │
        ▼
Finalizar venda
        │
        ├── Atualizar estoque
        │
        ├── Consultar Currency Service
        │
        ▼
Persistir venda
        │
        ▼
Retornar totais
```
---

# Currency Service

Base URL

```
http://localhost:5002
```

O Currency Service é responsável por fornecer as cotações das moedas utilizadas pelo Sales Service durante a finalização da venda.

Nesta versão do projeto, as cotações são mantidas em memória (In Memory), não utilizando banco de dados.

---

## Listar todas as moedas

**GET**

```
/currency
```

### Curl

```bash
curl http://localhost:5002/currency
```

### Response

```json
{
    "message": "Currencies found",
    "timestamp": "2026-07-27T12:00:00Z",
    "elapsed": 0,
    "data": [
        {
            "code": "USD",
            "value": 5.43
        },
        {
            "code": "EUR",
            "value": 6.12
        },
        {
            "code": "BRL",
            "value": 1.00
        }
    ]
}
```

---

## Buscar moeda por código

**GET**

```
/currency/{code}
```

### Exemplo

```
/currency/USD
```

### Curl

```bash
curl http://localhost:5002/currency/USD
```

### Response (200)

```json
{
    "message": "Currency found",
    "timestamp": "2026-07-27T12:00:00Z",
    "elapsed": 0,
    "data": {
        "code": "USD",
        "value": 5.43
    }
}
```

### Response (404)

```json
{
    "message": "Currency not found",
    "timestamp": "2026-07-27T12:00:00Z",
    "elapsed": 0,
    "error": "Invalid currency code"
}
```

---

# Fluxo Completo da Plataforma

```
Cliente
    │
    ▼
Cadastrar Cliente
    │
    ▼
Login
    │
    ▼
Receber JWT
    │
    ▼
Cadastrar Produto
    │
    ▼
Criar Venda
    │
    ▼
Adicionar Item
    │
    ▼
Consultar Produto
(Product Service)
    │
    ▼
Atualizar Estoque
(Product Service)
    │
    ▼
Consultar Cotação
(Currency Service)
    │
    ▼
Finalizar Venda
    │
    ▼
Consultar Venda
```

---

# Códigos HTTP utilizados

| Código | Significado 
|
| 200    | Requisição realizada com sucesso 
| 201    | Recurso criado com sucesso 
| 400    | Requisição inválida 
| 401    | Não autenticado 
| 404    | Recurso não encontrado 
| 500    | Erro interno do servidor 
| 503    | Serviço temporariamente indisponível 

--

# Comunicação entre os serviços

Durante o processamento de uma venda, o Sales Service realiza as seguintes integrações:

| Serviço           |  Objetivo 
                              
Client Service         Validar existência do cliente
Product Service        Consultar produto
Product Service        Consultar estoque
Product Service        Consultar preço
Product Service        Atualizar estoque
Currency Service       Obter cotação das moedas

Essa arquitetura mantém cada microserviço responsável apenas pelo seu domínio de negócio, promovendo baixo acoplamento e maior facilidade de manutenção e evolução da plataforma.


# Ferramentas utilizadas para testes

Durante o desenvolvimento da plataforma foram utilizadas diferentes estratégias de teste.

- Swagger
- curl
- Testes Unitários
- Testes de Integração
- Testes End-to-End (E2E)
- xUnit

---

# Observações

- Todos os serviços são executados em containers Docker.
- Cada microserviço possui banco de dados independente.
- O Sales Service atua como orquestrador do fluxo de vendas.
- A comunicação entre os serviços ocorre via HTTP.
- A autenticação é realizada através de JWT emitido pelo Client Service.
- Os identificadores das vendas utilizam ULID, permitindo ordenação cronológica e melhor desempenho em comparação ao UUID em cenários de persistência.

---