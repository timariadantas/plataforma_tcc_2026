CREATE TABLE IF NOT EXISTS sales (
    id VARCHAR(26) PRIMARY KEY,
    client_id VARCHAR(26) NOT NULL,
    status INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS sales_items (
    sale_id VARCHAR(26),
    product_id VARCHAR(26),
    quantity INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP

    CONSTRAINT fk_sale
        FOREIGN KEY (sale_id)
        REFERENCES sales(id)
);

-- Buscar vendas por cliente
CREATE INDEX IF NOT EXISTS idx_sales_client_id
ON sales(client_id);

-- Buscar itens de uma venda
CREATE INDEX IF NOT EXISTS idx_sale_items_sale_id
ON sale_items(sale_id);