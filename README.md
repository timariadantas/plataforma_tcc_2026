# Plataforma TCC 2026

# Plataforma de Microserviços para Gerenciamento de Vendas

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de aplicar conceitos estudados durante o curso, envolvendo:

- Arquitetura de Microserviços
- APIs REST
- Comunicação HTTP
- Persistência de dados
- Segurança utilizando JWT
- Containers Docker
- Testes automatizados
- Integração entre serviços
- Desenvolvimento distribuído
- Boas práticas de Engenharia de Software


A plataforma tem como objetivo simular um ambiente real de comércio eletrônico, permitindo que usuários realizem operações relacionadas a clientes, produtos e vendas através de serviços independentes.

A solução foi desenvolvida utilizando arquitetura de microserviços, onde cada serviço possui uma responsabilidade específica, banco de dados próprio e pode ser executado de forma independente.

Toda a aplicação foi containerizada utilizando Docker e Docker Compose, garantindo isolamento dos serviços, padronização do ambiente e facilidade de execução.

Além da implementação dos serviços, o projeto contempla:

- Autenticação baseada em JWT
- Testes unitários
- Testes de integração
- Testes End-to-End (E2E)

---

# Visão geral da arquitetura

                   Cliente
                      |
                      |
              Client Service
              Python + Flask
                      |
                     JWT
                      |
    ----------------------------------
    |                |               |
    |                |               |

Product Service  Sales Service      Currency Service

Python           C# .NET
MongoDB          PostgreSQL


---

# Arquitetura dos Microserviços

A plataforma é composta pelos seguintes serviços:

---

## Client Service

Responsável pelo gerenciamento dos clientes e autenticação.

### Funcionalidades:

- Cadastro de clientes
- Login
- Geração de JWT
- Alteração de senha
- Consulta de clientes

### Tecnologias:

- Python
- Flask
- Oracle Database

---

## Product Service

Responsável pelo gerenciamento dos produtos e controle de estoque.

### Funcionalidades:

- Gerenciamento de produtos
- Consulta de produtos
- Controle de estoque
- Atualização de quantidade
- Operações internas consumidas pelo Sales Service

### Tecnologias:

- Python
- Flask
- MongoDB

------

## Currency Service

Responsável por fornecer as cotações de moedas utilizadas pelo Sales Service durante o processamento das vendas.

### Funcionalidades

- Consulta de cotações
- Fornecimento das moedas suportadas
- Integração interna com o Sales Service

### Tecnologias

- C#
- ASP.NET Core 8
- Persistência em memória (In Memory)

O Currency Service utiliza armazenamento em memória (In Memory), pois fornece dados temporários durante a execução da aplicação, não sendo necessária persistência em banco de dados.


## Sales Service

Responsável pelo fluxo completo de vendas.

### Funcionalidades:

- Criação de vendas
- Inclusão de itens
- Atualização de itens
- Finalização de vendas
- Cancelamento de vendas
- Consulta de vendas
- Validação de clientes
- Consulta de produtos
- Atualização de estoque
- Integração com serviço de cotação de moedas


### Tecnologias:

- C#
- ASP.NET Core 8
- PostgreSQL


---

# Comunicação entre serviços

A comunicação entre os microserviços ocorre através de APIs REST utilizando HTTP.

O **Sales Service atua como orquestrador do fluxo de venda**, realizando chamadas para outros serviços quando necessário.

Exemplo:

Cliente cria uma venda

    |
    ↓

Sales Service

    |
    |---- Client Service
    |       valida cliente
    |
    |---- Product Service
    |       consulta produto
    |       atualiza estoque
    |
    |---- Currency Service
            consulta cotação

---

# Arquitetura dos bancos de dados

Cada microserviço possui seu próprio banco de dados.

|   **Serviço**     |   **Banco**   |
|---|---|
| Client Service    | Oracle XE     |
| Product Service   | MongoDB       |
| Currency          | In Memory
| Sales Service     | PostgreSQL    |
 
Essa abordagem mantém o isolamento dos dados, reduz acoplamento e permite evolução independente dos serviços.

---

# Containerização Docker

Toda a plataforma é executada utilizando Docker Compose.

Serviços executados:

|  **Container**    |  **Responsabilidade** |
|---|                   ---|
| client_service    | API de clientes       |
| product_service   | API de produtos       |
| sales_service     | API de vendas         |
| oracle-db         | Banco de clientes     |
| mongo_db          | Banco de produtos     |
| postgres-sales    | Banco de vendas       |


## Executar a aplicação

docker compose up --build

Parar os containers
docker compose down


### Tecnologias Utilizadas
ASP.NET Core 8
Python 3
Flask
Oracle XE
MongoDB
PostgreSQL
Docker
Docker Compose
JWT
xUnit
curl
Bash

### Estrutura do projeto

plataforma_tcc_2026

├── services
│   ├── client-service
│   ├── product-service
│   └── sales-service
│
├── e2e-tests
│   ├── flows
│   ├── SalesPlatform.E2E.Tests
│   ├── run-e2e.sh
│   └── README.md
│
├── docker-compose.yml
│
├── docs
│   └── API.md
│
└── README.md

### Autenticação e Segurança

A plataforma utiliza autenticação baseada em JWT (JSON Web Token) para identificação dos usuários e proteção dos endpoints.

O processo de autenticação é realizado pelo Client Service, responsável por validar as credenciais e gerar o token de acesso.

**Fluxo de autenticação**
Usuário realiza o cadastro.
Usuário realiza login.
Client Service valida as informações.
Um JWT é gerado.
O token é utilizado nas chamadas protegidas dos serviços.

Exemplo:

Authorization: Bearer {token}

### Modelo atual de autorização

A versão atual implementa autenticação dos usuários, porém ainda não possui controle de acesso baseado em perfis.

Como evolução futura poderá ser implementado:

Role Based Access Control (RBAC)
Perfil administrador
Perfil cliente
Controle de permissões por recurso
Testes

### O projeto possui três níveis de testes:

Testes Unitários
Validam regras internas dos serviços.

Testes de Integração
Validam componentes internos e comunicação entre módulos.

Testes End-to-End
Local:

e2e-tests/

Executar:

cd e2e-tests

./run-e2e.sh

***O fluxo valida:***

-criação de cliente
-autenticação JWT
-criação de produto
-criação de venda
-inclusão de itens
-atualização de estoque
-finalização da venda
-consulta da venda

#### Fluxo principal da venda
    Cadastro cliente
        ↓
        Login
        ↓
    Geração JWT
        ↓
    Cadastro produto
        ↓
    Criação venda
        ↓
    Adicionar itens
        ↓
    Atualização estoque
        ↓
    Finalização venda
        ↓
    Consulta venda

### Documentação da API

A documentação detalhada dos endpoints está disponível em:

docs/API.md

Contendo:
-Client Service
-Product Service
-Sales Service
-Exemplos de requisições curl
-Exemplos de respostas

### Melhorias futuras

Possíveis evoluções da plataforma:

-Implementação de autorização baseada em Roles
-Gateway de API
-Observabilidade com métricas e logs centralizados
-Mensageria entre serviços utilizando filas
-Deploy em ambiente cloud
-Pipeline CI/CD

-Autoria

Projeto desenvolvido por:

Maria Dantas

Trabalho de Conclusão de Curso — 2026.
